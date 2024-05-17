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
RUN CHROME_VERSION=125.0.6422.60
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN apt-get -y update
RUN apt-get install -y ./google-chrome-stable_${CHROME_VERSION}_amd64.deb


# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=125.0.6422.60 && \
    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chrome-linux64.zip   && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set display environment variable
ENV DISPLAY=:99

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run the script
CMD ["python", "./login-test.py"]
