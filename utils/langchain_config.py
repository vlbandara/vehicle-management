# # utils/langchain_config.py

# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import SystemMessage

# def initialize_language_model():
#     """
#     Initialize the OpenAI language model with appropriate settings.
#     """
#     return ChatOpenAI(
#         openai_api_key=os.getenv('OPENAI_API_KEY'),  # Ensure this is set in your .env file
#         model_name="gpt-3.5-turbo",                 # Cost-effective model choice
#         temperature=0.2,                             # Lower temperature for deterministic responses
#         max_tokens=1500                              # Adjust based on your needs
#     )

# def get_system_prompt():
#     """
#     Define the system prompt to guide the AI's behavior.
#     """
#     system_message = SystemMessage(
#         content="""
#         You are an expert in converting English instructions to SQL queries for a vehicle management system.
#         The SQLite database has the following tables:

#         1. Vehicles:
#            - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#            - make (TEXT NOT NULL)
#            - model (TEXT NOT NULL)
#            - year (INTEGER)
#            - license_plate (TEXT UNIQUE NOT NULL)

#         2. Expenses:
#            - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#            - vehicle_id (INTEGER)
#            - description (TEXT)
#            - amount (REAL)
#            - date (TEXT)
        
#         Please convert the following natural language instructions into valid SQL queries.
#         Do not include any markdown formatting or the word 'SQL' in your response.
#         Think step-by-step to ensure accuracy in the SQL query.
#         """
#     )
#     return system_message
