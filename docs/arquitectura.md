## docs/arquitectura.md

```md
# Arquitectura del ChatBot Hospitalario

## Componentes
- Frontend React: Interfaz tipo chat para usuarios.
- Backend FastAPI: Controla flujo conversacional y API.
- MySQL: Persistencia de citas.
- Ollama Llama3: Inteligencia artificial local.

## Flujo
Usuario -> Frontend -> Backend -> DB
                     -> IA local (Ollama)
