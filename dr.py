# D-matrix solving algorithm
# By: Murali Krishnan Rajasekharan Pillai @ Purdue University



import numpy as np

class DR(object):

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.valid_test_results = ["PASS", "FAIL", "UNKNOWN"]
        self.num_failure_modes = None
        self.num_tests = None
        self.d_matrix = None
        self.failure_modes = None


    def reason(self, d_matrix, test_result):
        ''' Reason with a `d_matrix` and `test_result`
        '''
        check_result = self.validate_inputs(d_matrix, test_result)
        verbose = self.verbose
        if check_result == "DR_ERROR_NO_ERROR":
            [num_failure_modes, num_tests] = d_matrix.shape
            # Assign 
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
                self.process_single_test(i_test, test_result[i_test])

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

    def process_single_test(self, test_index, test_result):
        ''' Finds the failure modes affected by a test and markes them
        '''

        for i in range(self.num_failure_modes):
            entry = self.d_matrix[i, test_index]
            if (entry == 1):
                self.set_failure_mode(i, test_index, test_result)
        

    def set_failure_mode(self, failure_mode_index, test_index, test_result):
        ''' Sets a singel failure mode depending on the test value and the
        current failure mode value.
        '''
        if test_result == "PASS":
            self.failure_modes[failure_mode_index] = "GOOD"

        if test_result == "FAIL":
            if self.failure_modes[failure_mode_index] != "GOOD":
                self.failure_modes[failure_mode_index] = "SUSPECT"

        # All other cases will not change the mode of the failure mode


    def check_suspect_for_bad(self, suspect_failure_mode_index, test_result):
        ''' For a suspect failure mode to be marked as bad
        '''

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
                    break

    def validate_inputs(self, d_matrix, test_result):
        ''' Runs validity tests for algorithm to proceed
        '''

        [num_failure_modes, num_tests] = d_matrix.shape
        check_result = "DR_ERROR_NO_ERROR"
        if num_tests != len(test_result):
            check_result = "DR_ERROR_WRONG_NUM_TESTS"

        for result in test_result:
            if result not in self.valid_test_results:
                check_result = "DR_ERROR_INVALID_TEST_RESULT"

        valid_error_modes = ["DR_ERROR_WRONG_NUM_TESTS", "DR_ERROR_INVALID_TEST_RESULT"]

        return check_result
