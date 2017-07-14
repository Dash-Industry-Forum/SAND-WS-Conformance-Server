"""
SAND WS conformance server.

This implements a conformance server for ISO/IEC 23009-5 SAND.
It validates the incoming SAND messages as well as the protocols used by
a SAND client.

Copyright (c) 2017-, TNO
All rights reserved.

See AUTHORS for a full list of authors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the ISO/IEC nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys

from twisted.python import log
from twisted.internet import reactor

from autobahn.twisted.websocket import (WebSocketClientFactory,
                                        WebSocketClientProtocol, connectWS)

SAND_MESSAGE = None

class TestClientProtocol(WebSocketClientProtocol):
    """
    Test client that reads a SAND message stored into a file
    and sends it to a WebSocket server.
    """

    def onOpen(self):
        self.send_file()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print "Binary message received: {0} bytes".format(len(payload))
        else:
            print "Text message received: {0}".format(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        reactor.stop()

    def send_file(self):
        with open(SAND_MESSAGE, "r") as sand_message:
            self.sendMessage(sand_message.read().encode('utf-8'))

def run():
    """
    Run the WS client.
    """
    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = TestClientProtocol
    connectWS(factory)
    reactor.run()

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    SAND_MESSAGE = sys.argv[2]
    run()
