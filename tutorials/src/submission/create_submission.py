import dotenv

import sqlalchemy

# from src.submission.crews.basic_crew import DataAnalysisCrew
# from src.submission.crews.python_help_crew import PythonHelpCrew
# from src.submission.crews.sceleton_crew import SceletonCrew
from src.submission.crews.student_knowing_crew import StudentKnowingCrew
from src.static.ChatBedrockWrapper import ChatBedrockWrapper
from src.static.submission import Submission

dotenv.load_dotenv()


# This function is used to run evaluation of your model.
# You MUST NOT change the signature of this function! The name of the function, name of the arguments,
# number of the arguments and the returned type mustn't be changed.
# You can modify only the body of this function so that it returned your implementation of the Submission class.
def create_submission(call_id: str) -> Submission:
    llm = ChatBedrockWrapper(
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        model_kwargs={'temperature': 0},
        call_id=call_id
    )
    
    crew = StudentKnowingCrew(llm)
    return crew

