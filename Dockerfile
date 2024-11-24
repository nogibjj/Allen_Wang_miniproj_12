# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
