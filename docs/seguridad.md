# Seguridad y Cumplimiento ISO 42001

**Controles implementados:**

- **7.2 Políticas**: Política de uso de IA documentada.
- **7.3 Roles y responsabilidades**: Human-in-the-Loop al final del chat.
- **8.2 Evaluación de riesgos**: Datos sensibles (documento, teléfono) con trazabilidad.
- **8.3 Controles de IA**: Llama3 corre 100% local (sin salida a internet).
- **9.1 Monitoreo**: Todos los mensajes guardados con timestamp.
- **10.3 Mejora continua**: Logs listos para auditoría.

**Riesgos identificados y mitigados**:
- Filtración de datos → Red interna + Docker networks
- Sesgos en Llama3 → Prompt engineering + supervisión humana
- Dependencia de IA → Siempre opción de transferir a humano
