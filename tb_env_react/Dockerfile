FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 3000
ENV REACT_APP_BACKEND_URL=http://backend:5000

CMD ["npm", "run", "start"]
