from crewai import Agent, Crew, Process, Task
from langchain_core.tools import tool
import random

from src.static.submission import Submission


class SkeletonCrew(Submission):
    def run(self, prompt: str) -> str:
        return self.crew.kickoff(inputs={'user_question': prompt}).raw

    def __init__(self, llm):
        self.llm = llm
        agent = Agent(
            role='A capitan of the Pirate ship named The Lost Marbles',
            goal='Be as piratey as possible',
            backstory='You are a capitan of a famous ship called The Lost Marbles. You\'r goal is to make funny comments',
            verbose=True,
            llm=self.llm,
            tools=[self.generate_random_number],
            allow_delegation=False
        )
        task = Task(
            description='Based on your see adventures answer this question {user_question}',
            expected_output='A funny story in a pirate manner',
            agent=agent
        )

        self.crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=2,
            max_iter=5,
            cache=True
        )

    @staticmethod
    @tool
    def generate_random_number() -> int:
        """
        A function that generates a random number from 1 to 100.
        """
        return random.randint(1, 100)
