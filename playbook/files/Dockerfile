FROM python:3.13.3-slim-bookworm
RUN ["pip3", "install", "psutil", "prometheus_client"]
ADD host_metrics_exporter.py host_metrics_exporter.py
EXPOSE 8080
ENTRYPOINT [ "python3", "host_metrics_exporter.py" ]