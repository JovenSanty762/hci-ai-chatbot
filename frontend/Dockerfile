# frontend/Dockerfile

FROM node:20-alpine AS builder

WORKDIR /app

# 1. Copiar solo dependencias primero (mejor caché)
COPY package*.json ./

RUN npm ci --frozen-lockfile

# 2. Copiar TODO el código fuente (index.html debe estar aquí)
COPY . .

# 3. Construir la aplicación
RUN npm run build

# ==================== Etapa de producción ====================
FROM nginx:alpine

# Copiar los archivos estáticos generados por Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# Opcional: Copiar configuración personalizada de nginx (si la tienes)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
