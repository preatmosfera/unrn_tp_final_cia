from notion_connector import NotionConnector

if __name__ == "__main__":
    connector = NotionConnector()

    # Crear una base
    db_id = connector.create_database("Base creada desde clase")

    # Agregar un registro dentro de la base
    connector.add_entry(
        database_id=db_id,
        name="Primera entrada",
        comentario="Creada automáticamente desde la clase NotionConnector",
        fecha="2025-10-18",
    )




