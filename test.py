import numpy as np
from pprint import pprint
from dr._dr import DR
from dr.dr import DiagnosticReasoner


if __name__ == '__main__':
    # Dependency matrix
    d_matrix = np.asarray([[1, 1, 1, 1], \
                           [0, 1, 1, 0], \
                           [0, 1, 1, 0], \
                           [0, 0, 0, 1], \
                           [0, 0, 1, 0]], dtype=np.float32)
    # Diagnostic Reasoner
    # dr = DR(verbose=False)
    dr = DiagnosticReasoner()

    # quit()


    # Test Example 1
    print("Example 1")
    test_result1 = ["PASS", "PASS", "FAIL", "PASS"]
    dr.process(d_matrix, test_result1)
    # pprint(vars(dr))
    # Test Example 2
    print("Example 2")
    test_result2 = ["UNKNOWN", "FAIL", "FAIL", "PASS"]
    dr.process(d_matrix, test_result2)