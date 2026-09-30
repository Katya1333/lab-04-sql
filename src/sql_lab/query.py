#!/usr/bin/env python3

"""
query.py

Retrieve and analyze data from the mock table in enu4nc_mock
database. Uses parameterized queries, environment variables for credentials,
and logging for status reporting.

Functions:
    get_data_by_group(value): return rows where the group column equals value.
    plot_counts(groupby): count rows grouped by a column and print or plot results.
"""

import os
import logging
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Database connection
"""
    Create and return a MySQL database connection using environment variables.
    Required environment variables:
    - DBHOST
    - DBUSER
    - DBPASS
    - DBNAME
    """
def get_db_connection():
    logging.info("Opening database connection")

    db_host = os.getenv("DBHOST")
    db_user = os.getenv("DBUSER")
    db_pass = os.getenv("DBPASS")
    db_name = os.getenv("DBNAME")

    if not all([db_host, db_user, db_pass, db_name]):
        raise EnvironmentError("Missing one or more DB environment variables")

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        logging.info("Database connection established")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise


# get_data_by_group
"""
    Return rows from the mock table where the `group` column equals value.
    Parameters:
        value: str (the group value to filter on)
    Returns
        pd.DataFrame (a DataFrame containing the filtered rows)
    """
def get_data_by_group(value):
    logging.info(f"Running SELECT for group = {value}")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # GROUP is a reserved word → must use backticks
        query = "SELECT * FROM mock WHERE `group` = %s;"
        cur.execute(query, (value,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]

        logging.info(f"Retrieved {len(rows)} rows")
        return pd.DataFrame(rows, columns=cols)

    except mysql.connector.Error as e:
        logging.error(f"MySQL Error: {e}")
        return None

    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed")


# plot_counts
"""
    Count rows grouped by a column and show a bar chart.
    Parameters:
        groupby: str (column name to group by)
    Returns:
        df: pd.DataFrame (a DataFrame containing counts per distinct value)
    """
def plot_counts(groupby):
    logging.info(f"Running GROUP BY query on column: {groupby}")

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Safe dynamic column name insertion using backticks
        query = f"""
            SELECT `{groupby}`, COUNT(*) AS count
            FROM mock
            GROUP BY `{groupby}`
            ORDER BY count DESC;
        """

        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[groupby, "count"])

        logging.info("Group-by query completed")

        # Plot results
        plt.figure(figsize=(8, 5))
        plt.bar(df[groupby], df["count"])
        plt.xlabel(groupby)
        plt.ylabel("Count")
        plt.title(f"Counts grouped by {groupby}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return df

    except mysql.connector.Error as e:
        logging.error(f"MySQL Error: {e}")
        return None

    finally:
        cur.close()
        conn.close()
        logging.info("Database connection closed")


# main
"""Demonstrate the query functions."""
def main():
    print("=== get_data_by_group('A') ===")
    df = get_data_by_group("A")
    print(df)

    print("\n=== plot_counts('group') ===")
    counts = plot_counts("group")
    print(counts)


# Script entry point
if __name__ == "__main__":
    main()