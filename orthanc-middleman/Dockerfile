FROM osimis/orthanc

RUN pip3 install requests
RUN pip3 install names

ENV VERBOSE_STARTUP=true
ENV VERBOSE_ENABLED=true
COPY orthanc.json /etc/orthanc/
COPY *.py /python/
