from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.static.submission import Submission
from src.static.util import PROJECT_ROOT
import src.submission.tools.database as db_tools


@CrewBase
class DataAnalysisCrew(Submission):
    """Data Analysis Crew for the GDSC project."""
    # Load the files from the config directory
    agents_config = PROJECT_ROOT / 'submission' / 'config' / 'agents.yaml'
    tasks_config = PROJECT_ROOT / 'submission' / 'config' / 'tasks.yaml'

    def __init__(self, llm):
        self.llm = llm

    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'user_question': prompt}).raw

    @agent
    def lead_data_analyst(self) -> Agent:
        a = Agent(
            config=self.agents_config['lead_data_analyst'],
            llm=self.llm,
            allow_delegation=True,
            verbose=True
        )
        return a

    @agent
    def data_engineer(self) -> Agent:
        a = Agent(
            config=self.agents_config['data_engineer'],
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            tools=[
                db_tools.query_database,
                db_tools.get_possible_answers_to_question,
                db_tools.get_questions_of_given_type
            ]
        )
        return a

    @task
    def answer_question_task(self) -> Task:
        t = Task(
            config=self.tasks_config['answer_question_task'],
            agent=self.lead_data_analyst()
        )
        return t

    @crew
    def crew(self) -> Crew:
        """Creates the data analyst crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_iter=5,
            cache=True
        )
