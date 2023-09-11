from gym.envs.registration import register

register(
    id='GeoWorldLandmarkEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkEnv',
)

register(
    id='GeoWorldLandmarkWithRestrictionsEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkWithRestrictionsEnv',
)

register(
    id='GeoWorldObstacleWithRestrictionEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldObstacleWithRestrictionEnv',
)

register(
    id='GeoWorldLandmarkOrBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkOrBuildingEnv',
)

register(
    id='GeoWorldLandmarkAndBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkAndBuildingEnv',
)

register(
    id='GeoWorldLandmarkIsBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkAndBuildingEnv',
)

register(
    id='GeoWorldLandmarkIsNotBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkIsNotBuildingEnv',
)

register(
    id='GeoWorldObstacleIsBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldObstacleIsBuildingEnv',
)

register(
    id='GeoWorldObstacleIsNotBuildingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldObstacleIsNotBuildingEnv',
)

register(
    id='GeoWorldLandmarkBuildingSequenceEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkBuildingSequenceEnv',
)

register(
    id='GeoWorldLandmarkSequenceWithRestrictionsEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldLandmarkSequenceWithRestrictionsEnv',
)

register(
    id='GeoWorldBranchingEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldBranchingEnv',
)

register(
    id='GeoWorldTestEnv-v0',
    entry_point='gym_subgoal_automata.envs.geoworld:GeoWorldTestEnv',
)