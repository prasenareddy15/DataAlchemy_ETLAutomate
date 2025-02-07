##  Data Transformation and Insertion Script
This project contains a Python script, code_1.py, which automates the process of transforming data from a source SQL table and inserting it into a destination SQL table after applying certain transformations, such as splitting stringified columns and formatting date columns.

The project requires configuration files (config.json and .env) to provide database connection details and define transformation rules.

## Project Files
### 1. code_1.py
This is the main Python script that:
1) Connects to the SQL Server database.
2) Creates a destination table based on the structure of the source table.
3) Transforms data from the source table (e.g., splits stringified columns, formats dates, etc.).
4) Inserts transformed data into the destination table.
### 2. config.json
A JSON file that specifies:
1) Source table names.
2) Destination file name.
3) Stringified columns and how many values to split for each column.
4) Columns that should be treated as dates.
Example config.json Structure:
{
    "source_table_name": {
        "stringified_columns": {
            "column_name1": 3,
            "column_name2": 2
        },
        "colDate": ["column_name1", "column_name2"]
    },
    "another_source_table": {
        "stringified_columns": {
            "column_name3": 2
        },
        "colDate": ["column_name3"]
    }
}
stringified_columns: A dictionary of columns where each key is a column name and the value is the number of values to split.
colDate: A list of column names that should be treated as dates.
### 3. .env
A file containing database connection details. This file is used to securely store sensitive information.
### 4 You can use Windows Task Scheduler to execute this .bat file daily.
Steps to Schedule:
#### Open Task Scheduler:
Press Win + R, type taskschd.msc, and press Enter.
#### Create a New Task:
Click on "Create Basic Task" on the right panel.
Give your task a name (e.g., "Run Data Transformation Script Daily") and optionally add a description.
#### Set the Trigger:
Choose "Daily" as the trigger and set the time you want the script to run.
#### Set the Action:
Select "Start a Program."
Browse to the .bat file you created earlier.
#### Finalize and Save:
Review the summary and click "Finish."
#### Additional Settings (Optional):
1) To ensure the task runs even if you're logged out:
2) Go to the task's properties.
3) Under the "General" tab, select "Run whether user is logged on or not."
4) Check "Do not store password" for higher security.
### 5. Dependencies
## To run the script, the following libraries and tools are required:
1) Python Libraries
2) sqlalchemy
3) pyodbc
4) datetime
5) json
6) dotenv
#### Install them using the following command:
bash
pip install sqlalchemy pyodbc python-dotenv
Required Software
1) Python
Download and install Python from Python.org. Ensure that Python is added to your system's PATH.
2) SQL Server
Install Microsoft SQL Server or ensure access to an existing SQL Server instance.
3) ODBC Driver 17 for SQL Server
Download and install the driver from the Microsoft ODBC Driver for SQL Server page.

## How to Use
### Step 1: Prepare the Files
Place the code_1.py, config.json, and .env files in the same directory.
Populate the .env file with your SQL Server connection details.
Define the transformation rules for your tables in the config.json file.
### Step 2: Run the Script
Use the following command to execute the script
bash
python code_1.py --config_file config.json
Example Execution
{
    "example_table": {
        "stringified_columns": {
            "column2": 2
        },
        "colDate": ["date_column"]
    }
}
### Run the script:
bash
python code_1.py --config_file config.json

## Functionality Breakdown
### 1. get_db_engine()
Creates a SQLAlchemy engine using connection details from the .env file. This is used for executing database queries.

### 2. transform_and_insert_data()
Fetches data from the source table.
Splits stringified columns into multiple separate columns.
Formats dates into mm-dd-yyyy format.
Inserts transformed data into the destination table.
### 3. create_destination_table()
Queries the source table structure.
Dynamically creates the destination table with split columns and formatted date columns.
### 4. process_multiple_tables()
Iterates through the configuration file and applies the transformation and insertion process to all specified tables.
Key Notes
## Date Handling
-> Dates in the colDate list are converted to DATETIME2 in the destination table.
-> Dates with a value of 01-01-0001 are treated as base dates and preserved as 01-01-0001.
-> Null Values
-> Stringified columns with missing or empty values are stored as NULL.
## Dynamic Table Creation
-> The destination table is created dynamically with column names like column1_1, column1_2, etc., for split stringified columns.
## Error Handling
-> Invalid date strings are stored as NULL.
-> Missing values in stringified columns are also stored as NULL.
## Troubleshooting
## Connection Issues
-> Ensure the ODBC driver is installed and properly configured.
-> Verify that the .env file has the correct credentials and server details.
## Missing Dependencies
-> Ensure all required libraries are installed using:
bash
pip install -r requirements.txt
## Invalid Configuration
-> Ensure the config.json file follows the correct structure.
## Permissions
-> Ensure the database user has sufficient permissions to create tables and insert data.
