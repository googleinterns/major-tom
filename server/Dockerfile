FROM node:10

ENV PORT=4000
ENV SEARCH_ENDPOINT="http://host.docker.internal:8080"
ENV DATABASE_ENDPOINT="http://host.docker.internal:8082"
ENV REDIS_IP="host.docker.internal"
ENV REDIS_PORT=6379

WORKDIR /app
COPY . .
RUN yarn install --production

CMD ["yarn", "start"]