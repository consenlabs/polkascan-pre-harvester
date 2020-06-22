import asyncio
import json
import requests
import websockets
import substrateinterface

from substrateinterface.exceptions import SubstrateRequestException, ConfigurationError

class SubstrateInterface(substrateinterface.SubstrateInterface):
    def rpc_request(self, method, params, result_handler=None):
        """
        Method that handles the actual RPC request to the Substrate node. The other implemented functions eventually
        use this method to perform the request.

        Parameters
        ----------
        result_handler: Callback of function that processes the result received from the node
        method: method of the JSONRPC request
        params: a list containing the parameters of the JSONRPC request

        Returns
        -------
        a dict with the parsed result of the request.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.request_id
        }

        self.debug_message('RPC request "{}"'.format(method))

        if self.url[0:6] == 'wss://' or self.url[0:5] == 'ws://':
            ws_result = {}

            async def ws_request(ws_payload):
                """
                Internal method to handle the request if url is a websocket address (wss:// or ws://)

                Parameters
                ----------
                ws_payload: a dict that contains the JSONRPC payload of the request

                Returns
                -------
                This method doesn't return but updates the `ws_result` object variable with the result
                """
                async with websockets.connect(
                        self.url,
                        max_size=2**40,
                ) as websocket:
                    await websocket.send(json.dumps(ws_payload))

                    if callable(result_handler):
                        event_number = 0
                        while not ws_result:
                            result = json.loads(await websocket.recv())
                            self.debug_message("Websocket result [{}] Received from node: {}".format(event_number, result))

                            # Check if response has error
                            if 'error' in result:
                                raise SubstrateRequestException(result['error'])

                            callback_result = result_handler(result)
                            if callback_result:
                                ws_result.update(callback_result)

                            event_number += 1
                    else:
                        ws_result.update(json.loads(await websocket.recv()))

            asyncio.run(ws_request(payload))
            json_body = ws_result

        else:

            if result_handler:
                raise ConfigurationError("Result handlers only available for websockets (ws://) connections")

            response = requests.request("POST", self.url, data=json.dumps(payload), headers=self.default_headers)

            if response.status_code != 200:
                raise SubstrateRequestException("RPC request failed with HTTP status code {}".format(response.status_code))

            json_body = response.json()

        return json_body
