FROM ubuntu:16.04
LABEL key="antonis gantzos <antonisgantzos@gmail.com>" 
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
RUN mkdir -p /app/data
COPY app2.py /app/app2.py
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "app2.py" ]