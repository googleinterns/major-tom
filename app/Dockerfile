# Step 0 - Build
FROM tiangolo/node-frontend:10 AS build

# If REACT_APP_HTTP_URI variable is not passed as argument during image build,
# it defaults to "http://localhost:4000"
# i.e. docker build --build-arg REACT_APP_HTTP_URI=${ANY REACT_APP_HTTP_URI} ...
ARG REACT_APP_HTTP_URI="http://localhost:4000"
ENV REACT_APP_HTTP_URI=$REACT_APP_HTTP_URI

WORKDIR /app
COPY package*.json /app/
RUN yarn install
COPY ./ /app/
RUN yarn build

# Step 1 - Nginx startup
FROM nginx:1.15

COPY --from=build /app/build/ /usr/share/nginx/html
COPY --from=build /nginx.conf /etc/nginx/conf.d/default.conf