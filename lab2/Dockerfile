FROM python:3.12

RUN apt-get update && apt-get install -y iputils-ping

COPY . .
ENTRYPOINT [ "python3", "solution.py" ]
CMD [ "-h" ]
