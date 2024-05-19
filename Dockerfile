FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Create a directory for logs (if needed)
RUN mkdir -p __logger

# Install dependencies and tools
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Set display environment variable
ENV DISPLAY=:99

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run the script
CMD ["python", "./headless.py"]
