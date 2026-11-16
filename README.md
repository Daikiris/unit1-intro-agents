# Hugging Face AI Agents Course - Unidad 1

- **Curso:** https://huggingface.co/learn/agents-course
- **Estudiante:** Jeison Bonivento Garrido
- **Username de Hugging Face:** daikiris
- **Certificado buscado:** Fundamentals

## Contenido

| Carpeta | Contenido |
|---|---|
| `unit1/CursodeAgentes.ipynb` | Notebook Dummy Agent Library de la Unidad 1, ejecutado con las salidas visibles |
| `src/`, `first_agent/` | Scripts propios de práctica (extra) |

## Observaciones

- La API de Hugging Face (Inference Providers) pedía créditos de pago (error 402),
  así que usé la API gratuita de Groq (compatible con OpenAI) con el modelo `openai/gpt-oss-120b`.
- Cambios respecto al notebook original: sustituí `InferenceClient` por el cliente de `openai`
  apuntando a Groq, añadí `model=MODEL` en cada llamada, quité el parámetro `extra_body`
  específico de Kimi y, por ser un modelo de razonamiento, subí `max_tokens` y usé
  `reasoning_effort="low"`.
- - Aprendí que el agente debe esperar la respuesta real de la herramienta antes de continuar, para evitar inventar información y dar respuestas confiables. Con `stop=["Observation:"]` el modelo se detiene tras pedir la acción, el agente la ejecuta y se inserta la Observation real.
- Tuve dificultades con la versión de Python, la compatibilidad del modelo y el error 402 relacionado con el pago, lo que impidió ejecutar correctamente algunas partes.

## Fechas

El trabajo se hizo el 15 de noviembre de 2026; las fechas de los commits son las reales.