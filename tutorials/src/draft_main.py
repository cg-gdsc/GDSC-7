import asyncio
import datetime as dt
import random

import dotenv
import uvicorn
from async_timeout import timeout
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.submission.create_submission import create_submission
from src.static.ChatBedrockWrapper import TOKEN_COUNTER

assert dotenv.load_dotenv()


# questions:
# why is database connection moved  to submission folder? Shouldn't it be static?
# why create_submission returns Crew from crewai? We need an abstraction
# kickoff method does not accept str. It requires inputs={'user_prompt': prompt}


class Payload(BaseModel):
    prompt: str
    timeout: int = 5*60  # 5 minutes


app = FastAPI()


@app.post("/run")
async def run_task(payload: Payload):
    call_id = dt.datetime.now().strftime("%Y%m%d%H%M%S%f") + f'_{random.randint(0, 1_000_000)}'
    TOKEN_COUNTER[call_id] = {
        'total_tokens': 0,
        'prompt_tokens': 0,
        'completion_tokens': 0,
        'successful_requests': 0,
    }

    try:
        submission = create_submission(call_id=call_id)

        async def run_submission(prompt: str):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: submission.kickoff(inputs={
                'user_question': prompt
            }))

        # can raise TimeoutError
        async with timeout(payload.timeout):
            start_time = asyncio.get_event_loop().time()
            result = await run_submission(payload.prompt)
            end_time = asyncio.get_event_loop().time()
            time_diff = end_time - start_time

        return JSONResponse(content={
            "result": result,
            "time": time_diff,
            "timed_out": False,
            'tokens': TOKEN_COUNTER[call_id]['total_tokens']
        })

    except asyncio.TimeoutError as e:
        return JSONResponse(content={
            "result": None,
            "time": None,
            "timed_out": True,
            'tokens': TOKEN_COUNTER[call_id]['total_tokens']
        })
    finally:
        del TOKEN_COUNTER[call_id]


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
