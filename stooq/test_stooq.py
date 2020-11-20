import unittest
import stooq

class TestSum(unittest.TestCase):

    def test_AAPLStock(self):
        self.assertRegex(stooq.checkStock('AAPL.US|main'), r'\w*.\w* quote is \$\d*.\d* per share')

    def test_TSLAStock(self):
        self.assertRegex(stooq.checkStock('TSLA.US|main'), r'\w*.\w* quote is \$\d*.\d* per share')

    def test_COCAStock(self):
        self.assertNotRegex(stooq.checkStock('COCA.US|main'), r'\w*.\w* quote is \$\d*.\d* per share')

    def test_EmptyMessage(self):
        self.assertEqual(stooq.checkStock(''), 'ERR: Input is missing')

    def test_EmptyStock(self):
        self.assertEqual(stooq.checkStock('|main|'), 'ERR: Wrong No of parameters')        

    def test_NoNetwork(self):
        import socket

        oldSocket = socket.socket
        def guard(*args, **kwargs):
            raise Exception("I told you not to use the Internet!")
        socket.socket = guard
        result = stooq.checkStock('AMZN.US|main')
        socket.socket = oldSocket
        self.assertEqual(result, 'ERR: I told you not to use the Internet!')

        


if __name__ == '__main__':
    unittest.main()