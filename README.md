# UNRN - Trabajo Práctico Final de agentes de Inteligencia Artificial

Este proyecto implementa un agente cognitivo desarrollado con **LangGraph**, 
capaz de registrar decisiones y reportes estructurados en **Notion** mediante su API.

Se implemento un agente capaz de analizar si cuenta con todos los ingredientes para decidir si es posible realizar una receta de cocina, en caso de que no sea posible reportar que ingredientes son los faltantes.
- ejemplo de una receta posible:
  >Tú: Omelette de Queso y Tomate
  
  >Agente: Entendido. Revisando 'Omelette de Queso y Tomate'
  
  >Decisión: ✅ ¡Todo listo! Tienes los 6 ingredientes para hacer Omelette de Queso y Tomate.
- ejemplo de receta sin un ingrediente:
  >Tú: Empanadas
  
  >Decisión: ❌ No se puede cocinar. Faltan 7 ingredientes: comino, pimentón, morrón, tapa de empanadas, carne picada, huevo duro, aceitunas.
  
- Ejemplo de receta no encontrada:
  >Tú: asado
  
  >Decisión: No se pudo procesar. Receta 'asado' no encontrada en la base de conocimiento.
  
## Componentes principales
- **LangGraph**: orquestación de nodos y transiciones.
- **Notion API**: persistencia externa.
- **LangSmith**: observabilidad y trazas.
- **Python 3.13**

## Objetivo
Demostrar la integración de un agente con memoria, reasoning y trazabilidad en un entorno modular.

## Instalación

1. Es necesario crear un entorno virtual para instalar el requirements.txt

    Se recomienda usar UV:

   - Instalar [uv](https://pypi.org/project/uv/)

        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```

   - Crear entorno virtual:

        ``` 
        uv venv --python 3.13
        ```

   - levantar el entorno virtual 

        ```bash
        source .venv/bin/activate
        ```
1. Instalar requirements.txt
   
   ```bash
   uv pip install -r requirements.txt
   ```

## Ejecución

Dentro del entorno virtual ejecutar:

```
python main.py
```