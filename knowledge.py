import json
from pathlib import Path
from langchain_core.documents import Document

def load_documents() -> list[Document]:
   """Carga documentos que representan el inventario actual y un conjunto de recetas."""

   inventario_text = """
   Inventario del hogar (actualizado al 18/10/2025):

¡Claro que sí\! Aquí tienes la lista ampliada, formateada tal como la original para tu agente:

```
Heladera:
   - 6 huevos
   - 1 litro de leche
   - 200g de queso rallado
   - 4 tomates
   - 2 cebolla
   - 150g de manteca
   - 1 trozo de salmón
   - 500g de carne
   - 1kg de papas
   - 2 zanahorias
   - 1 morrón
   - 1 cabeza de ajo
   - 1 atado de perejil
   - 200g de jamón cocido
   - 250g de queso cremoso
   - 1 pote de crema de leche
   - 1 paquete de masa para tarta

Despensa:
   - 1 kg de harina
   - 500g de arroz
   - 1 lata de lentejas
   - aceite de oliva
   - aceite
   - Sal, pimienta, azúcar
   - 1 paquete de fideos
   - 1 tableta de chocolate
   - 500g de pan rallado
   - 100g de nueces
   - 1 pote de dulce de leche
   - 1 pote de polvo de hornear
   - 1 frasco de esencia de vainilla
   - 1 botella de vinagre
   - orégano, laurel, comino, pimentón
   - 1 lata de tomate triturado
   - 1 paquete de levadura seca
```
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
