import os
from ilasp.generator.utils.ilasp_task_generator_example import generate_examples
from ilasp.generator.utils.ilasp_task_generator_state import generate_state_statements
from ilasp.generator.utils.ilasp_task_generator_transition import generate_timestep_statements, generate_state_at_timestep_statements, generate_transition_statements
from ilasp.generator.utils.ilasp_task_generator_knowlegebase import generate_knowledgebase
from ilasp.generator.utils.ilasp_task_generator_mode import generate_constant_statements, generate_mode_bias



def generate_ilasp_task(num_states, accepting_state, rejecting_state, predicates, observables, goal_examples, dend_examples,
                        inc_examples, num_variables, learn_explicit, output_folder, output_filename):
    
    if len(dend_examples) == 0:
        rejecting_state = None

    with open(os.path.join(output_folder, output_filename), 'w') as f:
        task = _generate_ilasp_task_str(num_states, accepting_state, rejecting_state, predicates, observables, goal_examples,
                                        dend_examples, inc_examples, num_variables, learn_explicit)
        f.write(task)


def _generate_ilasp_task_str(num_states, accepting_state, rejecting_state, predicates, observables, goal_examples, dend_examples,
                             inc_examples, num_variables, learn_explicit):
    
    task = generate_state_statements(num_states, accepting_state, rejecting_state)

    task += generate_timestep_statements(goal_examples, dend_examples, inc_examples)
    task += generate_state_at_timestep_statements(num_states, accepting_state, rejecting_state)
    task += generate_transition_statements()
    
    task += generate_knowledgebase(num_states, rejecting_state, predicates, observables, learn_explicit)

    task += generate_constant_statements(num_states, accepting_state, rejecting_state, observables, learn_explicit)
    task += generate_mode_bias(predicates, num_variables, learn_explicit)
    
    task += generate_examples(goal_examples, dend_examples, inc_examples)

    return task