import os
from dotenv import load_dotenv
import openai
import psycopg2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()

# Test OpenAI API Key
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Completion.create(engine="text-davinci-002", prompt="Test", max_tokens=5)
    print("OpenAI API key is working.")
except Exception as e:
    print(f"Error with OpenAI API key: {e}")

# Test Google API Key and Programmable Search ID
try:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_programmable_search_id = os.getenv("GOOGLE_PROGRAMMABLE_SEARCH_ID")

    service = build("customsearch", "v1", developerKey=google_api_key)
    response = service.cse().list(q="test", cx=google_programmable_search_id).execute()

    if int(response["searchInformation"]["totalResults"]) > 0:
        print("Google API key and Programmable Search ID are working.")
except Exception as e:
    print(f"Error with Google API key or Programmable Search ID: {e}")

# Test PostgreSQL credentials
try:
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT")
    postgres_db = os.getenv("POSTGRES_DB")

    conn = psycopg2.connect(
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
    )
    conn.close()
    print("PostgreSQL credentials are working.")
except Exception as e:
    print(f"Error with PostgreSQL credentials: {e}")