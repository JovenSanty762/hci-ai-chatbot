# hci-ai-chatbot

Este proyecto implementa un chatbot hospitalario funcional con Inteligencia Artificial, diseñado para el agendamiento de citas médicas dentro de una red interna hospitalaria.

## Tecnologías
- Frontend: React + Vite
- Backend: FastAPI (Python)
- Base de datos: MySQL
- IA local: Ollama + Llama3
- Despliegue: Docker Compose

## Arquitectura
Usuario -> React Chat UI -> FastAPI -> MySQL
                           -> Ollama (Llama3)

## Requisitos
- Docker
- Docker Compose

## Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/USUARIO/hospital-ai-chatbot.git
cd hospital-ai-chatbot
