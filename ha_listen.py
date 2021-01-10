#!/usr/bin/env python3

import logging
import socket

from time import sleep

import paho.mqtt.client as mqtt
from zeroconf import ServiceBrowser, Zeroconf, IPVersion

# The mDNS service type we're using for the broker
service_type = "_mqtt._tcp.local."
broker_role = b"magic"

brokers = []


class ZeroconfListener:
    def update_service(self, zeroconf):
        return

    def remove_service(self, zeroconf, type, name):
        logging.info("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logging.debug("Service %s added, service info: %s" % (name, info))

        # Take the first IPv4 address that's offered
        address = info.addresses_by_version(IPVersion.V4Only)[0]

        a = socket.inet_ntoa(address)
        port = info.port
        logging.debug("%s:%d", a, port)
        logging.debug(info.name)

        logging.debug(info.properties.keys())

        if b"role" in info.properties:
            logging.debug("found a broker with a role")

            if info.properties[b"role"] == broker_role:
                logging.debug("found a broker in the magic role!")
                brokers.append(
                    {
                        "ip_address": a,
                        "port": port,
                        "name": name,
                        "info": info.properties[b"info"].decode("utf-8"),
                    }
                )


def find_magic_broker():
    logging.info("attempting to find the magic broker")

    zeroconf = Zeroconf()
    listener = ZeroconfListener()
    browser = ServiceBrowser(zeroconf, service_type, listener)

    sleep(3)

    zeroconf.close()


def listen_to_broker(broker):

    print("Attempting to connect to:", broker["name"])

    client = mqtt.Client("ha_listen.py")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker["ip_address"], port=broker["port"], keepalive=60)
    logging.debug("connected!")

    client.loop_forever()


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))

    client.subscribe("#")


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode("utf-8"))


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
    )

    find_magic_broker()
    print(brokers)
    listen_to_broker(brokers[0])
