import random
from abc import ABC
from gym import spaces
from gym_subgoal_automata.envs.gridworld.gridworld_env import GridWorldEnv, GridWorldActions
from gym_subgoal_automata.utils.subgoal_automaton import SubgoalAutomaton
from gym_subgoal_automata.utils import utils

from ilasp.ilasp_common import OBS_STR

class GeoWorldObject:
    AGENT     = "A"
    WALL      = "X"

    MUSEUM    = "ms"
    WATERFALL = "wf"
    CAVE      = "cv"
    PARK      = "pk"
    FOREST    = "ft"
    MOUNTAIN  = "mt"
    MALL      = "ml"
    SCHOOL    = "sc"
    CHURCH    = "ch"

    LANDMARK = "lmk"
    OBSTACLE = "obt"
    BUILDING = "bld"


class GeoWorldEnv(GridWorldEnv, ABC):

    GRID_HEIGHT = "height"
    GRID_WIDTH = "width"
    ENFORCE_SINGLE_OBSERVARBLE_PER_LOCATION = "enforce_single_observable_per_location"

    def __init__(self, params=None):
        super().__init__(params)

        self.agent = None       # agent's location
        self.prev_agent = None  # previous agent location
        self.init_agent = None  # agent's initial position, for resetting

        self.locations = {}     # locations of the objects

        # grid size
        self.height = utils.get_param(params, GeoWorldEnv.GRID_HEIGHT, 10)
        self.width = utils.get_param(params, GeoWorldEnv.GRID_WIDTH, 10)
        self.observation_space = spaces.Discrete(self._get_num_states())

        self.enforce_single_observable_per_location = utils.get_param(params, GeoWorldEnv.ENFORCE_SINGLE_OBSERVARBLE_PER_LOCATION, False)

        # the completion of the task is checked against the ground truth automaton
        self.automaton = self.get_automaton()
        self.automaton_state = None

        self._load_map()

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        if self.is_game_over:
            return self._get_state(), 0.0, True, self.get_observations()

        target_x, target_y = self.agent

        if action == GridWorldActions.UP:
            target_y += 1
        elif action == GridWorldActions.DOWN:
            target_y -= 1
        elif action == GridWorldActions.LEFT:
            target_x -= 1
        elif action == GridWorldActions.RIGHT:
            target_x += 1

        target_pos = (target_x, target_y)
        if self._is_valid_position(target_pos):
            self.prev_agent = self.agent
            self.agent = target_pos
            self._update_state()

        reward = 1.0 if self.is_goal_achieved() else 0.0
        self.is_game_over = self.is_terminal()

        return self._get_state(), reward, self.is_game_over, self.get_observations()

    def _get_num_states(self):
        return self.width * self.height

    def _get_state(self):
        num_states = self._get_num_states()

        state_possible_values = [self.width, self.height]
        state_variables = [self.agent[0], self.agent[1]]

        state_id = self.get_state_id(num_states, state_possible_values, state_variables)

        if self.use_one_hot_vector:
            return self.get_one_hot_state(num_states, state_id)

        return state_id

    def get_observables(self):
        return [GeoWorldObject.MUSEUM, GeoWorldObject.WATERFALL, GeoWorldObject.CAVE, GeoWorldObject.PARK,
                GeoWorldObject.FOREST, GeoWorldObject.MOUNTAIN, GeoWorldObject.MALL, GeoWorldObject.SCHOOL, GeoWorldObject.CHURCH]
    
    def get_predicates(self):
        return [GeoWorldObject.LANDMARK, GeoWorldObject.OBSTACLE, GeoWorldObject.BUILDING]
    
    def get_typed_observables(self):
        return [[GeoWorldObject.MUSEUM, GeoWorldObject.WATERFALL, GeoWorldObject.CAVE, GeoWorldObject.PARK],
                [GeoWorldObject.FOREST, GeoWorldObject.WATERFALL, GeoWorldObject.MOUNTAIN, GeoWorldObject.MALL],
                [GeoWorldObject.MUSEUM, GeoWorldObject.SCHOOL, GeoWorldObject.CHURCH, GeoWorldObject.MALL]]

    def get_observations(self):
        return set(self.locations[self.agent]) if self.agent in self.locations else {}

    def is_terminal(self):
        return self.automaton.is_terminal_state(self.automaton_state)

    def is_goal_achieved(self):
        return self.automaton.is_accept_state(self.automaton_state)

    def reset(self):
        super().reset()

        # set initial state
        self.agent = self.init_agent
        self.prev_agent = None
        self.automaton_state = self.automaton.get_initial_state()

        # update initial automaton state according to the map layout
        self._update_state()

        return self._get_state()

    def _update_state(self):
        if self.prev_agent != self.agent:
            self.automaton_state = self.automaton.get_next_state(self.automaton_state, self.get_observations(), self.get_predicates(), self.get_typed_observables())
            #print(self.automaton_state)
            #print(self.get_observations())

    def _load_map(self):
        random_gen = random.Random(self.seed)

        self._add_location(GeoWorldObject.MUSEUM, 2, random_gen)
        self._add_location(GeoWorldObject.WATERFALL, 3, random_gen)
        self._add_location(GeoWorldObject.CAVE, 3, random_gen)
        self._add_location(GeoWorldObject.PARK, 5, random_gen)
        self._add_location(GeoWorldObject.FOREST, 5, random_gen)
        self._add_location(GeoWorldObject.MOUNTAIN, 2, random_gen)
        self._add_location(GeoWorldObject.MALL, 4, random_gen)
        self._add_location(GeoWorldObject.SCHOOL, 3, random_gen)
        self._add_location(GeoWorldObject.CHURCH, 3, random_gen)

        self.init_agent = self._generate_random_pos(random_gen)
        while self.init_agent in self.locations:
            self.init_agent = self._generate_random_pos(random_gen)

    def _add_location(self, symbol, number, random_gen):
        for _ in range(number):
            pos = (-1, -1)
            while not self._is_valid_position(pos) or \
                    (pos in self.locations and symbol in self.locations[pos]) or \
                    (self.enforce_single_observable_per_location and pos in self.locations):
                pos = self._generate_random_pos(random_gen)
            if pos not in self.locations:
                self.locations[pos] = []
            self.locations[pos].append(symbol)

    def _generate_random_pos(self, random_gen):
        return random_gen.randint(0, self.width - 1), random_gen.randint(0, self.height - 1)

    def _is_valid_position(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def render(self, mode='human'):
        self._render_horizontal_border()

        for y in range(self.height - 1, -1, -1):
            print(GeoWorldObject.WALL, end="")
            for x in range(self.width):
                position = (x, y)
                if position == self.agent:
                    print(GeoWorldObject.AGENT, end="")
                elif position in self.locations:
                    print(self.locations[position][0], end="")  # just print one of the items in the position
                else:
                    print(" ", end="")
            print(GeoWorldObject.WALL)

        self._render_horizontal_border()

    def _render_horizontal_border(self):
        for i in range(self.width + 2):
            print(GeoWorldObject.WALL, end="")
        print()



# Env

class GeoWorldLandmarkEnv(GeoWorldEnv):
    """ 
    Task 1
    Observe a landmark while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkWithRestrictionsEnv(GeoWorldEnv):
    """
    Task 2
    Observe a landmark that is not a museum while avoiding an obstacle that is not a mountain.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not eq(V2,ms); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2); not eq(V2,mt)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2); not eq(V2,mt)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldObstacleWithRestrictionEnv(GeoWorldEnv):
    """
    Task 3
    Observe a landmark while avoiding an obstacle that is not the said landmark.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2); not lmk(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2); not lmk(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkOrBuildingEnv(GeoWorldEnv):
    """
    Task 4
    Observe a landmark or a building while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)",
                                            "obs(V2,V1); bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkAndBuildingEnv(GeoWorldEnv):
    """
    Task 5
    Observe a landmark and a building simultaneously while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); obs(V3,V1); bld(V3); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkIsBuildingEnv(GeoWorldEnv):
    """
    Task 6
    Observe a landmark that is a building while avoiding an obstacle.
    In this case the only avaliable choice is to see a museum ("ms").
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkIsNotBuildingEnv(GeoWorldEnv):
    """
    Task 7
    Observe a landmark that is not a building while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldObstacleIsBuildingEnv(GeoWorldEnv):
    """
    Task 8
    Observe a landmark while avoiding an obstacle that is a building.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); bld(V2); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); bld(V2); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldObstacleIsNotBuildingEnv(GeoWorldEnv):
    """
    Task 9
    Observe a landmark while avoiding an obstacle that is not a building.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); not bld(V2); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); not bld(V2); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkBuildingSequenceEnv(GeoWorldEnv):
    """
    Task 10
    Observe, in sequence, a landmark and a building while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u1")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u1", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u1", "u_acc", ["obs(V2,V1); bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u1", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldLandmarkSequenceWithRestrictionsEnv(GeoWorldEnv):
    """
    Task 11
    Observe, in sequence, a landmark that is a building and a landmark that is not a building while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u1")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u1", ["obs(V2,V1); lmk(V2); bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u1", "u_acc", ["obs(V2,V1); lmk(V2); not bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u1", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton

class GeoWorldTestEnv(GeoWorldEnv):
    """
    Observe, in sequence, a landmark that is a building and a landmark that is not a building while avoiding an obstacle.
    """

    def get_restricted_observables(self):# not using this function
        return []

    def get_automaton(self):
        automaton = SubgoalAutomaton()
        automaton.add_state("u0")
        automaton.add_state("u_acc")
        automaton.add_state("u_rej")

        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); lmk(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_acc", ["obs(V2,V1); bld(V2); not rej_cond(V1)"])
        automaton.add_edge("u0", "u_rej", ["obs(V2,V1); obt(V2)"])
        automaton.add_edge("u_rej", "u_rej", ["obs(V2,V1); obt(V2)"])

        automaton.set_initial_state("u0")
        automaton.set_accept_state("u_acc")
        automaton.set_reject_state("u_rej")
        return automaton