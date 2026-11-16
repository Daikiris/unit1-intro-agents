# Notas de la Unidad 1

## Agente y LLM
Un agente combina un LLM (el cerebro) con herramientas que le permiten actuar.
El LLM solo recibe y produce texto; no ejecuta nada por si mismo.

## Mensajes y chat templates
- El modelo recibe un unico prompt: todos los mensajes se concatenan con los
  tokens especiales de ese modelo. No "recuerda": relee todo en cada turno.
- Roles: system, user, assistant.
- tokenizer.apply_chat_template aplica el formato correcto de cada modelo.
- Base model: predice el siguiente token. Instruct: afinado para seguir instrucciones.

## Tools
Funcion con objetivo claro: descripcion, callable, argumentos tipados, salida tipada.
El LLM no llama la tool: genera texto que representa la llamada; el agente la ejecuta.
Con type hints y docstrings se genera la descripcion automaticamente (@tool).
MCP: protocolo abierto que estandariza como se ofrecen tools a los LLM.

## Ciclo Thought - Action - Observation
Bucle while hasta cumplir el objetivo: pensar, actuar con una tool, observar el resultado.

## ReAct
CoT = razonamiento paso a paso sin tools. ReAct = CoT + acciones y observaciones intercaladas.

## Actions
Tipos de agente: JSON, Code, Function-calling.
Stop and parse: el LLM emite la accion, se detiene, un parser la extrae.
Code agents: mas expresivos, pero ejecutar codigo generado tiene riesgos.

## Observations
Señales del entorno (respuestas de API, errores, logs). El framework parsea,
ejecuta y añade el resultado como Observation.

## smolagents
Libreria ligera centrada en CodeAgent. Las tools con @tool necesitan type hints
y docstring con seccion Args.