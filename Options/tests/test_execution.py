import unittest
from unittest.mock import patch
from trading.execution import Execution

class TestExecution(unittest.TestCase):
    def setUp(self):
        self.execution = Execution()

    @patch('trading.execution.Execution.place_order')
    def test_execute_trade(self, mock_place_order):
        # Arrange
        mock_place_order.return_value = {
            'status': 'success',
            'order_id': '12345',
            'symbol': 'BTCUSD',
            'price': '40000',
            'quantity': '1'
        }
        order_details = {
            'symbol': 'BTCUSD',
            'price': '40000',
            'quantity': '1'
        }

        # Act
        result = self.execution.execute_trade(order_details)

        # Assert
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['order_id'], '12345')
        self.assertEqual(result['symbol'], 'BTCUSD')
        self.assertEqual(result['price'], '40000')
        self.assertEqual(result['quantity'], '1')

if __name__ == '__main__':
    unittest.main()
