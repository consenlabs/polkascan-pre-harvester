import json
import websockets
import substrateinterface

class SubstrateInterface(substrateinterface.SubstrateInterface):
    async def ws_request(self, payload):
        """
        Internal method to handle the request if url is a websocket address (wss:// or ws://)

        Parameters
        ----------
        payload: a dict that contains the JSONRPC payload of the request

        Returns
        -------
        This method doesn't return but sets the `_ws_result` object variable with the result
        """
        async with websockets.connect(
                self.url,
                max_size=2**40,
        ) as websocket:
            await websocket.send(json.dumps(payload))
            self._ws_result = json.loads(await websocket.recv())
