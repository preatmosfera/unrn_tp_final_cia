import sys
from agent.agent_graph import app # Importamos la 'app' compilada

def chat_loop():
    """
    Inicia un bucle de chat interactivo con el agente de cocina.
    """
    print("\n==============================================")
    print("🤖 Hola! Soy tu Asistente de Cocina RAG.")
    print("     Escribe el nombre de una receta para revisarla.")
    print("     Escribe 'salir' o presiona Ctrl+C para terminar.")
    print("==============================================")

    try:
        while True:

            recipe_name = input("🍳 Tú: ")

            if recipe_name.lower().strip() == 'salir':
                break
            if not recipe_name.strip():
                continue

            print(f"🤖 Agente: Entendido. Revisando '{recipe_name}'...")

            inputs = {"recipe_name": recipe_name}

            # final_state = {}
            for event in app.stream(inputs):
                # event es un diccionario como: {'node_name': state_update}
                node_name = list(event.keys())[0]
                node_output = event[node_name]

                if node_name == "analyze":
                    print(f"Agente (Decisión): {node_output['decision']}")

                if node_name == "save_report":
                    print("Agente (Guardado): ¡Informe guardado en Notion!")

            print("----------------------------------------------")

    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\nHa ocurrido un error: {e}")
        
    print("\n🤖 ¡Hasta luego!")

if __name__ == "__main__":
    chat_loop()
