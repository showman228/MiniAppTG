FROM node:22-alpine

WORKDIR /app

# Отдельным слоем — чтобы npm install не переигрывался на каждое изменение src/
COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
