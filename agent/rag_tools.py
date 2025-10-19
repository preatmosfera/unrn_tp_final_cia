import os
from dotenv import load_dotenv

# Componentes específicos de Google
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Importar tus módulos locales
from knowledge import load_documents
from mock_notion_connector import NotionConnector


class RagTools:
    """
    """
    def __init__(self):
        print("Inicializando RagTools...")
        load_dotenv()

        if not os.getenv("GEMINI_API_KEY"):
            raise EnvironmentError("GEMINI_API_KEY no encontrada en el archivo .env")
        os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


        self.retriever = self._build_retriever()


        self.recipe_chain = self._build_recipe_chain()
        self.inventory_chain = self._build_inventory_chain()

        # Herramienta de Notion
        self.notion_db_id = os.getenv("NOTION_DATABASE_ID")
        self.notion_tool = NotionConnector()
        print("RagTools listo.")


    def _build_retriever(self):
        """Función privada para construir el retriever RAG."""
        docs = load_documents()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        all_splits = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(all_splits, self.embeddings)
        print("Base de Conocimiento RAG lista (FAISS).")
        return vectorstore.as_retriever(search_kwargs={"k": 2})
    
    def _build_recipe_chain(self):
        """Método privado para construir la cadena de extracción de recetas."""
        recipe_prompt = ChatPromptTemplate.from_template(
            "Eres un asistente de cocina. Basado en el siguiente contexto de un libro de recetas, "
            "extrae la lista de ingredientes para la receta: '{recipe_name}'.\n\n"
            "Contexto:\n{context}\n\n"
            "Responde SÓLO con los nombres de los ingredientes (ej: 'harina', 'huevos', 'azúcar'), "
            "separados por comas. Si la receta no se encuentra, responde 'RECETA_NO_ENCONTRADA'."
        )
        return create_stuff_documents_chain(self.llm, recipe_prompt) | StrOutputParser()

    def _build_inventory_chain(self):
        """Método privado para construir la cadena de extracción de inventario."""
        inventory_prompt = ChatPromptTemplate.from_template(
            "Eres un asistente de inventario. Basado en el siguiente contexto, "
            "extrae TODOS los items de comida disponibles en la heladera y la despensa.\n\n"
            "Contexto:\n{context}\n\n"
            "Responde SÓLO con los nombres de los items (ej: 'huevos', 'leche', 'queso rallado'), "
            "separados por comas."
        )
        return create_stuff_documents_chain(self.llm, inventory_prompt) | StrOutputParser()

tools = RagTools()