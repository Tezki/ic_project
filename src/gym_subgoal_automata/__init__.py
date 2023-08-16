from gym.envs.registration import register

register(
    id='GeoWorldLandmarkIsNotBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkIsNotBuildingEnv',
)

register(
    id='GeoWorldLandmarkWithRestrictionsEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkWithRestrictionsEnv',
)

register(
    id='GeoWorldLandmarkSequenceWithRestrictionsEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkSequenceWithRestrictionsEnv',
)