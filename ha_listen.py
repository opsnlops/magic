#!/usr/bin/env python3

import logging
import socket

from time import sleep
from zeroconf import ServiceBrowser, Zeroconf, IPVersion

# The mDNS service type we're using for the broker
service_type = "_mqtt._tcp.local."

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

            if info.properties[b"role"] == b"magic":
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


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
    )

    find_magic_broker()
    print(brokers)
