import re
from ilasp.ilasp_common import TRANSITION_STR, CONNECTED_STR, REJ_STR
from collections import namedtuple

ParsedEdgeRule = namedtuple("ParsedEdgeRule", field_names=["src", "dst"])
ParsedTransitionRule = namedtuple("ParsedTransitionRule",
                                          field_names=["src", "dst", "body"])


def parse_edge_rule(edge_str):
    match = re.search(rf'{CONNECTED_STR}\((\w+),(\w+)\)', edge_str)
    return ParsedEdgeRule(match.group(1), match.group(2))

def parse_transition_rule(transition_str):
    match = re.search(rf'{TRANSITION_STR}\((\w+),(\w+),(\w+)\) :- (.+)$', transition_str)
    return ParsedTransitionRule(match.group(1), match.group(2), match.group(4).rstrip('.'))

def parse_reject_rule(reject_str):
    match = re.search(rf'{REJ_STR}\((\w+)\) :- (.+)$', reject_str)
    return match.group(2).rstrip('.')