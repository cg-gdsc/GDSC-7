import sqlalchemy
from textwrap import dedent
from crewai import Agent, Crew, Process, Task
from langchain_core.tools import tool
from crewai.project import agent, crew, task
from src.static.submission import Submission
from sqlalchemy import text, Engine
from langchain_aws import ChatBedrock


DB_ENDPOINT = "unesco-reader.crqaeg62obh7.us-east-1.rds.amazonaws.com"
DB_PASSWORD = "gdsc!!24--*part"
DB_USER = "gdsc_participant"
DB_PORT = 5432
DB_NAME = "postgres"

__connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}'
ENGINE = sqlalchemy.create_engine(__connection_string)


class StudentKnowingCrew(Submission):
    
    def __init__(self, llm: ChatBedrock):
        self.llm = llm
    
    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={"prompt": prompt})
    
    
    @agent
    def database_expert(self) -> Agent:
        return Agent(
            role="Students database expert",
            backstory=dedent("""
                Database expert that knows the structure of PIRLS database regarding students.
                You know that there is the table Students with columns Stident_ID and Country_ID, and a table
                Countries with column Country_ID, Name and Code.
            """),
            goal="Use the tool to query the database and answer the question.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            tools=[
                query_database
            ]
        )
    
    @task
    def answer_question(self) -> Task:
        return Task(
            description="Query the database and answer the question \"{prompt}\".",
            expected_output="Answer to the queston",
            agent=self.database_expert()
        )

   
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
            max_iter=5,
            cache=False
        )
    
@tool
def query_database(query: str) -> str:
    """Query the PIRLS postgres database and return the results as a string.

    Args:
        query (str): The SQL query to execute.

    Returns:
        str: The results of the query as a string, where each row is separated by a newline.
    """
    
    with ENGINE.connect() as connection:
        try:
            res = connection.execute(text(query))
        except Exception as e:
            return f'Encountered exception {e}.'

    ret = '\n'.join(", ".join(map(str, result)) for result in res)

    return f'Query: {query}\nResult: {ret}'
