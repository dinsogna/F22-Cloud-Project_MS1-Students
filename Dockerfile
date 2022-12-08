# Set base image (host OS)
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app


COPY . . 
COPY nginx.conf /etc/nginx/conf.d/virtual.conf

# Copy all files to the working directory

RUN apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
# Install any dependencies
RUN pip install -r requirements.txt

EXPOSE 80

# Specify the command to run on container start
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]