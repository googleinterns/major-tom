# Step 0 - Build
FROM node:10 AS build

# If REACT_APP_HTTP_URI variable is not passed as argument during image build,
# it defaults to "http://localhost:4000"
# i.e. docker build --build-arg REACT_APP_HTTP_URI=${ANY REACT_APP_HTTP_URI} ...
ARG REACT_APP_HTTP_URI="/graphql"
ENV REACT_APP_HTTP_URI=$REACT_APP_HTTP_URI

COPY . .
RUN yarn global add serve
RUN yarn install --production
RUN yarn build

ENV PORT=8080
CMD ["serve", "-s", "-l", "tcp://0.0.0.0:$PORT", "build"]