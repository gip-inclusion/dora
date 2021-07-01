FROM node:16-slim

RUN apt update
RUN apt install -y git

WORKDIR /app
COPY ./package.json package.json
RUN npm install

EXPOSE 3000
ENV HOST=0.0.0.0
ENV VITE_API_URL=http://localhost:8000
ENV VITE_INTERNAL_API_URL=http://host.docker.internal:8000
