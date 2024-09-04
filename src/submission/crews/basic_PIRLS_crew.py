from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, task
from textwrap import dedent

from src.static.submission import Submission
from src.static.ChatBedrockWrapper import ChatBedrockWrapper
from src.submission.tools.database import query_database


class BasicPIRLSCrew(Submission):

    def __init__(self, llm: ChatBedrockWrapper):
        self.llm = llm

    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={"prompt": prompt}).raw

    @agent
    def database_expert(self) -> Agent:
        return Agent(
            role="PIRLS Student Database Expert",
            backstory=dedent("""
                You are a senior data engineer that has a lot of experience in working with the PIRLS data.
                Given a question, you come up with an SQL query that get the relevant data and run it with the'query_database' tool.

                You know that there is the table 'Students' with columns Student_ID and Country_ID, and a table 'Countries' with columns 'Country_ID', 'Name' and 'Code'.
            """),
            goal="Use the tool to query the database and answer the question.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            tools=[query_database]
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
            verbose=True,
            max_iter=3,
            cache=False
        )