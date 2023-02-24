# Use a lightweight Python image
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the necessary files into the container
COPY . .

COPY requirements.txt .
# Install dependencies
RUN pip install -r requirements.txt


# Specify the command to run by default
CMD [ "python", "./thairath_crawler.py" ]