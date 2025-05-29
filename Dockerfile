# Use an official Python runtime as a parent image
# python:3.10-slim-buster is a good choice for smaller image size
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# This step is done early to leverage Docker's build cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container at /app
COPY . .

# If predict.py were a web service (e.g., using FastAPI, Flask), we will need to expose a port.
# For a command-line script, it's not strictly necessary unless it is run via an API later.
# EXPOSE 8000 # Example for a web service

# Define the command to run the application
# This is how the container will execute your script when it starts
# We use 'python3 (we'll run this on Linux) -u' for unbuffered output, useful in logs.
CMD ["python3", "-u", "predict.py"]

# Optional: Add metadata to the image
LABEL maintainer="Your Name"
LABEL version="1.0"
LABEL description="NYC Yellow Taxi Demand Forecasting Prediction Service"
