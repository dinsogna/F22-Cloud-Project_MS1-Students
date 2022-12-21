# Set base image (host OS)
FROM amazonlinux:latest
RUN yum -y install which unzip aws-cli


# Install Python
RUN yum install -y amazon-linux-extras
RUN amazon-linux-extras install python3


# Install Nginx
RUN amazon-linux-extras install nginx1

# Set the working directory in the container
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools wheel

# copy requirements.txt and install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy Flask application code
COPY src/ src/ 
COPY start.sh /start.sh
COPY nginx.conf /etc/nginx/conf.d/virtual.conf


EXPOSE 80

# Specify the command to run on container start
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]
