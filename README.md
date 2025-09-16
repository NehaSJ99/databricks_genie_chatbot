# databricks_genie_chatbot

## Overview
This repository provides a Streamlit-based chatbot interface for interacting with Databricks Genie. The chatbot allows users to send natural language queries, receive responses, and view the generated SQL queries that Genie produces for those questions. It is designed for data teams and analysts who want to quickly generate and review SQL for Databricks using conversational AI.

## Features
- Chatbot interface using Streamlit
- Sends user queries to Databricks Genie API
- Displays Genie responses and the generated SQL
- Shows tabular or textual results from Genie

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```sh
git clone https://github.com/NehaSJ99/databricks_genie_chatbot.git

```

### 2. Create and Activate a Python Virtual Environment (Recommended)
```sh
python -m venv genie-env
# On Windows:
genie-env\Scripts\activate
# On macOS/Linux:
source genie-env/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Credentials
Create a `.env` file in the project root directory with the following content:
```
DATABRICKS_INSTANCE=your-databricks-instance-url
SPACE_ID=your-space-id
AUTH_TOKEN=your-databricks-personal-access-token
```
- `DATABRICKS_INSTANCE`: The hostname of your Databricks workspace (e.g., adb-1234567890123456.7.azuredatabricks.net)
- `SPACE_ID`: The Genie space ID you want to use
- `AUTH_TOKEN`: Your Databricks personal access token

### 5. Run the Streamlit App
```sh
streamlit run streamlit_app.py
```

## How It Works
1. The user enters a question in the Streamlit chatbot interface.
2. The app sends the question to the Databricks Genie API using the credentials from the `.env` file.
3. Genie processes the question, generates a SQL query, and executes it.
4. The app displays both the Genie response and the generated SQL query.
5. If the result is tabular, it is formatted and shown; otherwise, text or raw JSON is displayed.

## Required Credentials
- **Databricks Instance URL**: Found in your Databricks workspace URL.
- **Space ID**: Provided by your Databricks Genie admin or found in your Genie space settings.
- **Auth Token**: Generate a personal access token in your Databricks user settings -> Developer -> Create Token.

## Notes
- Make sure your Databricks account has access to Genie and the specified space.
- Do not share your `.env` file or credentials publicly.

## License
This project is licensed under the MIT License. See the LICENSE file for details.