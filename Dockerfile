FROM resin/rpi-raspbian
MAINTAINER Nathan Osman <nathan@quickmediasolutions.com>

RUN \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN \
    pip3 install influxdb w1thermsensor

COPY tsat.py /root/tsat.py

ENV \
    INTERVAL=300 \
    INFLUXDB_HOST=localhost \
    INFLUXDB_PORT=8086 \
    INFLUXDB_DATABASE=thsat \
    INFLUXDB_USERNAME= \
    INFLUXDB_PASSWORD= \
    INFLUXDB_TAGS=

CMD python /root/tsat.py \
    --influxdb-host "$INFLUXDB_HOST" \
    --influxdb-port "$INFLUXDB_PORT" \
    --influxdb-database "$INFLUXDB_DATABASE" \
    --influxdb-username "$INFLUXDB_USERNAME" \
    --influxdb-password "$INFLUXDB_PASSWORD" \
    --influxdb-tags "$INFLUXDB_TAGS"
