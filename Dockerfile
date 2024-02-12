FROM python:3.12

ADD ./ebAlert /app/
ADD ./ebAlert-TelegramBot /app/
ADD ./setup.py /app/

WORKDIR /app

RUN pip install .

ENTRYPOINT ["python", "/app/ebAlert-TelegramBot/main.py"]

# Cron job needed:
# */5 * * * * root docker exec $CONTAINER python3 -m ebAlert start