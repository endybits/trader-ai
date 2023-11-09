import asyncio
import os
from typing import Any

import sqlvalidator
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.schema import BaseOutputParser
from langchain.prompts import ChatPromptTemplate

from app.config.fconfig import get_openai_apikey as API_KEY
from app.utils.prompts import get_constrains_or_conditions
from app.utils.prompts import text2SQL_template, data_to_natural_language
from app.utils.table_description import get_target_table_description
from app.utils.db_utils import TARGET_TABLE

os.environ["OPENAI_API_KEY"] = API_KEY()

chat_model = ChatOpenAI()


## Get templates
target_table_description = get_target_table_description()
constraints = get_constrains_or_conditions()

base_template = text2SQL_template(TARGET_TABLE, target_table_description, constraints)

human_template = "{text}"

class SQLCommandOutputParser(BaseOutputParser):
    """Output parser for SQL command generation."""
    def parse(self, text: str) -> Any:
        global SQL_COMMAND
        SQL_COMMAND = text
        return super().parse(text)


## Get prompts
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", base_template),
        ("human", human_template),
    ]
)

## LLM Text to SQL
async def text2sql(user_id:str = "4359", question: str = None) -> str:
    await asyncio.sleep(0.1)
    chain = chat_prompt | chat_model | SQLCommandOutputParser()
    chain.invoke({"text": f"""I am the user id {user_id}. {question}"""})
    generated_sql_command = SQL_COMMAND
    try:
        validated = sqlvalidator.parse(generated_sql_command)
        if not validated.is_valid():
            return "Invalid SQL command"
        print("SQL command is valid")
    except ValueError:
        return "Invalid SQL command"
    return generated_sql_command



## LLM Data to Text
llm = OpenAI()
async def data2text(db_query: str = None, data: str = None, user_question: str = None) -> str:
    '''This function returns a string with the template prompt for transform the data to natural language'''
    await asyncio.sleep(0.1)
    ai_response = ''
    data_to_text_prompt = data_to_natural_language(db_query, data, user_question)
    for chunk in llm(data_to_text_prompt):
        ai_response += chunk

    return ai_response