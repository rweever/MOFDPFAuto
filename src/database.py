import os

import pyodbc
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """
    Create and return a connection to the SQL Server database
    using credentials stored in the local .env file.
    """

    driver = os.getenv("DB_DRIVER")
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    # Check that all required configuration values exist
    required_values = {
        "DB_DRIVER": driver,
        "DB_SERVER": server,
        "DB_DATABASE": database,
        "DB_USER": username,
        "DB_PASSWORD": password,
    }

    missing_values = [
        name
        for name, value in required_values.items()
        if not value
    ]

    if missing_values:
        raise ValueError(
            "Missing database configuration: "
            + ", ".join(missing_values)
        )

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    return pyodbc.connect(connection_string)