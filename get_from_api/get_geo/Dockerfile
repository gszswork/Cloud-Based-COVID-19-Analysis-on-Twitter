FROM python:3.8.5

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000


RUN mkdir /workspace
WORKDIR /workspace
ADD . /workspace

RUN pip install -r get_location_requirement.txt

ENTRYPOINT [ "python", "./get_locate.py"]