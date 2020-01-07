# Pull base image
FROM python:3.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

# Set work directory
WORKDIR /app
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt