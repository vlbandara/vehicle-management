# Use the official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for the API key
ENV GOOGLE_API_KEY=AIzaSyDEZIEEnGFJ2OoKsNCTIo0w9zrBgR1Dtfk

# Copy project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment variable for Streamlit
ENV STREAMLIT_PORT=8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
