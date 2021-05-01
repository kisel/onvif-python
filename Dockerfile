FROM python:3
RUN pip install onvif_zeep pyyaml
WORKDIR /app/
COPY init.py ./
COPY docs/ docs/
ENV PYTHONSTARTUP init.py
ENV PYTHONUNBUFFERED 1


