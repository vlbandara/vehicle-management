# # app.py

# from dotenv import load_dotenv
# import streamlit as st
# import os
# import sqlite3
# import re
# import json
# import pandas as pd
# from utils.nlp_helpers import generate_sql_query, handle_nlp_errors

# # Load environment variables
# load_dotenv()

# # [Optional] If you still intend to use Google Gemini, retain the configuration
# # import google.generativeai as genai
# # genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # Function to execute SQL queries
# def execute_sql_query(sql, db='db/vehicle_management.db'):
#     # Basic validation to prevent dangerous operations
#     prohibited_commands = ['DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
#     sql_upper = sql.strip().upper()
#     for cmd in prohibited_commands:
#         if sql_upper.startswith(cmd):
#             return ("ERROR", f"Operation '{cmd}' is not permitted.")
    
#     conn = sqlite3.connect(db)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql)
#         # Determine the type of query
#         query_type = sql_upper.split()[0]
#         if query_type == "SELECT":
#             rows = cursor.fetchall()
#             return ("SELECT", rows)
#         else:
#             conn.commit()
#             return (query_type, "Query executed successfully.")
#     except sqlite3.Error as e:
#         return ("ERROR", f"An error occurred: {e}")
#     finally:
#         conn.close()

# # Function to clean and validate SQL response (Retained for backward compatibility)
# def clean_sql(sql_response):
#     # Remove code blocks and the word 'SQL' if present
#     sql_response = re.sub(r'```sql\s*', '', sql_response)
#     sql_response = re.sub(r'```', '', sql_response)
#     sql_response = re.sub(r'\bsql\b', '', sql_response, flags=re.IGNORECASE)
#     return sql_response.strip()

# # Define your Prompt with data manipulation examples
# query_prompt = """
# You are an expert in converting English instructions to SQL queries for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Please convert the following natural language instructions into valid SQL queries.
# Do not include any markdown formatting or the word 'SQL' in your response.

# Here are some examples:

# Example 1:
# Instruction: Show me all vehicles from 2020.
# SQL Query: SELECT * FROM Vehicles WHERE year = 2020;

# Example 2:
# Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
# SQL Query: INSERT INTO Vehicles (make, model, year, license_plate) VALUES ('Toyota', 'Corolla', 2022, 'ABC123');

# Example 3:
# Instruction: Update the license plate of the vehicle with ID 3 to XYZ789.
# SQL Query: UPDATE Vehicles SET license_plate = 'XYZ789' WHERE id = 3;

# Example 4:
# Instruction: Delete the expense with ID 5.
# SQL Query: DELETE FROM Expenses WHERE id = 5;

# Now, convert the following instruction into an SQL query:
# """

# # Define your Prompt for Form Data Extraction
# form_prompt = """
# You are an expert in extracting structured data from natural language instructions for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Extract the relevant fields from the following instruction and present them in JSON format with the appropriate keys.

# Here are some examples:

# Example 1:
# Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
# Extracted Data: {"make": "Toyota", "model": "Corolla", "year": 2022, "license_plate": "ABC123"}

# Example 2:
# Instruction: Add an expense for vehicle ID 3 with description "Oil Change", amount 75.50, and date 2024-04-15.
# Extracted Data: {"vehicle_id": 3, "description": "Oil Change", "amount": 75.50, "date": "2024-04-15"}

# Now, extract the data from the following instruction:
# Instruction:
# """

# # Streamlit App Configuration
# st.set_page_config(page_title="Vehicle Management App", layout="wide")
# st.header("🚗 Vehicle Management System with Conversational UI")

# # Initialize session state for chat history and form fields
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# form_fields = {
#     "make": "",
#     "model": "",
#     "year": "",
#     "license_plate": "",
#     "vehicle_id": "",
#     "description": "",
#     "amount": "",
#     "date": ""
# }

# for key in form_fields:
#     if f'form_{key}' not in st.session_state:
#         st.session_state[f'form_{key}'] = ""

# # User Input for Conversational UI
# instruction = st.text_input("Enter your command:", key="input")

# submit = st.button("Execute")

# if submit and instruction:
#     with st.spinner("Processing your instruction..."):
#         # Generate SQL query using LangChain
#         sql_response = generate_sql_query(instruction)
        
#         # Update chat history with user and assistant messages
#         st.session_state['chat_history'].append({"role": "user", "content": instruction})
#         st.session_state['chat_history'].append({"role": "assistant", "content": sql_response})
    
#     st.subheader("Conversation History:")
#     for message in st.session_state['chat_history']:
#         if message['role'] == 'user':
#             st.markdown(f"**You:** {message['content']}")
#         else:
#             st.markdown(f"**App:** {message['content']}")
    
#     st.subheader("Generated SQL Query:")
#     st.code(sql_response, language='sql')
    
#     # Detect if the query is potentially destructive
#     destructive_commands = ['DELETE', 'DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
#     query_type = sql_response.strip().split()[0].upper()
    
#     if query_type in destructive_commands:
#         confirm = st.checkbox("⚠️ Are you sure you want to execute this operation?")
#         if confirm:
#             with st.spinner("Executing SQL query..."):
#                 result_type, result = execute_sql_query(sql_response)
            
#             st.subheader("Execution Result:")
#             if result_type == "SELECT":
#                 if result:
#                     # Fetch column names for better table display
#                     conn = sqlite3.connect('db/vehicle_management.db')
#                     cursor = conn.cursor()
#                     cursor.execute(sql_response)
#                     columns = [description[0] for description in cursor.description]
#                     conn.close()
#                     # Convert result to list of dicts for better display
#                     data = [dict(zip(columns, row)) for row in result]
#                     st.table(data)
#                 else:
#                     st.write("No records found.")
#             elif result_type in destructive_commands:
#                 st.success(result)
#             else:
#                 st.error(result)
#         else:
#             st.info("Operation cancelled.")
#     else:
#         # Non-destructive queries
#         with st.spinner("Executing SQL query..."):
#             result_type, result = execute_sql_query(sql_response)
        
#         st.subheader("Execution Result:")
#         if result_type == "SELECT":
#             if result:
#                 # Fetch column names for better table display
#                 conn = sqlite3.connect('db/vehicle_management.db')
#                 cursor = conn.cursor()
#                 cursor.execute(sql_response)
#                 columns = [description[0] for description in cursor.description]
#                 conn.close()
#                 # Convert result to list of dicts for better display
#                 data = [dict(zip(columns, row)) for row in result]
#                 st.table(data)
#             else:
#                 st.write("No records found.")
#         elif result_type in destructive_commands:
#             st.success(result)
#         else:
#             st.success(result)

# # ------------------------------
# # Natural Language Form Filling Section
# # ------------------------------
# st.markdown("---")
# st.subheader("📝 Fill Forms Using Natural Language")

# # Natural Language Input
# nl_instruction = st.text_input("Enter your instruction to fill the form:", key="nl_input")

# # Button to parse instruction
# parse_button = st.button("Parse Instruction")

# if parse_button and nl_instruction:
#     with st.spinner("Parsing instruction..."):
#         extracted_data = generate_sql_query(nl_instruction)  # Reusing generate_sql_query for form data extraction
#         try:
#             # Attempt to parse the response as JSON
#             data = json.loads(extracted_data)
#             st.success("Instruction parsed successfully!")
#             st.json(data)  # Display the extracted data
            
#             # Populate session state with extracted data
#             for key, value in data.items():
#                 st.session_state[f'form_{key}'] = value
#         except json.JSONDecodeError:
#             st.error("Failed to parse the instruction. Please ensure it's clear and follows the examples.")

# # ------------------------------
# # Sidebar Forms for Manual Data Entry
# # ------------------------------
# st.sidebar.header("Add Data")

# # Add Vehicle Form
# with st.sidebar.form("add_vehicle"):
#     st.subheader("Add a New Vehicle")
#     make = st.text_input("Make", value=st.session_state.get('form_make', ''))
#     model = st.text_input("Model", value=st.session_state.get('form_model', ''))
#     year_input = st.text_input("Year", value=st.session_state.get('form_year', ''))
#     # Convert year to integer if possible
#     try:
#         year = int(year_input)
#     except ValueError:
#         year = 2000  # Default value or handle accordingly
#     license_plate = st.text_input("License Plate", value=st.session_state.get('form_license_plate', ''))
#     submitted_vehicle = st.form_submit_button("Add Vehicle")
    
#     if submitted_vehicle:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Vehicles (make, model, year, license_plate)
#                 VALUES (?, ?, ?, ?)
#             ''', (make, model, year, license_plate))
#             conn.commit()
#             st.success("Vehicle added successfully.")
            
#             # Clear form fields in session state after successful submission
#             for key in ['make', 'model', 'year', 'license_plate']:
#                 st.session_state[f'form_{key}'] = ""
#         except sqlite3.IntegrityError:
#             st.error("License plate already exists.")
#         finally:
#             conn.close()

# # Add Expense Form
# with st.sidebar.form("add_expense"):
#     st.subheader("Add a New Expense")
#     vehicle_id_input = st.text_input("Vehicle ID", value=st.session_state.get('form_vehicle_id', ''))
#     # Convert vehicle_id to integer if possible
#     try:
#         vehicle_id = int(vehicle_id_input)
#     except ValueError:
#         vehicle_id = 1  # Default value or handle accordingly
#     description = st.text_input("Description", value=st.session_state.get('form_description', ''))
#     amount_input = st.text_input("Amount", value=str(st.session_state.get('form_amount', '0.0')))
#     # Convert amount to float if possible
#     try:
#         amount = float(amount_input)
#     except ValueError:
#         amount = 0.0
#     date_input = st.text_input("Date (YYYY-MM-DD)", value=str(st.session_state.get('form_date', '2024-01-01')))
#     try:
#         date = pd.to_datetime(date_input).date()
#     except:
#         date = pd.to_datetime('2024-01-01').date()
#     submitted_expense = st.form_submit_button("Add Expense")
    
#     if submitted_expense:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Expenses (vehicle_id, description, amount, date)
#                 VALUES (?, ?, ?, ?)
#             ''', (vehicle_id, description, amount, date))
#             conn.commit()
#             st.success("Expense added successfully.")
            
#             # Clear form fields in session state after successful submission
#             for key in ['vehicle_id', 'description', 'amount', 'date']:
#                 st.session_state[f'form_{key}'] = ""
#         except sqlite3.Error as e:
#             st.error(f"An error occurred: {e}")
#         finally:
#             conn.close()







# app.py
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re
import json
from ast import literal_eval
import pandas as pd  # Needed for date handling

# Load environment variables
load_dotenv()

# Configure Google Gemini API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to generate SQL query using Gemini
def get_gemini_response(instruction, prompt):
    model = genai.GenerativeModel('gemini-pro')  # Ensure 'gemini-pro' is the correct model name
    full_prompt = prompt + instruction
    response = model.generate_content([full_prompt])
    return response.text

# Function to execute SQL queries
def execute_sql_query(sql, db='db/vehicle_management.db'):
    # Basic validation to prevent dangerous operations
    prohibited_commands = ['DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
    sql_upper = sql.strip().upper()
    for cmd in prohibited_commands:
        if sql_upper.startswith(cmd):
            return ("ERROR", f"Operation '{cmd}' is not permitted.")
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        # Determine the type of query
        query_type = sql_upper.split()[0]
        if query_type == "SELECT":
            rows = cursor.fetchall()
            return ("SELECT", rows)
        else:
            conn.commit()
            return (query_type, "Query executed successfully.")
    except sqlite3.Error as e:
        return ("ERROR", f"An error occurred: {e}")
    finally:
        conn.close()

# Function to clean and validate SQL response
def clean_sql(sql_response):
    # Remove code blocks and the word 'SQL' if present
    sql_response = re.sub(r'```', '', sql_response)
    sql_response = re.sub(r'\bsql\b', '', sql_response, flags=re.IGNORECASE)
    return sql_response.strip()

# Function to extract form data using Gemini
def extract_form_data(instruction, prompt):
    model = genai.GenerativeModel('gemini-pro')  # Ensure the model name is correct
    full_prompt = prompt + instruction
    response = model.generate_content([full_prompt])
    return response.text

# Define your Prompt with data manipulation examples
query_prompt = """
You are an expert in converting English instructions to SQL queries for a vehicle management system.
The SQLite database has the following tables:

1. Vehicles:
   - id (INTEGER PRIMARY KEY AUTOINCREMENT)
   - make (TEXT NOT NULL)
   - model (TEXT NOT NULL)
   - year (INTEGER)
   - license_plate (TEXT UNIQUE NOT NULL)

2. Expenses:
   - id (INTEGER PRIMARY KEY AUTOINCREMENT)
   - vehicle_id (INTEGER)
   - description (TEXT)
   - amount (REAL)
   - date (TEXT)
   
Please convert the following natural language instructions into valid SQL queries.
Do not include any markdown formatting or the word 'SQL' in your response.

Here are some examples:

Example 1:
Instruction: Show me all vehicles from 2020.
SQL Query: SELECT * FROM Vehicles WHERE year = 2020;

Example 2:
Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
SQL Query: INSERT INTO Vehicles (make, model, year, license_plate) VALUES ('Toyota', 'Corolla', 2022, 'ABC123');

Example 3:
Instruction: Update the license plate of the vehicle with ID 3 to XYZ789.
SQL Query: UPDATE Vehicles SET license_plate = 'XYZ789' WHERE id = 3;

Example 4:
Instruction: Delete the expense with ID 5.
SQL Query: DELETE FROM Expenses WHERE id = 5;

Now, convert the following instruction into an SQL query:
"""

# Define your Prompt for Form Data Extraction
form_prompt = """
You are an expert in extracting structured data from natural language instructions for a vehicle management system.
The SQLite database has the following tables:

1. Vehicles:
   - id (INTEGER PRIMARY KEY AUTOINCREMENT)
   - make (TEXT NOT NULL)
   - model (TEXT NOT NULL)
   - year (INTEGER)
   - license_plate (TEXT UNIQUE NOT NULL)

2. Expenses:
   - id (INTEGER PRIMARY KEY AUTOINCREMENT)
   - vehicle_id (INTEGER)
   - description (TEXT)
   - amount (REAL)
   - date (TEXT)
   
Extract the relevant fields from the following instruction and present them in JSON format with the appropriate keys.

Here are some examples:

Example 1:
Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
Extracted Data: {"make": "Toyota", "model": "Corolla", "year": 2022, "license_plate": "ABC123"}

Example 2:
Instruction: Add an expense for vehicle ID 3 with description "Oil Change", amount 75.50, and date 2024-04-15.
Extracted Data: {"vehicle_id": 3, "description": "Oil Change", "amount": 75.50, "date": "2024-04-15"}

Now, extract the data from the following instruction:
Instruction:
"""

# Streamlit App Configuration
st.set_page_config(page_title="Vehicle Management App", layout="wide")
st.header("🚗 Vehicle Management System with Conversational UI")

# Initialize session state for form fields
form_fields = {
    "make": "",
    "model": "",
    "year": "",
    "license_plate": "",
    "vehicle_id": "",
    "description": "",
    "amount": "",
    "date": ""
}

for key in form_fields:
    if f'form_{key}' not in st.session_state:
        st.session_state[f'form_{key}'] = ""

# User Input for Conversational UI
instruction = st.text_input("Enter your command:", key="input")

submit = st.button("Execute")

if submit and instruction:
    with st.spinner("Generating SQL query..."):
        sql_response = get_gemini_response(instruction, query_prompt)
        sql_query = clean_sql(sql_response)
    
    st.subheader("Generated SQL Query:")
    st.code(sql_query, language='sql')
    
    # Detect if the query is potentially destructive
    destructive_commands = ['DELETE']
    query_type = sql_query.strip().split()[0].upper()
    
    if query_type in destructive_commands:
        confirm = st.checkbox("⚠️ Are you sure you want to execute this operation?")
        if confirm:
            with st.spinner("Executing SQL query..."):
                result_type, result = execute_sql_query(sql_query)
            
            st.subheader("Execution Result:")
            if result_type == "SELECT":
                if result:
                    # Fetch column names for better table display
                    conn = sqlite3.connect('db/vehicle_management.db')
                    cursor = conn.cursor()
                    cursor.execute(sql_query)
                    columns = [description[0] for description in cursor.description]
                    conn.close()
                    # Convert result to list of dicts for better display
                    data = [dict(zip(columns, row)) for row in result]
                    st.table(data)
                else:
                    st.write("No records found.")
            elif result_type in destructive_commands:
                st.success(result)
            else:
                st.error(result)
        else:
            st.info("Operation cancelled.")
    else:
        # Non-destructive queries
        with st.spinner("Executing SQL query..."):
            result_type, result = execute_sql_query(sql_query)
        
        st.subheader("Execution Result:")
        if result_type == "SELECT":
            if result:
                # Fetch column names for better table display
                conn = sqlite3.connect('db/vehicle_management.db')
                cursor = conn.cursor()
                cursor.execute(sql_query)
                columns = [description[0] for description in cursor.description]
                conn.close()
                # Convert result to list of dicts for better display
                data = [dict(zip(columns, row)) for row in result]
                st.table(data)
            else:
                st.write("No records found.")
        elif result_type in destructive_commands:
            st.success(result)
        else:
            st.success(result)

# ------------------------------
# Natural Language Form Filling Section
# ------------------------------
st.markdown("---")
st.subheader("📝 Fill Forms Using Natural Language")

# Natural Language Input
nl_instruction = st.text_input("Enter your instruction to fill the form:", key="nl_input")

# Button to parse instruction
parse_button = st.button("Parse Instruction")

if parse_button and nl_instruction:
    with st.spinner("Parsing instruction..."):
        extracted_data = extract_form_data(nl_instruction, form_prompt)
        try:
            data = json.loads(extracted_data)
            st.success("Instruction parsed successfully!")
            st.json(data)  # Display the extracted data
            
            # Populate session state
            for key, value in data.items():
                st.session_state[f'form_{key}'] = value
        except json.JSONDecodeError:
            st.error("Failed to parse the instruction. Please ensure it's clear and follows the examples.")

# ------------------------------
# Sidebar Forms for Manual Data Entry
# ------------------------------
st.sidebar.header("Add Data")

# Add Vehicle Form
with st.sidebar.form("add_vehicle"):
    st.subheader("Add a New Vehicle")
    make = st.text_input("Make", value=st.session_state.get('form_make', ''))
    model = st.text_input("Model", value=st.session_state.get('form_model', ''))
    year_input = st.text_input("Year", value=st.session_state.get('form_year', ''))
    # Convert year to integer if possible
    try:
        year = int(year_input)
    except ValueError:
        year = 2000  # Default value or handle accordingly
    license_plate = st.text_input("License Plate", value=st.session_state.get('form_license_plate', ''))
    submitted_vehicle = st.form_submit_button("Add Vehicle")
    
    if submitted_vehicle:
        conn = sqlite3.connect('db/vehicle_management.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Vehicles (make, model, year, license_plate)
                VALUES (?, ?, ?, ?)
            ''', (make, model, year, license_plate))
            conn.commit()
            st.success("Vehicle added successfully.")
            
            # Clear form fields in session state after successful submission
            for key in ['make', 'model', 'year', 'license_plate']:
                st.session_state[f'form_{key}'] = ""
        except sqlite3.IntegrityError:
            st.error("License plate already exists.")
        finally:
            conn.close()

# Add Expense Form
with st.sidebar.form("add_expense"):
    st.subheader("Add a New Expense")
    vehicle_id_input = st.text_input("Vehicle ID", value=st.session_state.get('form_vehicle_id', ''))
    # Convert vehicle_id to integer if possible
    try:
        vehicle_id = int(vehicle_id_input)
    except ValueError:
        vehicle_id = 1  # Default value or handle accordingly
    description = st.text_input("Description", value=st.session_state.get('form_description', ''))
    amount_input = st.text_input("Amount", value=str(st.session_state.get('form_amount', '0.0')))
    # Convert amount to float if possible
    try:
        amount = float(amount_input)
    except ValueError:
        amount = 0.0
    date_input = st.text_input("Date (YYYY-MM-DD)", value=str(st.session_state.get('form_date', '2024-01-01')))
    try:
        date = pd.to_datetime(date_input).date()
    except:
        date = pd.to_datetime('2024-01-01').date()
    submitted_expense = st.form_submit_button("Add Expense")
    
    if submitted_expense:
        conn = sqlite3.connect('db/vehicle_management.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Expenses (vehicle_id, description, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (vehicle_id, description, amount, date))
            conn.commit()
            st.success("Expense added successfully.")
            
            # Clear form fields in session state after successful submission
            for key in ['vehicle_id', 'description', 'amount', 'date']:
                st.session_state[f'form_{key}'] = ""
        except sqlite3.Error as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()









# # app.py
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai
# import re

# # Load environment variables
# load_dotenv()

# # Configure Google Gemini API Key
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # Function to generate SQL query using Gemini
# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')  # Ensure 'gemini-pro' is the correct model name
#     response = model.generate_content([prompt + question])
#     return response.text

# # Function to execute SQL queries
# def execute_sql_query(sql, db='db/vehicle_management.db'):
#     conn = sqlite3.connect(db)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql)
#         # If it's a SELECT query, fetch results
#         if sql.strip().upper().startswith("SELECT"):
#             rows = cursor.fetchall()
#             return rows
#         else:
#             conn.commit()
#             return "Query executed successfully."
#     except sqlite3.Error as e:
#         return f"An error occurred: {e}"
#     finally:
#         conn.close()

# # Function to clean and validate SQL response
# def clean_sql(sql_response):
#     # Remove code blocks and SQL word if present
#     sql_response = re.sub(r'```', '', sql_response)
#     sql_response = re.sub(r'\bsql\b', '', sql_response, flags=re.IGNORECASE)
#     return sql_response.strip()

# # Define your Prompt
# prompt = """
# You are an expert in converting English instructions to SQL queries for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Please convert the following natural language instructions into valid SQL queries.
# Do not include any markdown formatting or the word 'SQL' in your response.
# """

# # Streamlit App Configuration
# st.set_page_config(page_title="Vehicle Management App", layout="wide")
# st.header("🚗 Vehicle Management System with Conversational UI")

# # User Input
# question = st.text_input("Ask a question about vehicle management:", key="input")

# submit = st.button("Ask")

# if submit and question:
#     with st.spinner("Generating SQL query..."):
#         sql_response = get_gemini_response(question, prompt)
#         sql_query = clean_sql(sql_response)
    
#     st.subheader("Generated SQL Query:")
#     st.code(sql_query, language='sql')
    
#     # Execute the SQL query
#     with st.spinner("Executing SQL query..."):
#         result = execute_sql_query(sql_query)
    
#     st.subheader("Query Result:")
#     if isinstance(result, list):
#         if result:
#             # Display results in a table
#             st.table(result)
#         else:
#             st.write("No records found.")
#     else:
#         st.write(result)

# # Optional: Add manual forms for adding vehicles and expenses

# st.sidebar.header("Add Data")

# # Add Vehicle Form
# with st.sidebar.form("add_vehicle"):
#     st.subheader("Add a New Vehicle")
#     make = st.text_input("Make")
#     model = st.text_input("Model")
#     year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
#     license_plate = st.text_input("License Plate")
#     submitted_vehicle = st.form_submit_button("Add Vehicle")
    
#     if submitted_vehicle:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Vehicles (make, model, year, license_plate)
#                 VALUES (?, ?, ?, ?)
#             ''', (make, model, year, license_plate))
#             conn.commit()
#             st.success("Vehicle added successfully.")
#         except sqlite3.IntegrityError:
#             st.error("License plate already exists.")
#         finally:
#             conn.close()

# # Add Expense Form
# with st.sidebar.form("add_expense"):
#     st.subheader("Add a New Expense")
#     vehicle_id = st.number_input("Vehicle ID", min_value=1, step=1)
#     description = st.text_input("Description")
#     amount = st.number_input("Amount", min_value=0.0, step=0.1)
#     date = st.date_input("Date")
#     submitted_expense = st.form_submit_button("Add Expense")
    
#     if submitted_expense:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Expenses (vehicle_id, description, amount, date)
#                 VALUES (?, ?, ?, ?)
#             ''', (vehicle_id, description, amount, date))
#             conn.commit()
#             st.success("Expense added successfully.")
#         except sqlite3.Error as e:
#             st.error(f"An error occurred: {e}")
#         finally:
#             conn.close()

# # app.py (add to sidebar forms)
# with st.sidebar.form("add_maintenance"):
#     st.subheader("Add Maintenance Log")
#     vehicle_id = st.number_input("Vehicle ID", min_value=1, step=1)
#     maintenance_type = st.text_input("Maintenance Type")
#     date = st.date_input("Date")
#     mileage = st.number_input("Mileage", min_value=0, step=100)
#     cost = st.number_input("Cost", min_value=0.0, step=10.0)
#     next_maintenance_date = st.date_input("Next Maintenance Date")
#     submitted_maintenance = st.form_submit_button("Add Maintenance")
    
#     if submitted_maintenance:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO MaintenanceLogs (vehicle_id, maintenance_type, date, mileage, cost, next_maintenance_date)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             ''', (vehicle_id, maintenance_type, date, mileage, cost, next_maintenance_date))
#             conn.commit()
#             st.success("Maintenance log added successfully.")
#         except sqlite3.Error as e:
#             st.error(f"An error occurred: {e}")
#         finally:
#             conn.close()


# # app.py (add predictive maintenance section)
# import pickle
# import pandas as pd

# # Load the trained model
# try:
#     with open('maintenance_model.pkl', 'rb') as f:
#         maintenance_model = pickle.load(f)
# except FileNotFoundError:
#     maintenance_model = None

# def predict_maintenance(mileage):
#     if maintenance_model:
#         prediction = maintenance_model.predict([[mileage]])
#         return prediction[0]
#     else:
#         return None

# # Display Predictive Maintenance
# st.subheader("🔮 Predictive Maintenance")
# vehicle_id = st.number_input("Enter Vehicle ID for Prediction", min_value=1, step=1)
# if st.button("Predict Next Maintenance Cost"):
#     conn = sqlite3.connect('db/vehicle_management.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT mileage FROM Vehicles WHERE id=?", (vehicle_id,))
#     result = cursor.fetchone()
#     conn.close()
#     if result:
#         mileage = result[0] if result[0] else 0
#         predicted_cost = predict_maintenance(mileage)
#         if predicted_cost:
#             st.write(f"**Predicted Maintenance Cost:** ${predicted_cost:.2f}")
#         else:
#             st.write("Model not trained or insufficient data.")
#     else:
#         st.error("Vehicle ID not found.")

# # app.py (add retrain model button)
# if st.button("Retrain Maintenance Model"):
#     import subprocess
#     result = subprocess.run(['python', 'train_model.py'], capture_output=True, text=True)
#     st.text(result.stdout)
#     # Reload the model
#     try:
#         with open('maintenance_model.pkl', 'rb') as f:
#             maintenance_model = pickle.load(f)
#         st.success("Model retrained successfully.")
#     except FileNotFoundError:
#         maintenance_model = None
#         st.error("Model training failed.")














# # app.py
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai
# import re

# # Load environment variables
# load_dotenv()

# # Configure Google Gemini API Key
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # Function to generate SQL query using Gemini
# def get_gemini_response(instruction, prompt):
#     model = genai.GenerativeModel('gemini-pro')  # Ensure 'gemini-pro' is the correct model name
#     full_prompt = prompt + instruction
#     response = model.generate_content([full_prompt])
#     return response.text

# # Function to execute SQL queries
# def execute_sql_query(sql, db='db/vehicle_management.db'):
#     # Basic validation to prevent dangerous operations
#     prohibited_commands = ['DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
#     sql_upper = sql.strip().upper()
#     for cmd in prohibited_commands:
#         if sql_upper.startswith(cmd):
#             return ("ERROR", f"Operation '{cmd}' is not permitted.")
    
#     conn = sqlite3.connect(db)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql)
#         # Determine the type of query
#         query_type = sql_upper.split()[0]
#         if query_type == "SELECT":
#             rows = cursor.fetchall()
#             return ("SELECT", rows)
#         else:
#             conn.commit()
#             return (query_type, "Query executed successfully.")
#     except sqlite3.Error as e:
#         return ("ERROR", f"An error occurred: {e}")
#     finally:
#         conn.close()

# # Function to clean and validate SQL response
# def clean_sql(sql_response):
#     # Remove code blocks and the word 'SQL' if present
#     sql_response = re.sub(r'```', '', sql_response)
#     sql_response = re.sub(r'\bsql\b', '', sql_response, flags=re.IGNORECASE)
#     return sql_response.strip()

# # Define your Prompt with data manipulation examples
# prompt = """
# You are an expert in converting English instructions to SQL queries for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Please convert the following natural language instructions into valid SQL queries.
# Do not include any markdown formatting or the word 'SQL' in your response.

# Here are some examples:

# Example 1:
# Instruction: Show me all vehicles from 2020.
# SQL Query: SELECT * FROM Vehicles WHERE year = 2020;

# Example 2:
# Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
# SQL Query: INSERT INTO Vehicles (make, model, year, license_plate) VALUES ('Toyota', 'Corolla', 2022, 'ABC123');

# Example 3:
# Instruction: Update the license plate of the vehicle with ID 3 to XYZ789.
# SQL Query: UPDATE Vehicles SET license_plate = 'XYZ789' WHERE id = 3;

# Example 4:
# Instruction: Delete the expense with ID 5.
# SQL Query: DELETE FROM Expenses WHERE id = 5;

# Now, convert the following instruction into an SQL query:
# """

# # Streamlit App Configuration
# st.set_page_config(page_title="Vehicle Management App", layout="wide")
# st.header("🚗 Vehicle Management System with Conversational UI")

# # User Input
# instruction = st.text_input("Enter your command:", key="input")

# submit = st.button("Execute")

# if submit and instruction:
#     with st.spinner("Generating SQL query..."):
#         sql_response = get_gemini_response(instruction, prompt)
#         sql_query = clean_sql(sql_response)
    
#     st.subheader("Generated SQL Query:")
#     st.code(sql_query, language='sql')
    
#     # Detect if the query is potentially destructive
#     destructive_commands = ['DELETE']
#     query_type = sql_query.strip().split()[0].upper()
    
#     if query_type in destructive_commands:
#         confirm = st.checkbox("⚠️ Are you sure you want to execute this operation?")
#         if confirm:
#             with st.spinner("Executing SQL query..."):
#                 result_type, result = execute_sql_query(sql_query)
            
#             st.subheader("Execution Result:")
#             if result_type == "SELECT":
#                 if result:
#                     # Fetch column names for better table display
#                     conn = sqlite3.connect('db/vehicle_management.db')
#                     cursor = conn.cursor()
#                     cursor.execute(sql_query)
#                     columns = [description[0] for description in cursor.description]
#                     conn.close()
#                     # Convert result to list of dicts for better display
#                     data = [dict(zip(columns, row)) for row in result]
#                     st.table(data)
#                 else:
#                     st.write("No records found.")
#             elif result_type in destructive_commands:
#                 st.success(result)
#             else:
#                 st.error(result)
#         else:
#             st.info("Operation cancelled.")
#     else:
#         # Non-destructive queries
#         with st.spinner("Executing SQL query..."):
#             result_type, result = execute_sql_query(sql_query)
        
#         st.subheader("Execution Result:")
#         if result_type == "SELECT":
#             if result:
#                 # Fetch column names for better table display
#                 conn = sqlite3.connect('db/vehicle_management.db')
#                 cursor = conn.cursor()
#                 cursor.execute(sql_query)
#                 columns = [description[0] for description in cursor.description]
#                 conn.close()
#                 # Convert result to list of dicts for better display
#                 data = [dict(zip(columns, row)) for row in result]
#                 st.table(data)
#             else:
#                 st.write("No records found.")
#         elif result_type in destructive_commands:
#             st.success(result)
#         else:
#             st.success(result)

# # Optional: Add manual forms for adding vehicles and expenses

# st.sidebar.header("Add Data")

# # Add Vehicle Form
# with st.sidebar.form("add_vehicle"):
#     st.subheader("Add a New Vehicle")
#     make = st.text_input("Make")
#     model = st.text_input("Model")
#     year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
#     license_plate = st.text_input("License Plate")
#     submitted_vehicle = st.form_submit_button("Add Vehicle")
    
#     if submitted_vehicle:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Vehicles (make, model, year, license_plate)
#                 VALUES (?, ?, ?, ?)
#             ''', (make, model, year, license_plate))
#             conn.commit()
#             st.success("Vehicle added successfully.")
#         except sqlite3.IntegrityError:
#             st.error("License plate already exists.")
#         finally:
#             conn.close()

# # Add Expense Form
# with st.sidebar.form("add_expense"):
#     st.subheader("Add a New Expense")
#     vehicle_id = st.number_input("Vehicle ID", min_value=1, step=1)
#     description = st.text_input("Description")
#     amount = st.number_input("Amount", min_value=0.0, step=0.1)
#     date = st.date_input("Date")
#     submitted_expense = st.form_submit_button("Add Expense")
    
#     if submitted_expense:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Expenses (vehicle_id, description, amount, date)
#                 VALUES (?, ?, ?, ?)
#             ''', (vehicle_id, description, amount, date))
#             conn.commit()
#             st.success("Expense added successfully.")
#         except sqlite3.Error as e:
#             st.error(f"An error occurred: {e}")
#         finally:
#             conn.close()
# app.py







# # app.py
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai
# import re
# import json
# from ast import literal_eval
# import pandas as pd
# import plotly.express as px
# import altair as alt

# # Load environment variables
# load_dotenv()

# # Configure Google Gemini API Key
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # ------------------------------
# # Helper Functions
# # ------------------------------



# def get_gemini_response(instruction, prompt):
#     model = genai.GenerativeModel('gemini-pro')  # Ensure 'gemini-pro' is the correct model name
#     full_prompt = prompt + instruction
#     response = model.generate_content([full_prompt])
#     return response.text

# def execute_sql_query(sql, db='db/vehicle_management.db'):
#     # Basic validation to prevent dangerous operations
#     prohibited_commands = ['DROP', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
#     sql_upper = sql.strip().upper()
#     for cmd in prohibited_commands:
#         if sql_upper.startswith(cmd):
#             return ("ERROR", f"Operation '{cmd}' is not permitted.")
    
#     conn = sqlite3.connect(db)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql)
#         # Determine the type of query
#         query_type = sql_upper.split()[0]
#         if query_type == "SELECT":
#             rows = cursor.fetchall()
#             return ("SELECT", rows)
#         else:
#             conn.commit()
#             return (query_type, "Query executed successfully.")
#     except sqlite3.Error as e:
#         return ("ERROR", f"An error occurred: {e}")
#     finally:
#         conn.close()

# def clean_sql(sql_response):
#     # Remove code blocks and the word 'SQL' if present
#     sql_response = re.sub(r'```', '', sql_response)
#     sql_response = re.sub(r'\bsql\b', '', sql_response, flags=re.IGNORECASE)
#     return sql_response.strip()

# def generate_description(table_data, prompt):
#     """
#     Generates a natural language description based on table data.

#     Args:
#         table_data (list of tuples): The result of the SQL query.
#         prompt (str): The prompt guiding the AI to generate the description.

#     Returns:
#         str: The generated description.
#     """
#     if not table_data:
#         return "There are no vehicles in the database."

#     # Assuming the table has columns: ID, Make, Model, Year, License Plate
#     headers = ["ID", "Make", "Model", "Year", "License Plate"]
#     table_md = "| " + " | ".join(headers) + " |\n"
#     table_md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
#     for row in table_data:
#         table_md += "| " + " | ".join(map(str, row)) + " |\n"

#     # Complete prompt with the table data
#     full_prompt = prompt + "\n" + table_md + "\nDescription:"

#     # Generate description using Gemini API
#     description = get_gemini_response(full_prompt, "")  # Empty prompt since it's included in full_prompt

#     # Clean the response
#     description = clean_description(description)

#     return description

# def clean_description(description_response):
#     """
#     Cleans the AI-generated description by removing any unwanted formatting.

#     Args:
#         description_response (str): The raw response from the AI.

#     Returns:
#         str: The cleaned description.
#     """
#     # Remove any code blocks or markdown if present
#     description = re.sub(r'```', '', description_response)
#     description = re.sub(r'\bDescription:\b', '', description, flags=re.IGNORECASE)
#     return description.strip()

# def extract_form_data(instruction, prompt):
#     model = genai.GenerativeModel('gemini-pro')  # Ensure the model name is correct
#     full_prompt = prompt + instruction
#     response = model.generate_content([full_prompt])
#     return response.text

# # ------------------------------
# # Prompts
# # ------------------------------

# # Prompt for SQL Query Conversion
# query_prompt = """
# You are an expert in converting English instructions to SQL queries for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Please convert the following natural language instructions into valid SQL queries.
# Do not include any markdown formatting or the word 'SQL' in your response.

# Here are some examples:

# Example 1:
# Instruction: Show me all vehicles from 2020.
# SQL Query: SELECT * FROM Vehicles WHERE year = 2020;

# Example 2:
# Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
# SQL Query: INSERT INTO Vehicles (make, model, year, license_plate) VALUES ('Toyota', 'Corolla', 2022, 'ABC123');

# Example 3:
# Instruction: Update the license plate of the vehicle with ID 3 to XYZ789.
# SQL Query: UPDATE Vehicles SET license_plate = 'XYZ789' WHERE id = 3;

# Example 4:
# Instruction: Delete the expense with ID 5.
# SQL Query: DELETE FROM Expenses WHERE id = 5;

# Now, convert the following instruction into an SQL query:
# """

# # Prompt for Natural Language Description Generation
# description_prompt = """
# You are an expert in generating natural language descriptions from tabular data for a vehicle management system.
# Given the following table of vehicles, provide a concise and clear description summarizing the information.

# Here is the table:

# | ID | Make    | Model   | Year | License Plate |
# |----|---------|---------|------|---------------|
# | 1  | Toyota  | Corolla | 2022 | ABC123        |
# | 2  | Honda   | Civic   | 2021 | DEF456        |

# Description:
# There are two vehicles in the database. The first is a 2022 Toyota Corolla with the license plate ABC123. The second is a 2021 Honda Civic with the license plate DEF456.

# Now, generate a similar description for the following table:
# """

# # Prompt for Form Data Extraction
# form_prompt = """
# You are an expert in extracting structured data from natural language instructions for a vehicle management system.
# The SQLite database has the following tables:

# 1. Vehicles:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - make (TEXT NOT NULL)
#    - model (TEXT NOT NULL)
#    - year (INTEGER)
#    - license_plate (TEXT UNIQUE NOT NULL)

# 2. Expenses:
#    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
#    - vehicle_id (INTEGER)
#    - description (TEXT)
#    - amount (REAL)
#    - date (TEXT)
   
# Extract the relevant fields from the following instruction and present them in JSON format with the appropriate keys.

# Here are some examples:

# Example 1:
# Instruction: Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.
# Extracted Data: {"make": "Toyota", "model": "Corolla", "year": 2022, "license_plate": "ABC123"}

# Example 2:
# Instruction: Add an expense for vehicle ID 3 with description "Oil Change", amount 75.50, and date 2024-04-15.
# Extracted Data: {"vehicle_id": 3, "description": "Oil Change", "amount": 75.50, "date": "2024-04-15"}

# Now, extract the data from the following instruction:
# Instruction:
# """

# # ------------------------------
# # Data Fetching
# # ------------------------------

# def fetch_data():
#     conn = sqlite3.connect('db/vehicle_management.db')
#     vehicles_df = pd.read_sql_query("SELECT * FROM Vehicles;", conn)
#     expenses_df = pd.read_sql_query("SELECT * FROM Expenses;", conn)
#     conn.close()
#     return vehicles_df, expenses_df

# vehicles_df, expenses_df = fetch_data()

# # ------------------------------
# # Visualization Functions
# # ------------------------------

# def plot_vehicles_by_make(dataframe):
#     if dataframe.empty:
#         st.warning("No vehicle data available to display.")
#         return
    
#     # Generate count of vehicles by make
#     count_df = dataframe['make'].value_counts().reset_index()
    
#     if count_df.empty:
#         st.warning("No vehicle makes found in the data.")
#         return
    
#     # Rename columns to match Plotly's expectations
#     count_df.columns = ['make', 'count']
    
#     # Check if 'make' and 'count' columns exist
#     if not {'make', 'count'}.issubset(count_df.columns):
#         st.error("DataFrame does not contain the required columns for plotting.")
#         return
    
#     # Create a bar chart using Plotly
#     fig = px.bar(
#         count_df,
#         x='make',
#         y='count',
#         title='Number of Vehicles by Make',
#         labels={'make': 'Manufacturer', 'count': 'Number of Vehicles'},
#         color='make',
#         template='plotly_dark'
#     )
    
#     # Display the plot in Streamlit
#     st.plotly_chart(fig, use_container_width=True)

# def plot_vehicles_by_year(dataframe):
#     if dataframe.empty:
#         st.warning("No vehicle data available to display.")
#         return
    
#     fig = px.histogram(
#         dataframe,
#         x='year',
#         nbins=10,
#         title='Number of Vehicles by Year',
#         labels={'year': 'Manufacturing Year', 'count': 'Number of Vehicles'},
#         color='year',
#         template='plotly_dark'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def plot_expenses_per_vehicle(expenses_df, vehicles_df):
#     if expenses_df.empty or vehicles_df.empty:
#         st.warning("Insufficient data to display expenses per vehicle.")
#         return
    
#     # Merge expenses with vehicles to get license_plate and make/model
#     merged_df = expenses_df.merge(vehicles_df, left_on='vehicle_id', right_on='id', how='left')
    
#     if merged_df.empty:
#         st.warning("No expenses associated with any vehicle.")
#         return
    
#     total_expenses = merged_df.groupby(['license_plate', 'make', 'model'])['amount'].sum().reset_index()
    
#     if total_expenses.empty:
#         st.warning("No expenses found to aggregate.")
#         return
    
#     fig = px.bar(
#         total_expenses,
#         x='license_plate',
#         y='amount',
#         hover_data=['make', 'model'],
#         title='Total Expenses per Vehicle',
#         labels={'license_plate': 'License Plate', 'amount': 'Total Expenses'},
#         color='amount',
#         template='plotly_dark'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def plot_expenses_over_time(expenses_df):
#     if expenses_df.empty:
#         st.warning("No expense data available to display.")
#         return
    
#     expenses_df['date'] = pd.to_datetime(expenses_df['date'], errors='coerce')
#     expenses_over_time = expenses_df.dropna(subset=['date']).groupby(expenses_df['date'].dt.to_period('M'))['amount'].sum().reset_index()
#     expenses_over_time['date'] = expenses_over_time['date'].dt.to_timestamp()
    
#     if expenses_over_time.empty:
#         st.warning("No valid dates found in expenses data.")
#         return
    
#     fig = px.line(
#         expenses_over_time,
#         x='date',
#         y='amount',
#         title='Expenses Over Time',
#         labels={'date': 'Date', 'amount': 'Total Expenses'},
#         template='plotly_dark'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# def plot_vehicle_models(dataframe):
#     if dataframe.empty:
#         st.warning("No vehicle data available to display.")
#         return
    
#     model_counts = dataframe['model'].value_counts().reset_index()
    
#     if model_counts.empty:
#         st.warning("No vehicle models found in the data.")
#         return
    
#     model_counts.columns = ['model', 'count']
    
#     fig = px.pie(
#         model_counts,
#         names='model',
#         values='count',
#         title='Distribution of Vehicle Models',
#         hole=0.4,
#         template='plotly_dark'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# # ------------------------------
# # Streamlit App Configuration
# # ------------------------------

# st.set_page_config(page_title="Vehicle Management App", layout="wide")
# st.title("🚗 Vehicle Management System with Conversational UI and Visualizations")

# # ------------------------------
# # Initialize session state for form fields
# # ------------------------------

# form_fields = {
#     "make": "",
#     "model": "",
#     "year": "",
#     "license_plate": "",
#     "vehicle_id": "",
#     "description": "",
#     "amount": "",
#     "date": ""
# }

# for key in form_fields:
#     if f'form_{key}' not in st.session_state:
#         st.session_state[f'form_{key}'] = ""

# # ------------------------------
# # Conversational UI Section
# # ------------------------------
# st.markdown("---")
# st.subheader("💬 Execute Commands")

# # User Input for Conversational UI
# instruction = st.text_input("Enter your command:", key="input")

# submit = st.button("Execute")

# if submit and instruction:
#     with st.spinner("Generating SQL query..."):
#         sql_response = get_gemini_response(instruction, query_prompt)
#         sql_query = clean_sql(sql_response)
    
#     st.subheader("📄 Generated SQL Query:")
#     st.code(sql_query, language='sql')
    
#     # Detect if the query is potentially destructive
#     destructive_commands = [ 'DELETE']
#     query_type = sql_query.strip().split()[0].upper()
    
#     if query_type in destructive_commands:
#         confirm = st.checkbox("⚠️ Are you sure you want to execute this operation?")
#         if confirm:
#             with st.spinner("Executing SQL query..."):
#                 result_type, result = execute_sql_query(sql_query)
            
#             st.subheader("✅ Execution Result:")
#             if result_type == "SELECT":
#                 if result:
#                     # Fetch column names for better table display
#                     conn = sqlite3.connect('db/vehicle_management.db')
#                     cursor = conn.cursor()
#                     cursor.execute(sql_query)
#                     columns = [description[0] for description in cursor.description]
#                     conn.close()
#                     # Convert result to list of dicts for better display
#                     data = [dict(zip(columns, row)) for row in result]
#                     df = pd.DataFrame(data)
#                     st.table(df)
                    
#                     # Generate and display description
#                     description = generate_description(result, description_prompt)
#                     st.subheader("📝 Description:")
#                     st.write(description)
#                 else:
#                     st.write("No records found.")
#             elif result_type in destructive_commands:
#                 st.success(result)
#             else:
#                 st.error(result)
#     else:
#         # Non-destructive queries
#         with st.spinner("Executing SQL query..."):
#             result_type, result = execute_sql_query(sql_query)
        
#         st.subheader("✅ Execution Result:")
#         if result_type == "SELECT":
#             if result:
#                 # Fetch column names for better table display
#                 conn = sqlite3.connect('db/vehicle_management.db')
#                 cursor = conn.cursor()
#                 cursor.execute(sql_query)
#                 columns = [description[0] for description in cursor.description]
#                 conn.close()
#                 # Convert result to list of dicts for better display
#                 data = [dict(zip(columns, row)) for row in result]
#                 df = pd.DataFrame(data)
#                 st.table(df)
                
#                 # Generate and display description
#                 description = generate_description(result, description_prompt)
#                 st.subheader("📝 Description:")
#                 st.write(description)
#             else:
#                 st.write("No records found.")
#         elif result_type in destructive_commands:
#             st.success(result)
#         else:
#             st.success(result)

# # ------------------------------
# # Natural Language Form Filling Section
# # ------------------------------
# st.markdown("---")
# st.subheader("📝 Fill Forms Using Natural Language")

# # Natural Language Input
# nl_instruction = st.text_input("Enter your instruction to fill the form:", key="nl_input")

# # Button to parse instruction
# parse_button = st.button("Parse Instruction")

# if parse_button and nl_instruction:
#     with st.spinner("Parsing instruction..."):
#         extracted_data = extract_form_data(nl_instruction, form_prompt)
#         try:
#             data = json.loads(extracted_data)
#             st.success("✅ Instruction parsed successfully!")
#             st.json(data)  # Display the extracted data
            
#             # Populate session state
#             for key, value in data.items():
#                 st.session_state[f'form_{key}'] = value
#         except json.JSONDecodeError:
#             st.error("🚫 Failed to parse the instruction. Please ensure it's clear and follows the examples.")

# # ------------------------------
# # Sidebar Forms for Manual Data Entry
# # ------------------------------
# st.sidebar.header("📂 Add Data")

# # Add Vehicle Form
# with st.sidebar.form("add_vehicle"):
#     st.subheader("➕ Add a New Vehicle")
#     make = st.text_input("Make", value=st.session_state.get('form_make', ''))
#     model = st.text_input("Model", value=st.session_state.get('form_model', ''))
#     year_input = st.text_input("Year", value=str(st.session_state.get('form_year', '2000')))
#     # Convert year to integer if possible
#     try:
#         year = int(year_input)
#     except ValueError:
#         year = 2000  # Default value or handle accordingly
#     license_plate = st.text_input("License Plate", value=st.session_state.get('form_license_plate', ''))
#     submitted_vehicle = st.form_submit_button("Add Vehicle")
    
#     if submitted_vehicle:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Vehicles (make, model, year, license_plate)
#                 VALUES (?, ?, ?, ?)
#             ''', (make, model, year, license_plate))
#             conn.commit()
#             st.success("✅ Vehicle added successfully.")
            
#             # Clear form fields in session state after successful submission
#             for key in ['make', 'model', 'year', 'license_plate']:
#                 st.session_state[f'form_{key}'] = ""
#         except sqlite3.IntegrityError:
#             st.error("🚫 License plate already exists.")
#         finally:
#             conn.close()

# # Add Expense Form
# with st.sidebar.form("add_expense"):
#     st.subheader("➕ Add a New Expense")
#     vehicle_id_input = st.text_input("Vehicle ID", value=str(st.session_state.get('form_vehicle_id', '1')))
#     # Convert vehicle_id to integer if possible
#     try:
#         vehicle_id = int(vehicle_id_input)
#     except ValueError:
#         vehicle_id = 1  # Default value or handle accordingly
#     description = st.text_input("Description", value=st.session_state.get('form_description', ''))
#     amount_input = st.text_input("Amount", value=str(st.session_state.get('form_amount', '0.0')))
#     # Convert amount to float if possible
#     try:
#         amount = float(amount_input)
#     except ValueError:
#         amount = 0.0
#     date_input = st.text_input("Date (YYYY-MM-DD)", value=str(st.session_state.get('form_date', '2024-01-01')))
#     try:
#         date = pd.to_datetime(date_input).date()
#     except:
#         date = pd.to_datetime('2024-01-01').date()
#     submitted_expense = st.form_submit_button("Add Expense")
    
#     if submitted_expense:
#         conn = sqlite3.connect('db/vehicle_management.db')
#         cursor = conn.cursor()
#         try:
#             cursor.execute('''
#                 INSERT INTO Expenses (vehicle_id, description, amount, date)
#                 VALUES (?, ?, ?, ?)
#             ''', (vehicle_id, description, amount, date))
#             conn.commit()
#             st.success("✅ Expense added successfully.")
            
#             # Clear form fields in session state after successful submission
#             for key in ['vehicle_id', 'description', 'amount', 'date']:
#                 st.session_state[f'form_{key}'] = ""
#         except sqlite3.Error as e:
#             st.error(f"🚫 An error occurred: {e}")
#         finally:
#             conn.close()

# # ------------------------------
# # Data Visualization Section
# # ------------------------------
# st.markdown("---")
# st.subheader("📊 Data Visualizations")

# # Fetch updated data after any operation
# vehicles_df, expenses_df = fetch_data()

# # Sidebar Navigation for Visualizations
# visualization = st.sidebar.selectbox(
#     "Select a visualization to display:",
#     [
#         "Vehicles by Make",
#         "Vehicles by Year",
#         "Total Expenses per Vehicle",
#         "Expenses Over Time",
#         "Vehicle Model Distribution"
#     ]
# )

# # Display the selected visualization
# if visualization == "Vehicles by Make":
#     st.subheader("🚗 Number of Vehicles by Make")
#     plot_vehicles_by_make(vehicles_df)

# elif visualization == "Vehicles by Year":
#     st.subheader("📅 Number of Vehicles by Year")
#     plot_vehicles_by_year(vehicles_df)

# elif visualization == "Total Expenses per Vehicle":
#     st.subheader("💰 Total Expenses per Vehicle")
#     plot_expenses_per_vehicle(expenses_df, vehicles_df)

# elif visualization == "Expenses Over Time":
#     st.subheader("📈 Expenses Over Time")
#     plot_expenses_over_time(expenses_df)

# elif visualization == "Vehicle Model Distribution":
#     st.subheader("🚘 Distribution of Vehicle Models")
#     plot_vehicle_models(vehicles_df)
