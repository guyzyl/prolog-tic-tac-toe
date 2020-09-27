# Based on the official Debian Swipl Docker image
FROM swipl:latest

# Install Python dependencies
RUN apt update
RUN apt install -y python3 python3-pip

# Copy and install requirements.txt indepentntly to save build time
WORKDIR /opt
ADD requirements.txt /opt/requirements.txt
# Install Pyhton dependencies
RUN python3 -m pip install -r requirements.txt

# Copy files to image
ADD . /opt/.


# Expose server port
EXPOSE 5000

# Execute server on docker run
ENTRYPOINT [ "python3", "server.py" ]
