FROM gcc:11.3.0
# Install python3
ADD sources.list /etc/apt/
COPY pip.conf /etc/pip.conf
RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
CMD [ "bash" ]