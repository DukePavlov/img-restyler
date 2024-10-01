# Use an official Python runtime as a parent image
FROM python:3.9.7-slim

# Install required packages for PyQt5 GUI and X11 forwarding
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the entrypoint
CMD ["python", "gui/app.py"]