#!/usr/bin/env python3

import datetime
import logging
import socket
import sys
import traceback

import time

import paho.mqtt.client as mqtt
from zeroconf import ServiceBrowser, Zeroconf, IPVersion

# The mDNS service type we're using for the broker
service_type = "_mqtt._tcp.local."
broker_role = b"magic"
wait_time = 3  # How many seconds should we want for mDNS to respond

heartbeat_topic = "system/heartbeat"


# Stub client
client = mqtt.Client()


class ZeroconfListener:

    brokers = []

    def update_service(self, zeroconf):
        pass

    def remove_service(self, zeroconf, type, name):
        logging.info(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logging.debug(f"Service {name} added, service info: {info}")

        # Take the first IPv4 address that's offered
        address = info.addresses_by_version(IPVersion.V4Only)[0]

        a = socket.inet_ntoa(address)
        port = info.port
        logging.debug(f"found {a}:{port}, {info.name}")

        if b"role" in info.properties:
            logging.debug("found a broker with a role")

            if info.properties[b"role"] == broker_role:
                logging.debug(f"found a broker in the {broker_role} role!")
                self.brokers.append(
                    {
                        "ip_address": a,
                        "port": port,
                        "name": name,
                        "info": info.properties[b"info"].decode("utf-8"),
                    }
                )

    def get_brokers(self):
        return self.brokers


def find_magic_broker():
    logging.info("attempting to find the magic broker")

    zeroconf = Zeroconf()
    listener = ZeroconfListener()

    logging.debug(f"staring a browser for service type of {service_type}")
    browser = ServiceBrowser(zeroconf, service_type, listener)

    # Pause a bit and let services respond
    logging.debug(f"sleeping for {wait_time} seconds")
    time.sleep(wait_time)

    zeroconf.close()
    logging.debug("closed the zeroconf listener")

    return listener.get_brokers()


def disconnect_from_broker():
    logging.info("disconnecting from broker")
    client.disconnect()


# Connect and subscribe to everything
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    logging.debug(userdata)
    print("connected!")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logging.error("Unexpected disconnect from the broker")

    logging.info(f"Disconnected with result code {rc}")


# Print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
    )

    # Encode this at utf-8 for display to humans
    role = broker_role.decode("utf-8")

    print(f"Searching for the broker in the {role} role on the network...")
    brokers = find_magic_broker()

    # Make sure we have just one broker. It's an error if there's more than one, so
    # let me know that it found anything but one.
    if len(brokers) == 0:
        eprint(f"Couldn't find any brokers in the {role} role on the network; halting.")
        sys.exit(1)

    if len(brokers) > 1:
        eprint(
            f"There's more than one broker in the {role} role on the network. Ut oh."
        )
        sys.exit(1)

    # We've got the one we need
    broker = brokers[0]
    ip_address = broker["ip_address"]
    port = broker["port"]
    name = broker["name"]
    info = broker["info"]

    print(
        f"""...found!

    ip: {ip_address}
    port: {port}
    name: {name}
    info: {info}
    """
    )

    try:

        client.connect(ip_address, port=port, keepalive=60, bind_address="")

        print("Sending heartbeats!")
        while client.is_connected:

            now = time.localtime()

            hour = now.tm_hour
            minute = now.tm_min
            second = now.tm_sec

            heartbeat = (hour * 3600) + (minute * 60) + second
            logging.debug(f"heartbeat: {heartbeat}")

            info = client.publish(
                heartbeat_topic, payload=heartbeat, qos=0, retain=False
            )
            logging.debug(info)

            time.sleep(1)

    except KeyboardInterrupt:
        print("cleaning up...")
        disconnect_from_broker()
        time.sleep(2)

    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
