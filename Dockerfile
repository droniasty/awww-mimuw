# Use an official Python runtime as a parent image
FROM python:3.8.0-slim

# Install GCC and other system dependencies
RUN apt-get update
RUN apt-get -y install gcc
# install sdcc C compiler
RUN apt-get -y install sdcc


#set environment variables
ENV PYTHONUNBUFFERED 1 
ENV DJANGO_SETTINGS_MODULE awwwlab.settings

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run Django's development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
