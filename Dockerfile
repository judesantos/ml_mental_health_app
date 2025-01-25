# Use an official Python base image with Python 3.12
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering stdout and stdin
ENV PYTHONUNBUFFERED 1

# Install required system dependencies and Miniconda
RUN set -eux apt-get update
RUN set -eux apt-get install -y --no-install-recommends wget ca-certificates
RUN set -eux wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
RUN set -eux bash /tmp/miniconda.sh -b -p /opt/conda
RUN set -eux rm -rf /tmp/miniconda.sh
RUN set -eux apt-get clean
RUN set -eux rm -rf /var/lib/apt/lists/*

# Update PATH to include Conda binaries
ENV PATH="/opt/conda/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Copy the environment.yml file into the container
COPY environment.yml .

# Create the Conda environment using the environment.yml file
RUN set -eux conda env create -f environment.yml

# Activate the Conda environment
ENV CONDA_DEFAULT_ENV=base
ENV PATH="/opt/conda/envs/${CONDA_DEFAULT_ENV}/bin:$PATH"

# Expose the Flask default port
EXPOSE 5000

# Start the Flask service
CMD ["python3", "app/app_main.py"]

