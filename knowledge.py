import json
from pathlib import Path
from langchain_core.documents import Document

def load_documents() -> list[Document]:
   """Carga documentos que representan el inventario actual y un conjunto de recetas."""

   inventario_text = """
   Inventario del hogar (actualizado al 18/10/2025):

   Heladera:
   - 4 huevos
   - 1 litro de leche
   - 200g de queso rallado
   - 2 tomates
   - 1 cebolla
   - 100g de manteca
   - 1 trozo de salmón

   Despensa:
   - 1 kg de harina
   - 500g de arroz
   - 1 lata de lentejas
   - Aceite de oliva
   - Sal, pimienta, azúcar
   - 1 paquete de fideos
   - 1 tableta de chocolate
   """
   inventario_doc = Document(
      page_content=inventario_text,
      metadata={"source": "inventario.txt"}
   )

   json_path = Path("recetas_argentinas.json")
   
   if not json_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {json_path}, asegurate de crearlo en el proyecto.")
   recetas_data = {}
   with open(json_path, "r", encoding="utf-8") as f:
        recetas_data = json.load(f)
   
   recetas_doc = Document(
      page_content=json.dumps(recetas_data, ensure_ascii=False, indent=2),
      metadata={"source": "recetas_argentinas.json"}
   )

   docs = [inventario_doc, recetas_doc]
   print(f"Cargados {len(docs)} documentos: inventario y recetas.")
   return docs
