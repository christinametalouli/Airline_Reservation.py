FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask pymongo
RUN mkdir /airline
RUN mkdir -p /airline/data
COPY air.py /airline/air.py
ADD data /airline/data
EXPOSE 5000
WORKDIR /airline
ENTRYPOINT [ "python3","-u","air.py" ]