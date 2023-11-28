import unittest
from unittest.mock import Mock, patch
from fastapi import WebSocket
# from utils import manager
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from connectionManager import ConnectionManager


class TestConnectionManager(unittest.TestCase):

    def setUp(self):
        self.connection_manager = ConnectionManager()

    # def test_connect_lobby(self):
    #     # Mock WebSocket
    #     mock_websocket = Mock(spec=WebSocket)

    #     # Test the connect_lobby method
    #     self.connection_manager.connect_lobby(mock_websocket)

    #     # Assertions
    #     self.assertIn(mock_websocket, self.connection_manager.lobby_connections)
    #     mock_websocket.accept.assert_called_once()

    def test_disconnect_lobby(self):
        # Mock WebSocket
        mock_websocket = Mock(spec=WebSocket)
        self.connection_manager.lobby_connections.append(mock_websocket)

        # Test the disconnect_lobby method
        self.connection_manager.disconnect_lobby(mock_websocket)

        # Assertions
        self.assertNotIn(mock_websocket, self.connection_manager.lobby_connections)

    # Similar tests for other methods...

    # Example test for broadcast_json
    # @patch.object(WebSocket, 'send_json')
    # def test_broadcast_json(self, mock_send_json):
    #     # Mock WebSockets
    #     mock_websocket1 = Mock(spec=WebSocket)
    #     mock_websocket2 = Mock(spec=WebSocket)
    #     mock_websocket3 = Mock(spec=WebSocket)

    #     # Call the method under test
    #     message = {"type": "test"}
    #     self.connection_manager.broadcast_json(message, [mock_websocket1, mock_websocket2, mock_websocket3])

    #     # Assertions
    #     mock_send_json.assert_called_with(message)
    #     mock_send_json.assert_has_calls([
    #         unittest.mock.call(message) for _ in [mock_websocket1, mock_websocket2, mock_websocket3]
    #     ])

   

if __name__ == '__main__':
    unittest.main()
