
def get_state_names(num_states, accepting_state, rejecting_state):
    states = ["u" + str(i) for i in range(num_states - 2)]
    states.append(accepting_state)
    if rejecting_state is not None:
        states.append(rejecting_state)
    return states


def generate_state_statements(num_states, accepting_state, rejecting_state):
    states = get_state_names(num_states, accepting_state, rejecting_state)
    return "".join(["state(" + s + ").\n" for s in states]) + '\n'