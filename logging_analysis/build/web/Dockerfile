FROM taomercy/ubuntu-python3.7.4-nginx-django3:latest
COPY ./application/client/hcc.py /usr/bin/hcc
RUN chmod 777 /usr/bin/hcc
COPY ./Web /home/Web
RUN apt-get update
RUN apt-get install libmysqlclient-dev -y
RUN apt-get install python-pip -y
RUN apt-get install libffi-dev -y
RUN pip3 install -r /home/Web/requirements.txt
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime
RUN echo "UTC" > /etc/timezone
EXPOSE 80 8080
