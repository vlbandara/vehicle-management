# Vehicle Management App

🚗 **Vehicle Management System with Conversational UI**

Welcome to the Vehicle Management App! This application allows vehicle owners to manage their vehicles and expenses through a user-friendly conversational interface. Leveraging advanced Natural Language Processing (NLP) capabilities with LangChain and OpenAI's GPT-3.5 Turbo, the app converts natural language instructions into SQL queries, making vehicle management seamless and intuitive.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Database Setup](#database-setup)
  - [Running the Application](#running-the-application)
  - [Using Docker](#using-docker)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Conversational UI:** Interact with the app using natural language commands.
- **SQL Query Generation:** Automatically converts instructions into SQL queries.
- **Contextual Understanding:** Maintains context across interactions for complex instructions.
- **Error Handling:** Provides meaningful suggestions when instructions are unclear.
- **Data Management:** Add, view, update, and delete vehicle and expense records.
- **Form Filling:** Extracts structured data from natural language instructions to fill forms.
- **Secure Operations:** Prevents execution of potentially destructive SQL commands.



## Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite
- **NLP:** LangChain, OpenAI GPT-3.5 Turbo
- **Containerization:** Docker (optional)

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8 or higher:** [Download Python](https://www.python.org/downloads/)
- **Git:** [Download Git](https://git-scm.com/downloads)
- **Docker (optional):** [Download Docker](https://www.docker.com/get-started)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/VEHICLE-MANAGEMENT-APP.git
   cd VEHICLE-MANAGEMENT-APP
   ```

2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   - **Using `venv`:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

   - **Using `conda`:**

     ```bash
     conda create -n vehicle-management-app python=3.8
     conda activate vehicle-management-app
     ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables**

   The application requires certain environment variables to function correctly. Create a `.env` file in the root directory of the project and add the necessary variables.

   ```bash
   touch .env
   ```

   Open the `.env` file in a text editor and add the following:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # If you're still using Google Gemini, add:
   # GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

   **Note:** Replace `your_openai_api_key_here` with your actual OpenAI API key. If you plan to use Google Gemini, also include your Google API key.

2. **Obtain OpenAI API Key**

   - Sign up or log in to [OpenAI](https://platform.openai.com/).
   - Navigate to the API section and generate a new API key.
   - Copy the key and paste it into the `.env` file as shown above.

### Database Setup

Initialize the SQLite database with the necessary tables.

1. **Run the Database Setup Script**

   ```bash
   python db_setup.py
   ```

   This script will create the `vehicle_management.db` SQLite database with the required tables: `Vehicles` and `Expenses`.

### Running the Application

Start the Streamlit application using the following command:

```bash
streamlit run app.py
```

Upon successful execution, Streamlit will provide a local URL (typically `http://localhost:8501`). Open this URL in your web browser to interact with the Vehicle Management App.

### Using Docker

If you prefer using Docker to containerize the application, follow these steps:

1. **Build the Docker Image**

   ```bash
   docker build -t vehicle-management-app .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -d -p 8501:8501 --name vehicle-management-app \
     --env-file .env \
     vehicle-management-app
   ```

3. **Access the App**

   Open `http://localhost:8501` in your web browser.

**Note:** Ensure that your `.env` file is correctly configured with the necessary environment variables before building the Docker image.

## Usage

### Conversational UI

1. **Enter Command:**
   - In the "Enter your command" text box, type your instruction. For example:
     - `Show me all vehicles from 2020.`
     - `Add a new vehicle with make Toyota, model Corolla, year 2022, and license plate ABC123.`

2. **Execute Command:**
   - Click the **"Execute"** button to generate and execute the corresponding SQL query.

3. **View Results:**
   - The generated SQL query and its execution result will be displayed below the input box.

4. **Confirmation for Destructive Operations:**
   - For operations like `DELETE`, a confirmation checkbox will appear to prevent accidental data loss.

### Natural Language Form Filling

1. **Enter Instruction:**
   - In the "Enter your instruction to fill the form" text box, type your instruction. For example:
     - `Add an expense for vehicle ID 3 with description "Oil Change", amount 75.50, and date 2024-04-15.`

2. **Parse Instruction:**
   - Click the **"Parse Instruction"** button to extract structured data from your instruction.

3. **View Extracted Data:**
   - The extracted data will be displayed in JSON format and automatically populate the corresponding form fields in the sidebar.

### Manual Data Entry

Use the sidebar to manually add vehicles and expenses through structured forms.

1. **Add Vehicle:**
   - Fill in the vehicle details and click **"Add Vehicle"**.

2. **Add Expense:**
   - Fill in the expense details and click **"Add Expense"**.

## Project Structure

```
VEHICLE-MANAGEMENT-APP/
├── .streamlit/                 # Streamlit configuration files
├── db/                         # Database files and setup scripts
├── utils/                      # Utility modules
│   ├── langchain_config.py     # LangChain configuration
│   └── nlp_helpers.py          # NLP helper functions
├── venv/                       # Virtual environment (if applicable)
├── .dockerignore               # Docker ignore file
├── .env                        # Environment variables
├── .gitattributes              # Git attributes
├── .gitignore                  # Git ignore file
├── app.py                      # Main Streamlit application
├── db_setup.py                 # Database setup script
├── Dockerfile                  # Dockerfile for containerization
└── requirements.txt            # Python dependencies
```

## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. **Fork the Repository**

   Click the **Fork** button at the top-right corner of this page to create a personal copy of the repository.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your-username/VEHICLE-MANAGEMENT-APP.git
   cd VEHICLE-MANAGEMENT-APP
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add feature: Your feature description"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

   Go to the original repository and click **New Pull Request** to submit your changes for review.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the powerful and easy-to-use web app framework.
- [LangChain](https://www.langchain.com/) for enhancing NLP capabilities.
- [OpenAI](https://openai.com/) for providing the GPT-3.5 Turbo model.
- [SQLite](https://www.sqlite.org/index.html) for the lightweight database solution.

