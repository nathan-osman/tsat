from argparse import ArgumentParser
from time import sleep

from influxdb import InfluxDBClient
from w1thermsensor import W1ThermSensor


class Tsat:

    def __init__(self, args):
        self._client = InfluxDBClient(
            args.influxdb_host,
            args.influxdb_port,
            args.influxdb_username,
            args.influxdb_password,
            args.influxdb_database,
        )
        self._sensor = W1ThermSensor()
        self._interval = args.interval
        self._tags = self._parse_tags(args.influxdb_tags)

    def run(self):
        while True:
            t = self._sensor.get_temperature()
            self._client.write_points([
                {
                    'measurement': 'temperature',
                    'tags': self._tags,
                    'fields': {
                        'value': t,
                    },
                },
            ])
            sleep(self._interval)

    def _parse_tags(self, tagstr):
        tags = {}
        for p in tagstr.split(','):
            t = p.split('=')
            tags[t[0]] = t[1]
        return tags


if __name__ == '__main__':
    parser = ArgumentParser(description="Read temperature data and push to InfluxDB")
    parser.add_argument('--interval', default=300, type=int)
    parser.add_argument('--influxdb-host', default='localhost')
    parser.add_argument('--influxdb-port', default=8086, type=int)
    parser.add_argument('--influxdb-database', default='thsat')
    parser.add_argument('--influxdb-username')
    parser.add_argument('--influxdb-password')
    parser.add_argument('--influxdb-tags')
    Tsat(parser.parse_args()).run()
