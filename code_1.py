from sqlalchemy import text, create_engine
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import urllib

# Load environment variables from a .env file
load_dotenv()

# Get database connection details from .env variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# URL encode the password to handle special characters
password = urllib.parse.quote_plus(password)

# SQLAlchemy connection string for Microsoft SQL Server
driver = 'ODBC+Driver+17+for+SQL+Server'
connection_string = f'mssql+pyodbc://{server}/{database}?driver={driver}&trusted_connection=yes'

# Create a SQLAlchemy database engine
engine = create_engine(connection_string)

# Function to retrieve the database engine
def get_db_engine():
    return engine

# Function to transform and insert data from a source table to a destination table
def transform_and_insert_data(source_table, destination_table, stringified_columns, colDate):
    # Get the database engine
    engine = get_db_engine()
    
    # SQL query to select all data from the source table
    select_query = text(f"SELECT * FROM {source_table}")
    
    # Execute the query and fetch results
    with engine.connect() as connection:
        result = connection.execute(select_query)
        rows = result.fetchall()
        column_names = result.keys()  # Retrieve column names

    # Transform the data
    transformed_data = []
    for row in rows:
        row_dict = dict(zip(column_names, row))  # Convert row to a dictionary
        transformed_row = {}
        for col, value in row_dict.items():
            if col in stringified_columns:  # Handle stringified columns
                extracted_values = value.strip('{}').split(',')  # Parse the stringified values
                for i in range(stringified_columns[col]):  # Loop through the expected number of values
                    col_name = f"{col}_{i+1}"
                    extracted_value = extracted_values[i].strip('"') if i < len(extracted_values) else None
                    if not extracted_value:  # Handle empty or missing values
                        transformed_row[col_name] = None
                    else:
                        if col in colDate:  # Handle date columns
                            try:
                                date_obj = datetime.strptime(extracted_value, "%Y-%m-%d")
                                transformed_row[col_name] = date_obj.strftime("%m-%d-%Y")
                            except ValueError:  # Handle invalid date strings
                                transformed_row[col_name] = None
                        else:
                            transformed_row[col_name] = extracted_value
            else:
                # Convert "NULL" string to None for SQL NULL
                transformed_row[col] = None if value == "NULL" else value

        # Append the transformed row to the data list
        transformed_data.append(transformed_row)

    # Insert the transformed data into the destination table
    if transformed_data:
        columns = transformed_data[0].keys()
        insert_query = f"INSERT INTO {destination_table} ({', '.join(columns)}) VALUES ({', '.join([':' + col for col in columns])})"
        
        with engine.connect() as connection:
            connection.execute(text(insert_query), transformed_data)
            connection.commit()
            print(f"Data successfully inserted into {destination_table}")

# Function to create a destination table based on the structure of the source table
def create_destination_table(source_table, destination_table, stringified_columns, colDate):
    engine = get_db_engine()
    
    # SQL query to fetch column names and data types from the source table
    query_columns = text(f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{source_table}'
    """)
    # Query to calculate maximum length of stringified columns
    max_length_query = lambda col: f"SELECT MAX(LEN({col})) AS max_length FROM {source_table}"
    column_max_lengths = {}

    # Get column details and their max lengths
    with engine.connect() as connection:
        columns = connection.execute(query_columns).fetchall()
        for column in columns:
            if column.DATA_TYPE in ['varchar', 'nvarchar', 'char', 'nchar']:
                max_length = connection.execute(text(max_length_query(column.COLUMN_NAME))).scalar()
                column_max_lengths[column.COLUMN_NAME] = max_length or 1 

    # Drop the destination table if it exists
    drop_query = text(f"DROP TABLE IF EXISTS {destination_table}")
    with engine.connect() as connection:
        connection.execute(drop_query)
        connection.commit()

    # Create the destination table with the appropriate structure
    create_table_sql = f"CREATE TABLE {destination_table} ("
    for column in columns:
        column_name = column.COLUMN_NAME
        data_type = column.DATA_TYPE

        if column_name in stringified_columns:
            for i in range(1, stringified_columns[column_name] + 1):
                if column_name in colDate:  # Handle date columns
                    create_table_sql += f"{column_name}_{i} DATETIME2, "
                else:
                    create_table_sql += f"{column_name}_{i} {data_type}({column_max_lengths.get(column_name, 50)}), "
        else:
            if data_type in ['varchar', 'nvarchar', 'char', 'nchar']:
                max_length = column_max_lengths.get(column_name, 50)
                create_table_sql += f"{column_name} {data_type}({max_length}), "
            else:
                create_table_sql += f"{column_name} {data_type}, "
    create_table_sql = create_table_sql.rstrip(', ') + ')'

    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.commit()
        print(f"Table {destination_table} created successfully.")

    # Transform and insert data into the newly created table
    transform_and_insert_data(source_table, destination_table, stringified_columns, colDate)

# Function to process multiple tables based on a configuration file
def process_multiple_tables(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)

    for source_table, config_values in config.items():
        print(source_table)
        destination_table=config_values["destination_table_name"]
        stringified_columns = config_values["stringified_columns"]
        colDate = set(config_values["colDate"])
        print(f"Processing table: {source_table}")
        create_destination_table(source_table, destination_table, stringified_columns, colDate)

# Main function to handle command-line arguments
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process multiple tables for data transformation and insertion.")
    parser.add_argument("--config_file", required=True, help="Path to configuration file for stringified columns and date columns")

    args = parser.parse_args()

    process_multiple_tables(args.config_file)
