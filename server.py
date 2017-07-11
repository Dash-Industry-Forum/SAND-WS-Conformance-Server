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
from autobahn.twisted.websocket import WebSocketServerProtocol
import logging

from sand.xml_message import XMLValidator

logging.basicConfig(filename='debug.log', level=logging.DEBUG, filemode='w')
logging.basicConfig(filename='report.log', level=logging.INFO, filemode='w')

class SandConformanceServer(WebSocketServerProtocol):
    """
    Implements a WebSocket SAND conformance server that validates
    incoming SAND messages.
    """

    def onConnect(self, request):
        logging.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logging.debug("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        success = True
        # Test 1 - Data frame type
        if isBinary:
            logging.debug(
                "Binary message received: {0} bytes".format(len(payload)))
            logging.error(
                "[TEST][KO] Data frame type. Binary frame received, "
                "text frame expected.")

        else:
            logging.debug(
                "Text message received: {0}".format(payload.decode('utf8')))
            logging.info(
                "[TEST][OK] Data frame type. Text frame received.")

            # Test 2 - Message validation
            message = payload.decode('utf8')
            validator = XMLValidator()
            if validator.from_string(message):
                logging.info("[TEST][OK] SAND message validation")
                success &= True
            else:
                logging.info("[TEST][KO] SAND message validation")
                success = False

            # echo back message verbatim
            if success:
                response = "[RESULT][OK]"
            else:
                response = "[RESULT][KO]"

            self.sendMessage(response, False)

    def onClose(self, wasClean, code, reason):
        logging.info("WebSocket connection closed: {0}".format(reason))

def run():
    """
    Runs the server.
    """
    import sys
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)

    from autobahn.twisted.websocket import WebSocketServerFactory
    factory = WebSocketServerFactory()
    factory.protocol = SandConformanceServer

    import os
    port = 9000
    if os.environ.get('PORT') is not None:
        port = int(os.environ['PORT'])

    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':
    run()
