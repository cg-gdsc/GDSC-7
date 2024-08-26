from langchain_core.tools import tool
from sqlalchemy import text
from src.static.util import ENGINE
from typing import Literal


@tool
def query_database(query: str) -> str:
    """Query the PIRLS postgres database and return the results as a string.

    Args:
        query (str): The SQL query to execute.

    Returns:
        str: The results of the query as a string, where each row is separated by a newline.

    Raises:
        Exception: If the query is invalid or encounters an exception during execution.
    """
    # lower_query = query.lower()
    # record_limiters = ['count', 'where', 'limit', 'distinct', 'having', 'group by']
    # if not any(word in lower_query for word in record_limiters):
    #     return 'WARNING! The query you are about to perform has no record limitations! In case of large tables and ' \
    #            'joins this will return an incomprehensible output.'

    with ENGINE.connect() as connection:
        try:
            res = connection.execute(text(query))
        except Exception as e:
            return f'Wrong query, encountered exception {e}.'

    max_result_len = 3_000
    ret = '\n'.join(", ".join(map(str, result)) for result in res)
    if len(ret) > max_result_len:
        ret = ret[:max_result_len] + '...\n(results too long. Output truncated.)'

    return f'Query: {query}\nResult: {ret}'


@tool
def get_possible_answers_to_question(
        general_table: Literal['Students', 'Curricula', 'Homes', 'Teachers', 'Schools'],
        questionnaire_answers_table: Literal['StudentQuestionnaireAnswers', 'CurriculumQuestionnaireAnswers', 'HomeQuestionnaireAnswers', 'TeacherQuestionnaireAnswers', 'SchoolQuestionnaireAnswers'],
        questionnaire_entries_table: Literal['StudentQuestionnaireEntries', 'CurriculumQuestionnaireEntries', 'HomeQuestionnaireEntries', 'TeacherQuestionnaireEntries', 'SchoolQuestionnaireEntries'],
        question_code: str
) -> str:
    """Query the database and returns possible answer to a given question

    Args:
        general_table (str): the generic table related to the question topic. Can be one of: 'Students', 'Curricula', 'Homes', 'Teachers', 'Schools'
        questionnaire_answers_table (str): the table related to the `general_table` containing answers.
        questionnaire_entries_table (str): the table related to the `general_table` containing all possible questions.
        question_code (str): the code of the question the full list of possible answers to is returned.

    Returns:
        str: The list of all possible answers to the question with the code given in `question_code`.
    """
    entity_id = 'curriculum_id' if general_table.lower() == 'curricula' else f'{general_table.lower()[:-1]}_id'
    query = f"""
        SELECT DISTINCT ATab.Answer
        FROM {general_table} AS GTab
        JOIN {questionnaire_answers_table} AS ATab ON ATab.{entity_id} = GTab.{entity_id}
        JOIN {questionnaire_entries_table} AS ETab ON ETab.Code = ATab.Code
        WHERE ETab.Code = '{question_code.replace("'", "").replace('"', '')}'
    """

    with ENGINE.connect() as connection:
        try:
            res = connection.execute(text(query))
        except Exception as e:
            return f'Wrong query, encountered exception {e}.'

    ret = ""
    for result in res:
        ret += ", ".join(map(str, result)) + "\n"

    return ret


@tool
def get_questions_of_given_type(
    general_table: Literal['Students', 'Curricula', 'Homes', 'Teachers', 'Schools'],
    questionnaire_answers_table: Literal['StudentQuestionnaireAnswers', 'CurriculumQuestionnaireAnswers', 'HomeQuestionnaireAnswers', 'TeacherQuestionnaireAnswers', 'SchoolQuestionnaireAnswers'],
    questionnaire_entries_table: Literal['StudentQuestionnaireEntries', 'CurriculumQuestionnaireEntries', 'HomeQuestionnaireEntries', 'TeacherQuestionnaireEntries', 'SchoolQuestionnaireEntries'],
    question_type: str
) -> str:
    """Query the database and returns questions of a given type with their codes.

        Args:
            general_table (str): the generic table related to the question topic. Can be one of: 'Students', 'Curricula', 'Homes', 'Teachers', 'Schools'
            questionnaire_answers_table (str): the table related to the `general_table` containing answers.
            questionnaire_entries_table (str): the table related to the `general_table` containing all possible questions.
            question_type (str): the type of the question group.

        Returns:
            str: The list of all questions of type specified by `question_type`
        """
    entity_id = 'curriculum_id' if general_table.lower() == 'curricula' else f'{general_table.lower()[:-1]}_id'
    query = f"""
        SELECT DISTINCT ETab.Question, ETab.Code
        FROM {general_table} AS GTab
        JOIN {questionnaire_answers_table} AS ATab ON ATab.{entity_id} = GTab.{entity_id}
        JOIN {questionnaire_entries_table} AS ETab ON ETab.Code = ATab.Code
        WHERE ETab.Type = '{question_type.replace("'", "").replace('"', '')}'
    """

    with ENGINE.connect() as connection:
        try:
            res = connection.execute(text(query))
        except Exception as e:
            return f'Wrong query, encountered exception {e}.'

    questions = []
    for question, code in res:
        questions.append(f'(Code: {code}) {question}\n')
    return ''.join(questions)
