from pybricks.parameters import Direction

import constants, leg, rpc


class FrontBrick:

    front = None

    def __init__(self):
        self.frontLegs = leg.FrontLegSet()

    def connect(self):
        self.frontLegs.connect()


def main():
    fb = FrontBrick()
    fb.connect()
    server = rpc.RPCServer(fb)
    server.connect()
    server.run()


if __name__ == '__main__':
    main()
