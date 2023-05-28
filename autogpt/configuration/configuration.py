import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Configuration:
    debug = os.environ.get("DEBUG") == "1"
    profile = os.environ.get("PROFILE") == "1"

    backend = os.environ.get("BACKEND")

    open_api_key = os.environ.get("OPENAI_API_KEY")

    scheduler_url = os.environ.get("SCHEDULER_URL")

    notion_token = os.environ.get("NOTION_TOKEN")
    notion_task_database_id = os.environ.get("NOTION_TASK_DATABASE_ID")
    notion_session_database_id = os.environ.get("NOTION_SESSION_DATABASE_ID")
    notion_interaction_database_id = os.environ.get("NOTION_INTERACTION_DATABASE_ID")
