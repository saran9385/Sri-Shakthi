# Use Python 3.11.11 base image
FROM python:3.11.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Render port
EXPOSE 10000

# Start your Flask app with gunicorn using your command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "app:app"]
