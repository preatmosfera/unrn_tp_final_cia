import os
import sys
from dotenv import load_dotenv

# Importamos la clase Conector
from notion_connector import NotionConnector

def setup_database():
    """
    Script de configuración único para crear la base de datos 
    requerida en Notion.
    """
    print("Iniciando script de creación de base de datos...")

    load_dotenv()

    db_name = "Log de Cocina"

    try:
        connector = NotionConnector()

        connector.create_database(db_name)

    except Exception as e:
        print(f"Ocurrió un error general durante la configuración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
