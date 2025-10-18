from notion_client import Client
import os
from dotenv import load_dotenv

class NotionConnector:
    """Conector para interactuar con la API de Notion.
    
    Permite crear bases de datos, páginas y registrar información
    dentro de una página padre especificada en el archivo .env.
    """

    def __init__(self):
        load_dotenv()
        self.token = os.getenv("NOTION_TOKEN")
        self.parent_id = os.getenv("NOTION_PARENT_ID")

        if not self.token:
            raise ValueError("❌ Falta NOTION_TOKEN en el archivo .env")
        if not self.parent_id:
            raise ValueError("❌ Falta NOTION_PARENT_ID en el archivo .env")

        self.notion = Client(auth=self.token)

    def create_database(self, title: str):
        """Crea una base de datos dentro de la página especificada en el .env."""
        db = self.notion.databases.create(
            parent={"type": "page_id", "page_id": self.parent_id},
            title=[{"type": "text", "text": {"content": title}}],
            properties={
                "Name": {"title": {}},
                "Comentario": {"rich_text": {}},
                "Fecha": {"date": {}},
            },
        )

        print("✅ Base creada correctamente:")
        print(f"- Título: {db['title'][0]['plain_text']}")
        print(f"- ID: {db['id']}")
        print(f"- URL: {db['url']}")
        return db["id"]

    def add_entry(self, database_id: str, name: str, comentario: str, fecha: str = None):
        """Agrega una nueva fila (página) a una base de datos existente."""
        properties = {
            "Name": {"title": [{"text": {"content": name}}]},
            "Comentario": {"rich_text": [{"text": {"content": comentario}}]},
        }
        if fecha:
            properties["Fecha"] = {"date": {"start": fecha}}

        page = self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
        )

        print("📝 Registro agregado:")
        print(f"- Nombre: {name}")
        print(f"- URL: {page['url']}")
        return page["id"]
