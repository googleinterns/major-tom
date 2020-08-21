# Set base image, the slim one allows us to have a small build size
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /code

ENV PORT 8082
ENV KEYWORDS_SERVICE http://keywords.default.major-tom.googleinterns.app

# Copy dependencies file to container
COPY requirements.txt .

# Install dependencies using PIP
RUN pip install -r requirements.txt &&\
apt-get update &&\
apt-get install -y curl

# Copy Files to container
COPY . .

HEALTHCHECK CMD curl -X GET localhost:8082/articles/100

# Run the Flask App
CMD [ "python", "app.py" ]