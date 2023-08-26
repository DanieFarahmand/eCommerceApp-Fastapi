# Use the official Python image as the base image
FROM python:3.10.6

# Set the working directory to /app
WORKDIR /app

# Copy the src directory from the host into the container at /app/src
COPY src /app/src

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 80 to the host machine
EXPOSE 80

# Command to run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
