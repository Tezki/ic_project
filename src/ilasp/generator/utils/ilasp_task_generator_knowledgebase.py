from ilasp.ilasp_common import TRANSITION_STR, CONNECTED_STR

def generate_knowledgebase(num_states, rejecting_state, predicates, observables, learn_explicit):
    kb = ""

    knowledgebase = _generate_type_predicates(predicates, observables)
    if learn_explicit:
        knowledgebase += _generate_eq(predicates)
    knowledgebase += _generate_rej_condition_assumptions(num_states, rejecting_state)

    return knowledgebase


def _generate_type_predicates(predicates, observables):
    typeKnowledge = ""
    for i in range(len(predicates)):
        for obs in observables[i]:
            typeKnowledge += "%s(%s). " % (predicates[i], obs)
        typeKnowledge += "\n"
    return typeKnowledge

def _generate_eq(predicates):
    rules = ""
    for i in range(len(predicates)):
        for j in range(len(predicates)):
            rules += "eq(V,C) :- %s(V), %s(C), V==C.\n" % (predicates[i], predicates[j])
    return rules+"\n"

def _generate_rej_condition_assumptions(num_states, rejecting_state):
    stmt = ""

    if rejecting_state is not None:
        for i in range(num_states - 2):
            stmt += "%s(u%d, %s).\n" % (CONNECTED_STR, i, rejecting_state)
            stmt += "%s(u%d, %s, T) :- rej_cond(T).\n" % (TRANSITION_STR, i, rejecting_state)
    
    return stmt