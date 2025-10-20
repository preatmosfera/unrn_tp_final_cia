from langgraph.graph import StateGraph, END
from agent.agent_state import CookingAgentState
# Nodos del agente
from agent.agent_nodes import nodes


def create_agent_graph():
    """
    Función constructora para crear y compilar el grafo del agente.
    """
    print("\n Construyendo el grafo del agente...")

    # Crear una instancia del grafo
    workflow = StateGraph(CookingAgentState)

    # Añadir nodos
    workflow.add_node("fetch_recipe", nodes.get_required_ingredients)
    workflow.add_node("check_inventory", nodes.get_available_inventory)
    workflow.add_node("analyze", nodes.analyze_and_decide)
    workflow.add_node("generate_report",nodes.generate_notion_report)
    workflow.add_node("save_report", nodes.save_to_notion)

    # Definir flujo
    workflow.set_entry_point("fetch_recipe")
    workflow.add_edge("fetch_recipe", "check_inventory")
    workflow.add_edge("check_inventory", "analyze")
    workflow.add_edge("analyze", "generate_report")
    workflow.add_edge("generate_report", "save_report")
    workflow.add_edge("save_report", END)

    # Compilar el grafo en una aplicación "app"
    app = workflow.compile()
    print("Grafo compilado y listo.")
    return app

app = create_agent_graph()
