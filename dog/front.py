###############################################################################
# SPDX-License-Identifier: MIT
# Copyright 2020 by EV3 Robo Dog Authros
###############################################################################
"""Robo Dog Front Brick."""
import constants, leg, rpc


class Front:
    name = 'front'

    def __init__(self):
        self.legs = leg.FrontLegSet()

    def connect(self):
        self.legs.connect()

    def disconnect(self):
        self.legs.disconnect()


def main():
    fb = Front()
    server = rpc.RPCServer(fb)
    server.connect()
    server.run()


if __name__ == '__main__':
    main()
