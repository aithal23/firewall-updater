# Use an official Python runtime with cron, Alpine Linux version
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get -y install cron

# Copy the entry script
COPY entry.sh /usr/src/app/entry.sh

# Make the entry script executable
RUN chmod +x /usr/src/app/entry.sh


# Run entry.sh when the container launches
CMD ["/usr/src/app/entry.sh"]
