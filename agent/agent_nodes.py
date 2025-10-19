import re
from datetime import datetime

# Importar el estado y las herramientas
from agent.agent_state import CookingAgentState
from agent.rag_tools import tools

def _normalize_list(items_str: str) -> list[str]:
    """
    Función helper para limpiar la salida del LLM.
    Traduce de string separado por comas a una lista de Python.
    """
    items_str = re.sub(r'(\d+\s*k?g?|\d+\s*|\-|\*)', '', items_str.lower())
    return [item.strip() for item in items_str.split(',') if item.strip()]

# Lógica de Nodos
class CookingAgentNodes:
    def __init__(self, tools: "RagTools"):
        # Inyección de dependencias: para guardar las herramientas
        self.tools = tools


    def get_required_ingredients(self, state: CookingAgentState) -> CookingAgentState:
        """
        Nodo 1: Consulta el RAG para saber qué ingredientes necesita la receta.
        """
        print(f"\n[Nodo 1: get_required_ingredients]")
        recipe_name = state['recipe_name']
        
        context_docs = self.tools.retriever.invoke(recipe_name)
        
        print(f"-> Consultando RAG-LLM por ingredientes para: '{recipe_name}'")
        ingredients_str = self.tools.recipe_chain.invoke({
            "context": context_docs,
            "recipe_name": recipe_name
        })
        
        if "RECETA_NO_ENCONTRADA" in ingredients_str:
            print("-> ERROR: Receta no encontrada.")
            ingredients_list = ["RECETA_NO_ENCONTRADA"]
        else:
            ingredients_list = _normalize_list(ingredients_str)
            
        print(f"-> Ingredientes requeridos: {ingredients_list}")
        state['required_ingredients'] = ingredients_list
        return state

    def get_available_inventory(self, state: CookingAgentState) -> CookingAgentState:
        """
        Nodo 2: Consulta el RAG para saber qué ingredientes tenemos en el inventario.
        """
        print(f"\n[Nodo 2: get_available_inventory]")

        if "RECETA_NO_ENCONTRADA" in state['required_ingredients']:
            print("-> Saltando nodo, receta no encontrada.")
            state['available_ingredients'] = []
            return state

        context_docs = self.tools.retriever.invoke("Inventario del hogar heladera y despensa")

        print(f"-> Consultando RAG-LLM por inventario disponible...")
        inventory_str = self.tools.inventory_chain.invoke({
            "context": context_docs,
        })

        inventory_list = _normalize_list(inventory_str)
        print(f"-> Ingredientes disponibles: {inventory_list}")
        state['available_ingredients'] = inventory_list
        return state

    def analyze_and_decide(self, state: CookingAgentState) -> CookingAgentState:
        """
        Nodo 3: Compara las listas y toma una decisión.
        """
        print(f"\n[Nodo 3: analyze_and_decide]")

        if "RECETA_NO_ENCONTRADA" in state['required_ingredients']:
            state['decision'] = f"No se pudo procesar. Receta '{state['recipe_name']}' no encontrada en la base de conocimiento."
            state['missing_ingredients'] = []
            return state

        required_set = set(state['required_ingredients'])
        available_set = set(state['available_ingredients'])

        missing = []
        for req_item in required_set:
            is_available = False
            for avail_item in available_set:
                if req_item in avail_item: # ej: "sal" está en "sal, pimienta"
                    is_available = True
                    break
            if not is_available:
                missing.append(req_item)

        state['missing_ingredients'] = missing

        if not missing:
            decision = f"✅ ¡Todo listo! Tienes los {len(required_set)} ingredientes para hacer {state['recipe_name']}."
        else:
            decision = f"❌ No se puede cocinar. Faltan {len(missing)} ingredientes: {', '.join(missing)}."

        print(f"-> Decisión: {decision}")
        state['decision'] = decision
        return state

    def generate_notion_report(self, state: CookingAgentState) -> CookingAgentState:
        """
        Nodo 4: Formatea la decisión para la API de Notion.
        """
        print(f"\n[Nodo 4: generate_notion_report]")

        report_data = {
            "name": f"Informe de Cocina: {state['recipe_name']}",
            "comentario": state['decision'],
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }

        state['notion_report_data'] = report_data
        print(f"-> Informe estructurado para Notion: {report_data}")
        return state

    def save_to_notion(self, state: CookingAgentState) -> CookingAgentState:
        """
        Nodo 5: Llama a la herramienta externa (Notion) para la persistencia.
        """
        print(f"\n[Nodo 5: save_to_notion]")
        report_data = state['notion_report_data']

        try:
            self.tools.notion_tool.add_entry(
                database_id=self.tools.notion_db_id,
                name=report_data['name'],
                comentario=report_data['comentario'],
                fecha=report_data['fecha']
            )
            print("-> Persistencia en Notion completada.")
        except Exception as e:
            print(f"-> ERROR al guardar en Notion: {e}")

        return state

nodes = CookingAgentNodes(tools)