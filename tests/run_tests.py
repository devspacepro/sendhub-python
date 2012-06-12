#!/usr/bin/env python

import sys
import unittest

def suite():
    
    from functional.apiclient_basic_tests import APIBasicTests
    from functional.message_tests import MessageTests
    
    
    test_cases = [
        APIBasicTests,
        MessageTests,
    ]
    
    return unittest.TestSuite(
        [unittest.TestLoader().loadTestsFromTestCase(case)
            for case in test_cases]
    )
    
if __name__ == '__main__':
    
    # load tests
    test_suite = suite()
    
    # run tests
    unittest.TextTestRunner(verbosity=1, descriptions=1).run(test_suite)