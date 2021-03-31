# Simple file containing some win condition presets

RULE_1 = list()
RULE_2 = [2, 2, 2]
RULE_3 = [1, 2, 3]
RULE_4_DEFAULT = [1, 1, 2, 2]

DEFAULT_WIN_CONDITIONS = [RULE_1, RULE_2, RULE_3, RULE_4_DEFAULT]

def getDefaults():
    return DEFAULT_WIN_CONDITIONS.copy()