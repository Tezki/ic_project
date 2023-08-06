import argparse
from utils import utils
from ilasp.generator.ilasp_task_generator import generate_ilasp_task
from ilasp.solver.ilasp_solver import solve_ilasp_task
from ilasp.parser.ilasp_solution_parser import parse_ilasp_solutions


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("task_config", help="json file containing number of states, number of variables, max_body_literals, wheteher to learn explicitly, observables and examples")
    parser.add_argument("task_filename", help="filename of the ILASP task")
    parser.add_argument("solution_filename", help="filename of the ILASP task solution")
    parser.add_argument("plot_filename", help="filename of the automaton plot")
    return parser

if __name__ == "__main__":
    args = get_argparser().parse_args()
    config = utils.read_json_file(args.task_config)

    generate_ilasp_task(config["num_states"], "u_acc", "u_rej", config["predicates"], config["observables"], 
                        config["goal_examples"], config["deadend_examples"], config["inc_examples"],
                        config["num_variables"], config["learn_explicit"], ".", args.task_filename, )
    solve_ilasp_task(args.task_filename, args.solution_filename, max_body_literals=config["max_body_literals"] ,binary_folder_name="../bin")
    automaton = parse_ilasp_solutions(args.solution_filename)
    automaton.plot(".", args.plot_filename)