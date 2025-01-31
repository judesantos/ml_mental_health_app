# Use an official Python base image with Python 3.12
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering stdout and stdin
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y libpq-dev python3-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy the rest of the application code into the container
COPY . .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["python3", "app/app_main.py"]