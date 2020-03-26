###############################################################################
# SPDX-License-Identifier: MIT
# Copyright 2020 by EV3 Robo Dog Authros
###############################################################################
"""Generic RPC Server and Client based on Bluetooth Mailbox."""
import pickle
import sys

from pybricks import messaging, tools

COMMAND_MAILBOX_NAME = 'cmd'
RESULT_MAILBOX_NAME = 'res'

Quit = object()


def _getCallRepr(path, args, kw):
    argsStr = ', '.join(repr(arg) for arg in args)
    kwStr = ', '.join('%s=%r' %(key, val) for key, val in kw.items())
    sigStr = ', '.join(filter(None, [argsStr, kwStr]))
    return '%s(%s)' %(path, sigStr)


class ServerRpcError(Exception):

    def __init__(self, error, status=400):
        self.error = error
        self.status = status


class RemoteError(Exception):
    pass


class RPCMailbox(messaging.Mailbox):

    def __init__(self, name, connection):
        super().__init__(name, connection, pickle.dumps, pickle.loads)


class RemoteObject:

    _client = None
    path = None

    def __init__(self, path, client):
        self.path = path
        self._client = client

    def __getattr__(self, name):
        return RemoteObject(self.path + '.' + name, self._client)

    def __call__(self, *args, **kw):
        # tools.print('Calling ' + _getCallRepr(self.path, args, kw))
        cmd = self._client.cmd_mbx.send((self.path, args, kw))
        self._client.res_mbx.wait()
        status, message, data = self._client.res_mbx.read()
        if status >= 500:
            raise RemoteError(message, data)
        if status >= 400:
            data = '%s: %s' % (message, data)
        return data

    def __repr__(self):
        return RemoteObject('REPR', self._client)(self.path)


class RemoteCall:

    def __init__(self, path, args=None, kw=None):
        self.path = path
        self.args = args or ()
        self.kw = kw or {}

    def resolve(self, root, path=None):
        path = path if path is not None else self.path
        obj = root
        for name in path.split('.'):
            try:
                obj = getattr(obj, name)
            except AttributeError as err:
                raise ServerRpcError(err)
        return obj

    def call(self, root):
        callable = self.resolve(root)
        return callable(*self.args, **self.kw)

    def __repr__(self):
        return '<RemoteCall %s>' % _getCallRepr(self.path, self.args, self.kw)


class RPCServer:

    _server = None

    cmd_mbx = None
    res_mbx = None

    def __init__(self, root):
        self.root = root

    def connect(self):
        self._server = messaging.BluetoothMailboxServer()
        self.cmd_mbx = RPCMailbox(COMMAND_MAILBOX_NAME, self._server)
        self.res_mbx = RPCMailbox(RESULT_MAILBOX_NAME, self._server)

    def handle(self, call):
        # Handle system commands.
        if call.path == 'QUIT':
            self.root.disconnect()
            return Quit
        if call.path == 'PING':
            return 'PONG'
        if call.path == 'REPR':
            return repr(call.resolve(self.root, call.args[0]))
        # Run the command regularly.
        return call.call(self.root)

    def wait(self):
        tools.print('Waiting for command.')
        self.cmd_mbx.wait()
        call = RemoteCall(*self.cmd_mbx.read())
        tools.print('Received: %s' % call)
        return call

    def run(self):
        while True:
            tools.print('Waiting for connection.')
            self._server.wait_for_connection(1)
            self.root.connect()
            tools.print('Connected.')
            res = None
            while res is not Quit:
                call = self.wait()
                try:
                    res = self.handle(call)
                except ServerRpcError as err:
                    self.res_mbx.send((
                        err.status,
                        err.error.__class__.__name__, str(err.error)))
                except Exception as err:
                    tools.print('-----')
                    tools.print('Caught exception:')
                    sys.print_exception(err)
                    tools.print(err)
                    tools.print('-----')
                    self.res_mbx.send((500, err.__class__.__name__, str(err)))
                else:
                    self.res_mbx.send((200, 'Ok', res))


class RPCClient:

    server_brick_name = None
    _client = None

    cmd_mbx = None
    res_mbx = None

    def __init__(self, server_brick_name):
         self.server_brick_name = server_brick_name

    def connect(self):
        tools.print('Connecting to remote brick: ' + self.server_brick_name)
        self._client = messaging.BluetoothMailboxClient()
        self._client.connect(self.server_brick_name)
        tools.print('Connected to %r.' % self.server_brick_name)
        self.cmd_mbx = RPCMailbox(COMMAND_MAILBOX_NAME, self._client)
        self.res_mbx = RPCMailbox(RESULT_MAILBOX_NAME, self._client)

    def disconnect(self):
        self.cmd_mbx.send(('QUIT', (), {}))

    def __getattr__(self, name):
        return RemoteObject(name, self)
