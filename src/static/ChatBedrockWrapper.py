import logging
from collections import defaultdict
from typing import Dict, Any, Optional, List, Tuple, Iterator, AsyncIterator

from langchain_aws import ChatBedrock
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.outputs import GenerationChunk
from langchain_core.pydantic_v1 import Field

# Configure logging
from langchain_core.runnables import RunnableConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN_COUNTER: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: {})


def get_total_number_of_tokens(call_id: str) -> int:
    return sum(map(lambda d: d['total_tokens'], TOKEN_COUNTER[call_id].values()))


def get_total_cost(call_id: str) -> float:
    return sum(map(lambda d: d['total_cost'], TOKEN_COUNTER[call_id].values()))


def get_token_details(call_id: str) -> dict:
    return {
        model_id: {
            'prompt_tokens': values['prompt_tokens'],
            'completion_tokens': values['completion_tokens']
        }
        for model_id, values in TOKEN_COUNTER[call_id].items()
    }


def _empty_metrics() -> dict[str, int | float]:
    return {
        'total_tokens': 0,
        'prompt_tokens': 0,
        'completion_tokens': 0,
        'successful_requests': 0,
        'total_cost': 0
    }


class ChatBedrockWrapper(ChatBedrock):
    call_id: str = Field(exclude=False)
    model_name: str = Field(exclude=False, default='AWS_Bedrock')
    model_id: str = Field(exclude=False)

    def invoke(
            self,
            input: LanguageModelInput,
            config: Optional[RunnableConfig] = None,
            *,
            stop: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> BaseMessage:
        messages = map(lambda m: m.content, self._convert_input(input).to_messages())
        messages = [{'content': message} for message in messages]
        self._update_token_counter_prompt(None, None, messages)
        ret = super().invoke(input, config, stop=stop, **kwargs)
        content = ret.content if isinstance(ret.content, str) else ''
        self._update_token_counter_completion(content)
        return ret

    def _prepare_input_and_invoke(
            self,
            prompt: Optional[str] = None,
            system: Optional[str] = None,
            messages: Optional[List[Dict]] = None,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Tuple[str, Dict[str, Any]]:
        self._update_token_counter_prompt(prompt, system, messages)
        text, metadata = super()._prepare_input_and_invoke(prompt, system, messages, stop, run_manager, **kwargs)
        self._update_token_counter_completion(text)
        return text, metadata

    def _prepare_input_and_invoke_stream(
            self,
            prompt: Optional[str] = None,
            system: Optional[str] = None,
            messages: Optional[List[Dict]] = None,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        self._update_token_counter_prompt(prompt, system, messages)
        stream = super()._prepare_input_and_invoke_stream(prompt, system, messages, stop, run_manager, **kwargs)

        def inner() -> Iterator[GenerationChunk]:
            for chunk in stream:
                self._update_token_counter_completion(chunk.text)
                yield chunk

        return inner()

    async def _aprepare_input_and_invoke_stream(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> AsyncIterator[GenerationChunk]:
        self._update_token_counter_prompt(prompt, None, None)
        stream = super()._aprepare_input_and_invoke_stream(prompt, stop, run_manager, **kwargs)

        async def inner() -> AsyncIterator[GenerationChunk]:
            async for chunk in stream:
                self._update_token_counter_completion(chunk.text)
                yield chunk

        return inner()

    def __get_tokens_count(self, prompt: Optional[str], system: Optional[str], messages: Optional[List[Dict]]) -> int:
        tokens = 0
        if prompt is not None:
            tokens += self.get_num_tokens(prompt)
        if system is not None:
            tokens += self.get_num_tokens(system)
        if messages:
            for message in messages:
                tokens += self.get_num_tokens(message['content'])
        return tokens

    def _update_token_counter_prompt(self, prompt, system, messages):
        tokens = self.__get_tokens_count(prompt, system, messages)
        if self.model_id not in TOKEN_COUNTER[self.call_id]:
            TOKEN_COUNTER[self.call_id][self.model_id] = _empty_metrics()
        TOKEN_COUNTER[self.call_id][self.model_id]['total_tokens'] += tokens
        TOKEN_COUNTER[self.call_id][self.model_id]['prompt_tokens'] += tokens
        TOKEN_COUNTER[self.call_id][self.model_id]['successful_requests'] += 1
        TOKEN_COUNTER[self.call_id][self.model_id]['total_cost'] += get_token_cost(
            tokens=tokens,
            model_id=self.model_id,
            mode='prompt'
        )

    def _update_token_counter_completion(self, text):
        tokens = self.get_num_tokens(text)
        if self.model_id not in TOKEN_COUNTER[self.call_id]:
            TOKEN_COUNTER[self.call_id][self.model_id] = _empty_metrics()
        TOKEN_COUNTER[self.call_id][self.model_id]['total_tokens'] += tokens
        TOKEN_COUNTER[self.call_id][self.model_id]['completion_tokens'] += tokens
        TOKEN_COUNTER[self.call_id][self.model_id]['total_cost'] += get_token_cost(
            tokens=tokens,
            model_id=self.model_id,
            mode='completion'
        )


def get_token_cost(tokens: int, model_id: str, mode: str) -> float:
    assert mode in ['prompt', 'completion', 'input', 'output'], f'mode "{mode}" is not supported'
    cost_mapping = {
        'anthropic.claude-3-5-sonnet-20240620-v1:0': {'input': 0.003, 'output': 0.015},
        'anthropic.claude-3-haiku-20240307-v1:0': {'input': 0.00025, 'output': 0.00125},
        'amazon.titan-text-premier-v1:0': {'input': 0.0005, 'output': 0.0015}
    }
    if mode == 'prompt':
        mode = 'input'
    elif mode == 'completion':
        mode = 'output'
    return tokens / 1000 * cost_mapping[model_id][mode]

