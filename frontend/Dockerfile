FROM mhart/alpine-node:11 AS builder
ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV development
WORKDIR /app
COPY . /app
RUN npm install

CMD ["npm", "start"]

