FROM node:10

# If PORT variable is not passed as argument during image build, it defaults to 4000
# i.e. docker build --build-arg PORT=${ANY PORT} ...
ENV PORT=4000
ENV SEARCH_ENDPOINT="http://localhost:8080"
ENV DATABASE_ENDPOINT="http://localhost:8082"

WORKDIR /app
COPY . .
RUN yarn install --production

CMD ["yarn", "start"]