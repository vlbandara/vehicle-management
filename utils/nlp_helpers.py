# # utils/nlp_helpers.py

# import json
# from langchain.schema import HumanMessage
# from langchain.memory import ConversationBufferMemory
# from utils.langchain_config import initialize_language_model, get_system_prompt

# # Initialize the language model
# language_model = initialize_language_model()

# # Initialize memory for conversational context
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# def generate_sql_query(instruction):
#     """
#     Generate an SQL query from a natural language instruction using LangChain.
#     Maintains conversational context to handle complex and multi-step instructions.
#     """
#     system_message = get_system_prompt()
    
#     # Retrieve chat history from memory
#     messages = [system_message] + memory.load_memory_variables({})
    
#     # Add the new user instruction
#     messages.append(HumanMessage(content=instruction))
    
#     # Generate the response from the language model
#     response = language_model(messages)
    
#     # Update memory with the new interaction
#     memory.save_context({"input": instruction}, {"output": response.content})
    
#     # Handle potential errors in the response
#     sql_query = handle_nlp_errors(response.content)
    
#     return sql_query

# def handle_nlp_errors(response_text):
#     """
#     Detect and handle errors in the AI-generated SQL query.
#     Provides meaningful suggestions to the user when the instruction is unclear or problematic.
#     """
#     error_keywords = {
#         'syntax error': "There seems to be a syntax error in the SQL query. Please check your instruction and try again.",
#         'invalid column': "It looks like there's an issue with the column names. Please ensure you're using valid field names.",
#         'missing value': "Some values seem to be missing in your instruction. Please provide all necessary details.",
#         'no such table': "The table you're referring to does not exist. Please check the table name and try again.",
#         # Add more specific error detections as needed
#     }
    
#     for keyword, suggestion in error_keywords.items():
#         if keyword in response_text.lower():
#             return suggestion
    
#     # General error handling for ambiguous or unclear instructions
#     general_errors = ['error', 'unable', 'cannot', 'invalid', 'unclear', 'fail']
#     if any(keyword in response_text.lower() for keyword in general_errors):
#         return "I'm sorry, I couldn't understand your instruction. Could you please rephrase it or provide more details?"
    
#     return response_text.strip()
