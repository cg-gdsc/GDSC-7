from src.submission.crews.basic_crew import DataAnalysisCrew
from src.submission.crews.advanced_crew import AdvancedDataAnalysisCrew
from src.static.ChatBedrockWrapper import compute_llm_call_cost, TOKEN_COUNTER
from src.static.ChatBedrockWrapper import ChatBedrockWrapper

import dotenv
assert dotenv.load_dotenv()

call_id = 0


call_id += 1
# Load LLM
#"""
llm_haiku = ChatBedrockWrapper(
    model_id='anthropic.claude-3-haiku-20240307-v1:0',
    model_kwargs={'temperature': 0.2},
    call_id=str(call_id)
)
# """

#"""
llm_sonnet = ChatBedrockWrapper(
    model_id='anthropic.claude-3-5-sonnet-20240620-v1:0',
    model_kwargs={'temperature': 0.2},
    call_id=str(call_id)
)
#"""

#crew = DataAnalysisCrew(llm_sonnet).crew()
crew = AdvancedDataAnalysisCrew(llm_haiku, llm_sonnet).crew()

# Replace with your inputs, it will automatically interpolate any tasks and agents information
inputs = {
    'user_question': """
"The code for Overall Reading Score is 'ASRREA_avg'. 
To achieve the lower benchmark students have to score at least 400 points. 
How many students (percentage) in the Germany met the minimum reading standards?"
    """
}

inputs = {
    'user_question': """    
"What is the schema of the PIRLS dataset?"
    """
}

crew.tasks = crew.tasks[:1]

assert len(crew.tasks) == 1

result = crew.kickoff(inputs=inputs)
compute_llm_call_cost(llm_haiku.model_id, call_id)
print(TOKEN_COUNTER['1'])
