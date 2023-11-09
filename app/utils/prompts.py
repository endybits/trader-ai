
def get_constrains_or_conditions():
    '''This function returns a string with the conditions or constraints that the user must to apply to the SQL query'''

    return f""" For each query you must to filtrate the results using the condition WHERE is_trade=1"""


## TEXT TO SQL TEMPLATE PROMPT
def text2SQL_template(target_table, target_table_description_fields, contraints):
    '''This function returns a string with the template prompt for the text to SQL task'''
    # output_format = """{"sql_query": "SELECT...", "column_list": ["field1", "field2",]}"""
    return f"""You are a SQL expert assistant who generates SQL Query commands based on text.
                    A user will pass in a question and you should convert it in a SQL command 
                    to query against the table {target_table} in a MariaDB database.
                    Use this fields description of the table, for a more accurate results: {target_table_description_fields}
                    Also, apply this constraint: {contraints}
                    ONLY return the valid SQL QUERY and nothing more."""
