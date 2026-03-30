FROM node:20-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./

RUN npm run build

# Servir con nginx (más ligero)
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
