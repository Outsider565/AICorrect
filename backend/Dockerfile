FROM gcc:11.3.0
# Install python3
ADD sources.list /etc/apt/
COPY pip.conf /etc/pip.conf
COPY requirements.txt /root/requirements.txt
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --upgrade pip && python3 -m pip install -r /root/requirements.txt
EXPOSE 8080
CMD [ "bash" ]
