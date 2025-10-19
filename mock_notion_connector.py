import os
from dotenv import load_dotenv

load_dotenv()

class NotionConnector:
    """
    Un MOCK (simulador) del NotionConnector del usuario.
    Simula la escritura en la API de Notion.
    """
    def __init__(self):
        # En un conector real, aquí se inicializaría el cliente de Notion
        # con un token de autenticación.
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        if not self.database_id:
            print("⚠️ Advertencia: NOTION_DATABASE_ID no está configurada en .env")
            self.database_id = "db_id_simulada"
        
        print(f"🔌 MockNotionConnector inicializado. (Escribirá en DB_ID: {self.database_id})")

    def add_entry(self, database_id, name, comentario, fecha):
        """
        Simula agregar una entrada (página) a una base de datos de Notion.
        Imprime en consola lo que recibiría.
        """
        if database_id != self.database_id:
            print(f"Error: Se intentó escribir en la DB incorrecta: {database_id}")
            return None

        print("\n--- ↗️ SIMULANDO LLAMADA A API DE NOTION ---")
        print(f"  TARGET DB: {database_id}")
        print(f"  DATOS ENVIADOS:")
        print(f"    - Título (name): {name}")
        print(f"    - Comentario (propiedad): {comentario}")
        print(f"    - Fecha (propiedad): {fecha}")
        print("--- ✅ ESCRITURA SIMULADA EXITOSA ---")
        
        # Devuelve un objeto simulado de página de Notion
        return {
            "object": "page",
            "id": "mock_page_b5a5-4b3c-..."
        }