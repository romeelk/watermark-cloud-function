import unittest
import watermarklocal
import os
class TestWatermark(unittest.TestCase):

    def test_valid_watermark_file(self):
        input_file = os.path.abspath("input.pdf")
        watermark_file = os.path.abspath("watermark.pdf")
        result = watermarklocal.generate_watermark(input_file, watermark_file)
        self.assertEqual(os.path.basename(result), "input_watermark.pdf")

if __name__ == '__main__':
    unittest.main()