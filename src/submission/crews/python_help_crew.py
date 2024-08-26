from crewai import Agent, Crew, Process, Task
from langchain_core.tools import tool
from crewai.project import agent, crew, task
from src.static.submission import Submission


class PythonHelpCrew(Submission):
    def __init__(self, llm):
        self.llm = llm
    
    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={"prompt": prompt})

    @agent
    def python_developer(self) -> Agent:
        return Agent(
            role="Python developer", 
            backstory="Experienced Python developer with deep knowledge in Python programming.", # We do a role assumption technique here
            goal="Write a Python code to solve the user's question.", # The simpler goal the better
            llm=self.llm,
            allow_delegation=False,
            verbose=True)
    
    @agent
    def tester(self) -> Agent:
        return Agent(
            role="Tester",
            backstory="Experienced tester with deep knowledge in testing and using provided tools.", # We do a role assumption technique here and order the agent to provided tool for testing.
            goal="Test the Python code to ensure it works correctly.", # The simpler goal the better
            llm=self.llm,
            allow_delegation=True, # Allow delegation to other agents (python developer), if code fails it will be sent back to the python developer to fix.
            tools = [eval_python_code], # Tools need to be passed in python list format, even if there is only one tool.
            verbose=True
        )

    
    @task
    def code_python_task(self) -> Task: 
        return Task(
            description="Write a python code to solve the user's question: {prompt}.", # We format task description with the user prompt passed in the run method.
            expected_output="Python code that solves the user's question. Python code only.", # We specify the expected output of the task. Note that we narrow down response distribution to python code only.
            agent=self.python_developer()) # Pass appropriate agent to the task.
    @task
    def test_code_task(self) -> Task:
        return Task(
            description="Test the python code to ensure it works correctly.",
            expected_output="Python code only or test results.",
            agent=self.tester()
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # List of agents participating in the crew. Each agent flagged with @agent decorator will be added here.
            tasks=self.tasks,  # List of tasks to be performed by the agents in the crew. Each task flagged with @task decorator will be added here.
            process=Process.sequential,  # Process type (sequential or hierarchical)
            verbose=2,  # Verbosity level
            max_iter=5,  # Maximum number of repetitions each agent can perform to get the generate the best answer.
            cache=False  # Caching option. Useful when tools produce large output like result of SQL queries.
        )
    

@tool
def eval_python_code(code: str) -> str:
    """
    Evaluate the given Python code and return the result.

    Parameters:
    code (str): The Python code to be executed.

    Returns:
    str: The result of executing the code. If the code executes successfully, it returns "Code executed successfully."
         If an exception occurs during execution, it returns the error message as a string.
    """
    # Remember each tool should have informative docstring. It will be used in the CrewAI platform to provide information about the tool.
    # We recommend generating it with GenAI tools such as Microsoft Copilot.
    try:
        exec(code)
        return "Code executed successfully."
    except Exception as e:
        return str(e)