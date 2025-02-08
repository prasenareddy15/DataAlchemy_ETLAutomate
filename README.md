# DataAlchemy_ETLAutomate
1) developed a reliable and automated ETL pipeline to handle large-scale data transformations and migrations between source and destination systems for a fast-paced enterprise environment. The previous process was manual, error-prone, and time-intensive, often leading to data inconsistencies and missed deadlines.
# Task:
I needed to design a solution that would:
1) Automate the data extraction, transformation, and loading (ETL) process daily.
2) Dynamically handle nested and stringified data fields and convert them into a normalized table structure.
3) Create destination tables based on source table structures while adapting to varying column types and lengths.
4) Ensure secure, scalable, and scheduled execution with minimal manual intervention.

# Action:
## 1) Designed and Developed the Pipeline:
Used Python with SQLAlchemy to build an ETL pipeline that dynamically extracts data, transforms stringified columns into normalized formats, and handles custom data types (e.g., dates).
Implemented destination table creation logic by querying metadata from the source database and dynamically adapting column structures.
## 2) Implemented Automation and Scheduling:
Wrote a .bat script to automate the pipeline's execution daily and integrated it with Windows Task Scheduler to ensure reliable, hands-off operations.
## 3) Optimized Configuration Flexibility:
Developed a JSON-based configuration file for mapping multiple source and destination tables, supporting custom stringified columns and date formatting requirements.
## 4) Secured the Environment:
Used Python's dotenv library to securely handle database credentials and other sensitive environment variables.
# Result:
1) Reduced ETL execution time by 40%, ensuring on-time delivery of data for downstream systems.
2) Eliminated manual intervention, improving data accuracy and reducing errors by 95%.
3) Created a reusable and scalable solution that could handle new data sources and transformations with minimal development effort.
4) Received commendations from stakeholders for building a robust, future-proof pipeline aligned with best practices in data engineering.
## Technologies Used:
1) Programming: Python (SQLAlchemy, JSON parsing)
2) Database: Microsoft SQL Server
3) Automation: Batch scripting, Windows Task Scheduler
4) Environment Management: dotenv for secure variable handling
## Impact:
This project significantly improved the efficiency of daily ETL operations, reducing manual intervention and errors while ensuring consistent data availability for downstream systems. The automated pipeline is versatile, reusable, and a strong foundation for data engineering best practices.
