# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT=8081
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup.
CMD exec functions-framework --target=get_keywords_service --port=$PORT
