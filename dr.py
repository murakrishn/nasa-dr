# D-matrix solving algorithm
# By: Murali Krishnan Rajasekharan Pillai @ Purdue University



import numpy as np

class DR(object):
    """
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.valid_test_results = ["PASS", "FAIL", "UNKNOWN"]
        self.num_failure_modes = None
        self.num_tests = None
        self.d_matrix = None
        self.failure_modes = None


    def process(self, d_matrix: np.ndarray, test_result: list):
        """ Find failure modes with a `d_matrix` and `test_result`

        Input Arguments:
        ----------------
        d_matrix    : numpy.ndarray
                      The diagnostics-matrix indicating the relation failure modes to
                      the tests that are considered
        test_results: list
                      The test results that are used to reason out the failure modes
        """
        check_result = self.validate_inputs(d_matrix, test_result)
        verbose = self.verbose
        if check_result == "DR_ERROR_NO_ERROR":
            [num_failure_modes, num_tests] = d_matrix.shape
            # NOTE :: Change to setter / getter functions in Python
            self.d_matrix = d_matrix
            self.num_failure_modes = num_failure_modes
            self.num_tests = num_tests
            self.failure_modes = ["UNKNOWN"] * num_failure_modes
            if verbose:
                print("Passes all the checks!")
                print(f"num_failure_modes: {num_failure_modes}, num_tests: {num_tests}")
                print("Initial Failure modes:")
                print(self.failure_modes)

            # Step through the set of tests to process all, will find
            # `GOOD`, `SUSPECT` and `UNKONWN` failure modes
            for i_test in range(num_tests):
                self.process_single_test(i_test, test_result)

            if verbose:
                print("Failure modes after performing Step 2")
                print(self.failure_modes)


            # Check if any of the suspect failure modes is actually bad,
            # if so then mark it as such in the failure mode array
            for i_failure_mode in range(num_failure_modes):
                if self.failure_modes[i_failure_mode] == "SUSPECT":
                    self.check_suspect_for_bad(i_failure_mode, test_result)
            
            if verbose:
                print("Failure modes after performing Step 3")
                print(self.failure_modes)

            print(f"Test Results: {test_result}")
            print(f"D-matrix: {self.d_matrix}")
            print(f"Results: {self.failure_modes}")

    def process_single_test(self, test_index: int, test_result: list):
        """ Finds the failure modes affected by a test and markes them

        Input arguments:
        ----------------
        test_index      : int
                          The index of the test to process
        test_result     : list
                          All test results obtained at the current "process"-ing step of DR
        """

        for i in range(self.num_failure_modes):
            if (self.d_matrix[i, test_index] == 1):
                self.set_failure_mode(i, test_index, test_result)
        

    def set_failure_mode(self, failure_mode_index: int, test_index: int, test_result: list):
        """ Sets a singel failure mode depending on the test value and the current failure mode value.

        Input arguments:
        ----------------
        failure_mode_index  : int
                              Index of the single failure mode associated with the `test_index` result,
                              whose resulting value will be set based on the test result and the failure
                              mode's current value
        test_index          : int
                              Index of the test being considered to set the failure mode
        test_result         : list
                              All test results obtained at the current "process"-ing step of DR



        """
        if test_result[test_index] == "PASS":
            self.failure_modes[failure_mode_index] = "GOOD"
        elif test_result[test_index] == "FAIL":
            if self.failure_modes[failure_mode_index] != "GOOD":
                self.failure_modes[failure_mode_index] = "SUSPECT"
        
        else:
            # All other cases will not change the mode of the failure mode
            pass
        


    def check_suspect_for_bad(self, suspect_failure_mode_index: int, test_result: list):
        """ For a suspect failure mode to be marked as bad
        """
        test1 = lambda j: self.d_matrix[suspect_failure_mode_index,j] == 1 and test_result[j] == "FAIL"
        test2 = lambda j, k: self.d_matrix[k,j] == 1 and (self.failure_modes[k] == "SUSPECT" or self.failure_modes[k] == "BAD")
        
        for j in range(self.num_tests):
            if (self.d_matrix[suspect_failure_mode_index,j] == 1) and \
               (test_result[j] == "FAIL"):
                num_implicated_suspects_and_bad = 0
                for k in range(self.num_failure_modes):
                    if (self.d_matrix[k,j] == 1) and \
                       ((self.failure_modes[k] == "SUSPECT") or \
                        (self.failure_modes[k] == "BAD")):
                       num_implicated_suspects_and_bad += 1

                if num_implicated_suspects_and_bad == 1:
                    self.failure_modes[suspect_failure_mode_index] = "BAD"
                    # no need to check further
                    break

    def validate_inputs(self, d_matrix: np.ndarray, test_result: list):
        """ Runs validity tests for algorithm to proceed
        """

        [num_failure_modes, num_tests] = d_matrix.shape
        check_result = "DR_ERROR_NO_ERROR"
        if num_tests != len(test_result):
            check_result = "DR_ERROR_WRONG_NUM_TESTS"

        for result in test_result:
            if result not in self.valid_test_results:
                check_result = "DR_ERROR_INVALID_TEST_RESULT"

        valid_error_modes = ["DR_ERROR_WRONG_NUM_TESTS", "DR_ERROR_INVALID_TEST_RESULT"]

        return check_result
