FROM node:10

ENV PORT=4000
ENV SEARCH_ENDPOINT="http://localhost:8080"
ENV DATABASE_ENDPOINT="http://localhost:8082"

WORKDIR /app
COPY . .
RUN yarn install --production

CMD ["yarn", "start"]