FROM node:12-slim

# Create and change to the app directory.
WORKDIR /server

# A wildcard is used to ensure both package.json AND package-lock.json are copied.
# Copying this separately prevents re-running npm install on every code change.
COPY package*.json ./

RUN yarn install --production

# Copy local code to the container image.
COPY . ./

CMD [ "yarn", "start" ]