FROM node:10

# If PORT variable is not passed as argument during image build, it defaults to 4000
# i.e. docker build --build-arg PORT=${ANY PORT} ...
ARG PORT=4000
ENV PORT=${PORT}

WORKDIR /app
COPY package*.json ./
RUN yarn install --production
COPY . .

CMD ["yarn", "start"]