# Step 0 - Build
FROM node:10 AS build

# If REACT_APP_HTTP_URI variable is not passed as argument during image build,
# it defaults to "http://localhost:4000"
# i.e. docker build --build-arg REACT_APP_HTTP_URI=${ANY REACT_APP_HTTP_URI} ...
ARG REACT_APP_HTTP_URI="http://localhost:4000"
ENV REACT_APP_HTTP_URI=$REACT_APP_HTTP_URI

COPY . .
RUN yarn install --production
RUN yarn build

# Step 1 - Nginx startup
FROM nginx:1.15

COPY --from=build /build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]