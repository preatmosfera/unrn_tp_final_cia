from notion_client import Client
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def create_page(title: str, comment: str):
    """Crea una nueva página en la base de datos de Notion."""
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Comentario": {"rich_text": [{"text": {"content": comment}}]},
            "Fecha": {"date": {"start": datetime.now().isoformat()}}
        },
    )
    return response["url"]

