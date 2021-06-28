FROM node:16-slim

RUN apt update
RUN apt install -y git

WORKDIR /app
COPY ./package.json package.json
RUN npm install

EXPOSE 3000
ENV HOST=0.0.0.0
