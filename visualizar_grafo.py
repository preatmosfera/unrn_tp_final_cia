"""
Script utilitario para visualizar el grafo del agente de cocina (LangGraph)
sin inicializar el entorno RAG ni las dependencias externas (Google, Notion, etc.).

Uso:
    INIT_RAG_TOOLS=false python3 visualizar_grafo.py
"""

import os
from pathlib import Path
from IPython.display import Image, display
from agent.agent_graph import create_agent_graph

# --- Desactivar inicialización pesada ---
os.environ["INIT_RAG_TOOLS"] = "false"

# --- Crear el grafo ---
app = create_agent_graph()

# --- Generar la imagen ---
print("\n🧩 Renderizando diagrama del grafo LangGraph...\n")
image_bytes = app.get_graph().draw_mermaid_png()

# --- Guardar en /docs/grafo.png ---
docs_dir = Path(__file__).parent / "docs"
docs_dir.mkdir(exist_ok=True)
output_path = docs_dir / "grafo.png"

with open(output_path, "wb") as f:
    f.write(image_bytes)

# --- Mostrar en consola (si hay entorno gráfico) ---
try:
    display(Image(image_bytes))
except Exception:
    pass

print(f"✅ Diagrama guardado correctamente en: {output_path}\n")
