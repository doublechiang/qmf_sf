from difflib import unified_diff
import unittest
from pu9sf import Pu9sf

class testPu9sf(unittest.TestCase):
    def test_wip(self):
        """ Wip call should get something.
        """
        wip_rack = Pu9sf().wip()
        self.assertTrue(len(wip_rack)>0)

    def test_racklink(self):
        racklink = Pu9sf().racklink('R21932204000601E')
        # Rack R21932204000601E has 34 link items.
        self.assertEqual(len(racklink), 34)

if __name__ == '__main__':
    unittest.main()
