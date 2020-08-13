# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
ENV KEYWORDS_ENDPOINT="http://localhost:8081"
ENV PORT=8080
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup.
# https://github.com/GoogleCloudPlatform/functions-framework-python
CMD exec functions-framework --target=search_service --port=$PORT
