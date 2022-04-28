"""API configurations"""
import os


def get_postgres_uri():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", 54321 if host == "localhost" else 5432)
    database = os.environ.get("POSTGRES_NAME", "allocation")
    user = os.environ.get("POSTGRES_USER", "allocation")
    password = os.environ.get("POSTGRES_PASSWORD", "allocation")

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT", 5005 if host == "localhost" else 80)

    return f"http://{host}:{port}"
