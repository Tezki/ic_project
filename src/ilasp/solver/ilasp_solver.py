import os
import subprocess

ILASP_BINARY_NAME = "ILASP"
CLINGO_BINARY_NAME = "clingo"  # use clingo.rb for minimal solutions
CLINGO_MINIMAL_BINARY_NAME = "clingo.rb"
TIMEOUT_ERROR_CODE = 124

ILASP_OPERATION_SOLVE = "solve"
ILASP_OPERATION_SEARCH_SPACE = "search_space"


def solve_ilasp_task(ilasp_problem_filename, output_filename, version="4", max_body_literals=3,
                     timeout=60*10, binary_folder_name=None, compute_minimal=False, operation=ILASP_OPERATION_SOLVE):
    with open(output_filename, 'w') as f:
        arguments = []
        if timeout is not None:
            arguments = ["timeout", str(timeout)]

        if binary_folder_name is None:
            ilasp_binary_path = ILASP_BINARY_NAME
        else:
            ilasp_binary_path = os.path.join(binary_folder_name, ILASP_BINARY_NAME)

        arguments.extend([ilasp_binary_path,
                          "--version=" + version,  # test 2 and 2i
                          "--max-rule-length=4" + str(max_body_literals+1),
                          "-ml=" + str(max_body_literals),
                          ilasp_problem_filename
                          ])

        if operation == ILASP_OPERATION_SEARCH_SPACE:
            arguments.append("-s")

        return_code = subprocess.call(arguments, stdout=f)
        return return_code != TIMEOUT_ERROR_CODE