# Use an official Python runtime as a parent image
FROM python:3.6.2

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run Installation commands
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip install -U pip

# Install any needed packages specified in requirements.txt
 RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
 ENTRYPOINT ["python3", "run.py"]
