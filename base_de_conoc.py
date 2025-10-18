from langchain_core.documents import Document

def load_documents() -> list[Document]:
    """Carga documentos que representan el inventario actual y un conjunto de recetas."""
    
    # ------------------------
    # 🧊 INVENTARIO ACTUAL
    # ------------------------
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

    # ------------------------
    # 🍝 RECETAS DISPONIBLES
    # ------------------------
    recetas_text = """
    Recetas disponibles:

    1. Omelette de Queso y Tomate:
       Ingredientes: huevos, queso rallado, tomate, sal, pimienta, manteca.
       Tiempo de preparación: 10 minutos.
       Nivel: fácil.
       Observación: todos los ingredientes están disponibles.

    2. Salmón a la Plancha con Arroz:
       Ingredientes: salmón, arroz, manteca, aceite de oliva, sal.
       Tiempo de preparación: 25 minutos.
       Nivel: medio.
       Observación: todos los ingredientes están disponibles.

    3. Lentejas Guisadas:
       Ingredientes: lentejas, cebolla, zanahoria, morrón, ajo, aceite de oliva, sal, pimienta.
       Tiempo de preparación: 40 minutos.
       Nivel: medio.
       Observación: faltan zanahoria, morrón y ajo.

    4. Brownies de Chocolate:
       Ingredientes: harina, huevos, azúcar, manteca, chocolate, nueces.
       Tiempo de preparación: 30 minutos.
       Nivel: medio.
       Observación: faltan nueces.
    """
    recetas_doc = Document(
        page_content=recetas_text,
        metadata={"source": "recetas.txt"}
    )

    # ------------------------
    # 📦 RETORNO FINAL
    # ------------------------
    docs = [inventario_doc, recetas_doc]
    print(f"📦 Cargados {len(docs)} documentos: inventario y recetas.")
    return docs
