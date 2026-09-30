"""
process.py

A small ETL pipeline for loading my mock CSV data into a MySQL database.
Reads DB credentials from environment variables, loads and cleans
a CSV file, and uploads the cleaned data into a table named 'mock'.
"""

import os
import logging
import pandas as pd
from sqlalchemy import create_engine

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# read_data
"""
    Read a CSV file into a pandas DataFrame.
    Parameters:
        filename - str (Path to the CSV file)
    Returns:
        df - pd.DataFrame (The loaded DataFrame)
    """
def read_data(filename):
    logging.info(f"Reading data from {filename}")
    try:
        df = pd.read_csv(filename)
        logging.info(f"Loaded {len(df)} rows")
        return df
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        raise

# clean_data
"""
    Clean the DataFrame before upload.
    Steps:
        - Remove rows with missing values.
        - (Optional) Rename columns or cast types.
    Parameters:
        data: pd.DataFrame (Raw DataFrame)
    Returns:
        cleaned: pd.DataFrame (Cleaned DataFrame)
    """
def clean_data(data):
    logging.info("Cleaning data: removing rows with missing values")
    cleaned = data.dropna()

    logging.info(f"Remaining rows after cleaning: {len(cleaned)}")
    return cleaned

# load_data
"""
    Upload the DataFrame to MySQL using SQLAlchemy (bulk upload).
    Parameters:
        data: pd.DataFrame (Cleaned DataFrame to upload)
        table: str (Destination table name (always 'mock'))
    """
def load_data(data, table):
    logging.info("Preparing database connection")

    # Read environment variables
    db_host = os.getenv("DBHOST")
    db_name = os.getenv("DBNAME")
    db_user = os.getenv("DBUSER")
    db_pass = os.getenv("DBPASS")

    if not all([db_host, db_name, db_user, db_pass]):
        raise EnvironmentError("Missing one or more DB environment variables")

    # Create SQLAlchemy engine
    engine_url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = create_engine(engine_url)

    logging.info(f"Uploading data to table '{table}'")

    try:
        # if_exists="replace" ensures table exists and is overwritten
        data.to_sql(table, engine, if_exists="replace", index=False)
        logging.info("Upload complete")
    except Exception as e:
        logging.error(f"Failed to upload data: {e}")
        raise

# main
"""
    Main ETL workflow:
    - Read CSV
    - Clean DataFrame
    - Load into MySQL
    """
def main():
    logging.info("Starting ETL process")

    filename = "MOCK_DATA.csv"
    table = "mock"

    df = read_data(filename)
    cleaned = clean_data(df)
    load_data(cleaned, table)

    logging.info("ETL process completed successfully")


# Script entry point
if __name__ == "__main__":
    main()
