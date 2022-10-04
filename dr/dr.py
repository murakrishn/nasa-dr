"""Diagnostic reasoner

Author:
    Murali Krishnan R

Date:
    10.04.2022

"""


__all__ = ["DiagnosticReasoner"]


import numpy as np
import numpy.typing as npt
from typing import List


class DiagnosticReasoner:
    """Algorithm for diagnostic reasoning"""

    _valid_test_results = ["PASS", "FAIL", "UNKNOWN"]


    def __init__(self, verbose=False):
        self.verbose = verbose


        pass

    def validate_inputs(self, dmatrix: npt.NDArray, test_results: List):
        """Run validity tests for the D-matrix and `test_results`"""

        [num_failure_modes, num_tests] = dmatrix.shape

        check_result = "DR_ERROR_NO_ERROR"

        if num_tests != len(test_results):
            check_result = "DR_ERROR_WRONG_NUM_TESTS"

        for result in test_results:
            if result not in self._valid_test_results:
                check_result = "DR_ERROR_INVALID_TEST_RESULT"
        
        return check_result

    def process_single_test(self, test_id, test_result):
        """Process the result of a single test"""

        for fmode_id in range(self.num_failure_modes):
            if self.dmatrix[fmode_id, test_id] == 1:
                if test_result == "PASS":
                    self.failure_modes[fmode_id] = "GOOD"
                elif test_result == "FAIL":
                    if self.failure_modes[fmode_id] != "GOOD":
                        self.failure_modes[fmode_id] = "SUSPECT"
                    else:
                        pass
                else:
                    pass
            else:
                pass
                    
        pass

    def process(self, dmatrix: npt.NDArray, test_results: List):
        """Process a collection of `test_results` to"""

        check_result = self.validate_inputs(dmatrix, test_results)

        if check_result == "DR_ERROR_NO_ERROR":
            [num_failure_modes, num_tests] = dmatrix.shape
            self.dmatrix = dmatrix
            self.num_failure_modes = num_failure_modes
            self.num_tests = num_tests
            self.failure_modes = ["UNKNOWN" for _ in range(num_failure_modes)]
            if self.verbose:
                print()
                print("Passes all the checks!")
                print(f"num_failure_modes: {num_failure_modes}, num_tests: {num_tests}")
                print("Initial Failure modes:")
                print(self.failure_modes)
                print()
            
            # Step through tests
            # Will classify each failure mode as
            # - `GOOD`
            # - `SUSPECT`
            # - `UNKNOWN`
            for test_id, test_result in enumerate(test_results):
                self.process_single_test(test_id, test_result)

            if self.verbose:
                print("Failure modes after performing Step 2")
                print(self.failure_modes)
            
            # Check if any suspect failure modes is bad
            for fmode_id in range(self.num_failure_modes):
                if self.failure_modes[fmode_id] == "SUSPECT":
                    self.check_suspect_for_bad(fmode_id, test_results)


            if self.verbose:
                print("Failure modes after performing Step 3")
                print(self.failure_modes)
        else:
            raise RuntimeError(f"[{check_result}]!!")


        print(f"Test results: {test_results}")
        print(f"D-matrix: {self.dmatrix}")
        print(f"Results: {self.failure_modes}")
        pass

    def check_suspect_for_bad(self, failure_mode_idx: int, test_results: List):

        for test_id in range(self.num_tests):
            if (self.dmatrix[failure_mode_idx, test_id] == 1) \
                and (test_results[test_id] == "FAIL"):
                count_implicated = 0
                for fmode_id in range(self.num_failure_modes):
                    if (self.dmatrix[fmode_id, test_id] == 1) \
                        and ((self.failure_modes[fmode_id] in ["SUSPECT", "BAD"])):
                        count_implicated += 1
                    else:
                        pass
                if count_implicated == 1:
                    self.failure_modes[failure_mode_idx] = "BAD"
                    break
                else:
                    # All are "SUSPECT"
                    pass
            else:
                pass