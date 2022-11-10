FROM taomercy/ubuntu-python3.7.4-nginx-django3:tzutc
COPY ./application /root/application
COPY ./hwwuex_check /root/hwwuex_check
RUN apt-get update
RUN apt-get install libffi-dev -y
RUN pip3 install -r /root/application/server/requirements.txt
EXPOSE 8888
