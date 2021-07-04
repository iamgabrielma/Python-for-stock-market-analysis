from ios_calc_rsi import read_tickers_from_txt
import unittest

class TestReadTickersFromTXT(unittest.TestCase):

	def test_basic(self):
		testcase = "custom-tickers-test.txt"
		expected = ['AMZN','AAPL','PLTR']
		self.assertEqual(read_tickers_from_txt(testcase), expected)

unittest.main()