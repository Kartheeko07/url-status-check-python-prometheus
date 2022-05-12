ARG PYTHON_VERSION=3.9

FROM python:$PYTHON_VERSION

LABEL description="Service to check an external URL status and outputs the response in Prometheus format"
LABEL maintainer="Kartheek Anumolu"

COPY . /

RUN pip install -r /requirements.txt

EXPOSE 80

WORKDIR /

ENTRYPOINT ["python"]

CMD ["/url-status-check.py"]