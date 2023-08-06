from ilasp.ilasp_common import TRANSITION_STR, CONNECTED_STR
from ilasp.generator.utils.ilasp_task_generator_example import get_longest_example_length


def generate_timestep_statements(goal_examples, dend_examples, inc_examples):
    stmt = "all_steps(0..%d).\n" % get_longest_example_length(goal_examples, dend_examples, inc_examples)
    stmt += "step(T) :- all_steps(T), last(U), T<U+1.\n\n"
    return stmt

def generate_state_at_timestep_statements(num_states, accepting_state, rejecting_state):
    stmt = _generate_initial_state_at_timestep(num_states)
    stmt += "st(T+1, Y) :- st(T, X), delta(X, Y, T).\n\n"
    stmt += _generate_acceptance_rejection_rules(accepting_state, rejecting_state)
    return stmt


def _generate_initial_state_at_timestep(num_states):
    if num_states >= 3:
        stmt = "st(0, u0).\n"
    else:
        raise ValueError("The number of states should be >= 3.")
    return stmt

def _generate_acceptance_rejection_rules(accepting_state, rejecting_state):
    # a trace is accepted if it is at the accepting state in the last timestep (or reject if it is at the rejecting
    # state in the last timestep)
    stmt = "accept :- last(T), st(T+1, %s).\n" % accepting_state
    if rejecting_state is not None:
        stmt += "reject :- last(T), st(T+1, %s).\n\n" % rejecting_state
    return stmt


def generate_transition_statements():
    # transitions are defined as the negative of the n_transitions (negative transitions)
    stmt = "phi(X, Y, T) :- %s(X, Y, T), %s(X, Y), step(T).\n" % (TRANSITION_STR, CONNECTED_STR)
    stmt += "out_phi(X, T) :- phi(X, _, T).\n"
    stmt += "delta(X, Y, T) :- phi(X, Y, T).\n"
    stmt += "delta(X, X, T) :- not out_phi(X, T), state(X), step(T).\n\n"

    # all states must be reachable from the initial state
    stmt += "reachable(u0).\n"
    stmt += "reachable(Y) :- reachable(X), ed(X, Y).\n"
    stmt += ":- not reachable(X), state(X).\n\n"

    stmt += "path(X, Y) :- %s(X, Y).\n" % CONNECTED_STR
    stmt += "path(X, Y) :- %s(X, Z), path(Z, Y).\n" % CONNECTED_STR
    stmt += ":- path(X, Y), path(Y, X).\n\n"

    stmt += ":- %s(X, Y1, T), %s(X, Y2, T), Y1!=Y2.\n\n" % (TRANSITION_STR, TRANSITION_STR)

    return stmt