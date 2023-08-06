from ilasp.ilasp_common import TRANSITION_STR, CONNECTED_STR, OBS_STR
from ilasp.generator.utils.ilasp_task_generator_state import get_state_names
from ilasp.generator.utils.ilasp_task_generator_example import get_max_single_step_observations

def generate_constant_statements(num_states, accepting_state, rejecting_state, observables, learn_explicit=False):
    stmt = ""

    states = get_state_names(num_states, accepting_state, rejecting_state)
    for state in states:
        stmt += "#constant(st, %s).\n" % state
    stmt += "\n"
    
    if learn_explicit:
        for type in observables:
            for obs in type:
                stmt += "#constant(o, %s).\n" % obs

    return stmt


def generate_mode_bias(predicates, num_var=2, learn_explicit=False):
    stmt = ""

    stmt += "#modeh(%s(const(st),const(st))).\n" % CONNECTED_STR
    stmt += "#modeh(%s(const(st),const(st),var(t))).\n" % TRANSITION_STR
    stmt += "#modeh(rej_cond(var(t))).\n\n"

    stmt += "#modeb(%i, %s(var(v1),var(t)),(positive)).\n" % (num_var-1,OBS_STR)
    for predicate in predicates:
        stmt += "#modeb(%i, %s(var(v1))).\n"  % (num_var-1,predicate)
    if learn_explicit:
        stmt += "#modeb(%i, eq(var(v1),const(o))).\n" % (num_var-1)
    stmt += "#modeb(1, rej_cond(var(t)),(negative)).\n\n"

    stmt += _generate_bias(predicates)

    stmt += "\n#maxv(%i).\n" % num_var

    return stmt


def _generate_bias(predicates):
    stmt = "#bias(\"\n"

    stmt += ":- not head(_).\n\n"

    stmt += ":- head(%s(U,U)).\n" % CONNECTED_STR
    stmt += ":- head(%s(U,_)), U=u_acc.\n" % CONNECTED_STR
    stmt += ":- head(%s(U,_)), U=u_rej.\n" % CONNECTED_STR
    stmt += ":- head(%s(_,U)), U=u_rej.\n" % CONNECTED_STR
    stmt += ":- head(%s(U1,U2)), body(B).\n\n" % CONNECTED_STR

    stmt += ":- head(%s(U,U,T)).\n" % TRANSITION_STR
    stmt += ":- head(%s(U,_,T)), U=u_acc.\n" % TRANSITION_STR
    stmt += ":- head(%s(U,_,T)), U=u_rej.\n" % TRANSITION_STR
    stmt += ":- head(%s(_,U,T)), U=u_rej.\n\n" % TRANSITION_STR

    for predicate in predicates:
        stmt += ":- body(%s(V)), not body(%s(V,_)).\n"  % (predicate,OBS_STR)
        stmt += ":- body(naf(%s(V))), not body(%s(V,_)).\n"  % (predicate,OBS_STR)
    
    stmt += ":- body(eq(V,C)), not body(%s(V,_)).\n"  % OBS_STR
    stmt += ":- body(naf(eq(V,C))), not body(%s(V,_)).\n\n"  % OBS_STR

    stmt += ":- head(%s(U1,U2,T)), not body(naf(rej_cond(T))).\n"  % TRANSITION_STR
    stmt += ":- head(%s(U1,U2,T1)), body(naf(rej_cond(T2))), T1!=T2.\n"  % TRANSITION_STR
    stmt += ":- head(rej_cond(T)), body(rej_cond(_)).\n \").\n"

    return stmt


def get_max_num_variables(goal_examples, dend_examples, inc_examples):
    max_obs = get_max_single_step_observations(goal_examples, dend_examples, inc_examples)
    return max_obs