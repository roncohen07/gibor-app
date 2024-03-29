# Use an official Python 3.11 slim-buster image as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /gibor-app

# Copy the current directory contents into the container at /app
COPY . /gibor-app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set permissions of the SQLite database file
RUN chmod 644 database.db

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=webapp.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
