"""Example scripts for diagnostic reasoning

Author:
    Murali Krishnan R
    
Date:
    10.07.2022

"""

import numpy as np
from dr.dr import DiagnosticReasoner


if __name__ == '__main__':
    # 1. Specify a Dependency-matrix (fault-to-effect mapping)
    d_matrix = np.asarray([[1, 1, 1, 1], \
                           [0, 1, 1, 0], \
                           [0, 1, 1, 0], \
                           [0, 0, 0, 1], \
                           [0, 0, 1, 0]], dtype=np.float32)
    # 2. Instantiate a static diagnostic reasoner
    dr = DiagnosticReasoner()

    # 3a. Example Test 1
    print("Example 1")
    test_result1 = ["PASS", "PASS", "FAIL", "PASS"]
    dr.process(d_matrix, test_result1)
    
    # 3b. Test Example 2
    print("Example 2")
    test_result2 = ["UNKNOWN", "FAIL", "FAIL", "PASS"]
    dr.process(d_matrix, test_result2)