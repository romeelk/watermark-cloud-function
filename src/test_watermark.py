import unittest
import watmerklocal

class TestWatermark(unittest.TestCase):
    def test_watermark_file(self):
        result = watmerklocal.format_file("result")
        self.assertEqual(result, "result_watermark.pdf")

if __name__ == '__main__':
    unittest.main()