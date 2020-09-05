import unittest
import process

class TestMyModule(unittest.TestCase):
    
    def test_process(self):
        self.assertEqual(process.run_process(), 'ok')



if __name__ == "__main__":
    unittest.main()
