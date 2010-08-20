"""
Test for single criteria EI example.
"""

import unittest
import random

from numpy import random as numpy_random

from pyevolve import Selectors

from openmdao.main.api import set_as_top
from openmdao.examples.singleEI.branin_ei_example import Analysis, Iterator
from openmdao.lib.doegenerators.full_factorial import FullFactorial



class EITest(unittest.TestCase):
    """Test to make sure the EI sample problem works as it should"""
    
    def setUp(self):
        # pyevolve does some caching that causes failures during our
        # complete unit tests due to stale values in the cache attributes
        # below, so reset them here
        Selectors.GRankSelector.cachePopID = None
        Selectors.GRankSelector.cacheCount = None
        Selectors.GRouletteWheel.cachePopID = None
        Selectors.GRouletteWheel.cacheWheel = None
        

    def tearDown(self):
        pass
    
    def test_EI(self): 
        random.seed(10)
        analysis = Analysis()
        set_as_top(analysis)
        analysis.DOE_trainer.DOEgenerator = FullFactorial(2, 2)
        analysis.iterations = 1
        analysis.run()
        analysis.cleanup()
        self.assertAlmostEqual(9.85,analysis.EI_driver.next_case[0].inputs[0][2],1)
        self.assertAlmostEqual(2.95,analysis.EI_driver.next_case[0].inputs[1][2],1)
        analysis = None
        
if __name__=="__main__": #pragma: no cover
    import sys
    if '--profile' in sys.argv:
        sys.argv.remove('--profile')
        import cProfile
        import pstats
        cProfile.run("unittest.main()", "test.prof")
        p = pstats.Stats("test.prof")
        p.sort_stats('cumulative').print_stats()
    else:
        unittest.main()



