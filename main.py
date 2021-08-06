import numpy as np
from dr import DR


if __name__ == '__main__':
    d_matrix = np.asarray([[1, 1, 1, 1], \
                           [0, 1, 1, 0], \
                           [0, 1, 1, 0], \
                           [0, 0, 0, 1], \
                           [0, 0, 1, 0]], dtype=np.float32)
    dr = DR(verbose=False)
    print("Example 1")
    test_result1 = ["PASS", "PASS", "FAIL", "PASS"]
    dr.process(d_matrix, test_result1)

    print("Example 2")
    test_result2 = ["UNKNOWN", "FAIL", "FAIL", "PASS"]
    dr.process(d_matrix, test_result2)