import pathlib
import unittest


class TestStub(unittest.TestCase):

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
