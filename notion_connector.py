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
            raise ValueError("Falta NOTION_TOKEN en el archivo .env")
        if not self.parent_id:
            raise ValueError("Falta NOTION_PARENT_ID en el archivo .env")

        try:
            self.notion = Client(auth=self.token)

        except Exception as e:
            print(f"ERROR al inicializar el cliente de Notion: {e}")
            raise

    def create_database(self, db_name: str = "Log de Cocina"):
        """Crea una base de datos dentro de la página especificada en el .env."""

        properties_schema={
            "Receta": {"title": {}},
            "Decisión": {"rich_text": {}},
            "Se puede cocinar?": {
                "select": {
                    "options": [
                        {"name": "Sí", "color": "green"},
                        {"name": "No", "color": "red"},
                    ]
                }
            },
            "Faltantes": {"rich_text": {}},
            "Fecha": {"date": {}}
            }
        try:
            response = self.notion.databases.create(
                parent={"page_id": self.parent_id},
                title=[{"type": "text", "text": {"content": db_name}}],
                properties=properties_schema
            )
            new_db_id = response['id']
            print("Base creada correctamente:")
            
            return new_db_id
        except Exception as e:
            print(f"ERROR al crear la base de datos: {e}")
            print("Causas probables: 1) El 'PARENT_PAGE_ID' es incorrecto. 2) La API key no tiene permisos.")
            return None

    def add_entry(self, database_id: str, receta_nombre: str, decision_texto: str, se_puede_cocinar: str, faltantes_lista: list, fecha: str):
        """Agrega una nueva fila (página) a una base de datos existente."""

        # lista de faltantes
        faltantes_str = ", ".join(faltantes_lista) if faltantes_lista else "Ninguno"

        new_page_properties = {
            "Receta": {
                "title": [{"text": {"content": receta_nombre}}]
            },
            "Decisión": {
                "rich_text": [{"text": {"content": decision_texto}}]
            },
            "Se puede cocinar?": {
                "select": {"name": se_puede_cocinar}
            },
            "Faltantes": {
                "rich_text": [{"text": {"content": faltantes_str}}]
            },
            "Fecha": {
                "date": {"start": fecha} # Formato YYYY-MM-DD
            }
        }

        print(f"Enviando entrada a Notion DB ID: {database_id}...")
        try:
            response = self.notion.pages.create(
                parent={"database_id": database_id},
                properties=new_page_properties
            )
            print(f"Nueva página creada en Notion con ID: {response['id']}")
            return response
        except Exception as e:
            print(f"ERROR al crear la página en Notion: {e}")
            return None
