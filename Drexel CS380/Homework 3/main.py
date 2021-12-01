import random
import copy
import sys
import time

ONE_AWAY = ['WWWWBBRRRRGGYYYYGGOOOOBB', 'WWWWGGRROOGGYYYYBBOORRBB', 'WGWGRRRRGYGYYBYBOOOOWBWB', 'WBWBRRRRGWGWYGYGOOOOYBYB', 'WWOOWRWRGGGGRRYYOYOYBBBB', 'WWRRYRYRGGGGOOYYOWOWBBBB', 'WWWWRRGGGGOOYYYYOOBBBBRR', 'WWWWRRBBGGRRYYYYOOGGBBOO', 'BWBWRRRRWGWGGYGYOOOOBYBY', 'GWGWRRRRYGYGBYBYOOOOBWBW', 'RRWWRYRYGGGGYYOOWOWOBBBB', 'OOWWRWRWGGGGYYRRYOYOBBBB', 'RRRRWWGGGGYYOOOOYYBBBBWW', 'RRRRYYGGBBYYOOOOWWBBGGWW', 'RYRYGGGGYOYOOWOWBBBBRWRW', 'RWRWGGGGYRYROYOYBBBBOWOW', 'RRBBRGRGYYYYGGOOBOBOWWWW', 'RRGGOGOGYYYYBBOOBRBRWWWW', 'RRRRGGYYYYBBOOOOBBWWWWGG', 'RRRRGGWWYYGGOOOOBBYYWWBB', 'WRWRGGGGRYRYYOYOBBBBWOWO', 'YRYRGGGGOYOYWOWOBBBBWRWR', 'GGRRGOGOYYYYOOBBRBRBWWWW', 'BBRRGRGRYYYYOOGGOBOBWWWW', 'GGGGRRYYYYOOBBBBOOWWWWRR', 'GGGGOOYYWWOOBBBBRRWWYYRR', 'GOGOYYYYOBOBBRBRWWWWGRGR', 'GRGRYYYYOGOGBOBOWWWWBRBR', 'GGWWGYGYOOOOYYBBWBWBRRRR', 'GGYYBYBYOOOOWWBBWGWGRRRR', 'GGGGYYOOOOWWBBBBWWRRRRYY', 'GGGGYYRROOYYBBBBWWOORRWW', 'RGRGYYYYGOGOOBOBWWWWRBRB', 'OGOGYYYYBOBORBRBWWWWRGRG', 'YYGGYBYBOOOOBBWWGWGWRRRR', 'WWGGYGYGOOOOBBYYBWBWRRRR', 'YYYYGGOOOOBBWWWWBBRRRRGG', 'YYYYBBOORRBBWWWWGGRROOGG', 'YBYBOOOOBWBWWGWGRRRRYGYG', 'YGYGOOOOBYBYWBWBRRRRWGWG', 'YYRRYOYOBBBBOOWWRWRWGGGG', 'YYOOWOWOBBBBRRWWRYRYGGGG', 'YYYYOOBBBBRRWWWWRRGGGGOO', 'YYYYOOGGBBOOWWWWRRBBGGRR', 'GYGYOOOOYBYBBWBWRRRRGWGW', 'BYBYOOOOWBWBGWGWRRRRGYGY', 'OOYYOWOWBBBBWWRRYRYRGGGG', 'RRYYOYOYBBBBWWOOWRWRGGGG', 'OOOOYYBBBBWWRRRRWWGGGGYY', 'OOOOWWBBGGWWRRRRYYGGBBYY', 'OWOWBBBBWRWRRYRYGGGGOYOY', 'OYOYBBBBWOWORWRWGGGGRYRY', 'OOGGOBOBWWWWBBRRGRGRYYYY', 'OOBBRBRBWWWWGGRRGOGOYYYY', 'OOOOBBWWWWGGRRRRGGYYYYBB', 'OOOOBBYYWWBBRRRRGGWWYYGG', 'YOYOBBBBOWOWWRWRGGGGYRYR', 'WOWOBBBBRWRWYRYRGGGGYOYO', 'BBOOBRBRWWWWRRGGOGOGYYYY', 'GGOOBOBOWWWWRRBBRGRGYYYY', 'BBBBOOWWWWRRGGGGRRYYYYOO', 'BBBBRRWWYYRRGGGGOOYYWWOO', 'BRBRWWWWRGRGGOGOYYYYBOBO', 'BOBOWWWWRBRBGRGRYYYYGOGO', 'BBYYBWBWRRRRWWGGYGYGOOOO', 'BBWWGWGWRRRRYYGGYBYBOOOO', 'BBBBWWRRRRYYGGGGYYOOOOWW', 'BBBBWWOORRWWGGGGYYRROOYY', 'OBOBWWWWBRBRRGRGYYYYOGOG', 'RBRBWWWWGRGROGOGYYYYOBOB', 'WWBBWGWGRRRRGGYYBYBYOOOO', 'YYBBWBWBRRRRGGWWGYGYOOOO']

# ============================================================================
# get_arg() returns command line arguments.
# ============================================================================
def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default


# ============================================================================
# List of possible moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php
#
# Each move permutes the tiles in the current state to produce the new state
# ============================================================================

RULES = {
    "U": [2, 0, 3, 1, 20, 21, 6, 7, 4, 5, 10, 11,
          12, 13, 14, 15, 8, 9, 18, 19, 16, 17, 22, 23],
    "U'": [1, 3, 0, 2, 8, 9, 6, 7, 16, 17, 10, 11,
           12, 13, 14, 15, 20, 21, 18, 19, 4, 5, 22, 23],
    "R": [0, 9, 2, 11, 6, 4, 7, 5, 8, 13, 10, 15,
          12, 22, 14, 20, 16, 17, 18, 19, 3, 21, 1, 23],
    "R'": [0, 22, 2, 20, 5, 7, 4, 6, 8, 1, 10, 3,
           12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
    "F": [0, 1, 19, 17, 2, 5, 3, 7, 10, 8, 11, 9,
          6, 4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
    "F'": [0, 1, 4, 6, 13, 5, 12, 7, 9, 11, 8, 10,
           17, 19, 14, 15, 16, 3, 18, 2, 20, 21, 22, 23],
    "D": [0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 18, 19,
          14, 12, 15, 13, 16, 17, 22, 23, 20, 21, 6, 7],
    "D'": [0, 1, 2, 3, 4, 5, 22, 23, 8, 9, 6, 7,
           13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
    "L": [23, 1, 21, 3, 4, 5, 6, 7, 0, 9, 2, 11,
          8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
    "L'": [8, 1, 10, 3, 4, 5, 6, 7, 12, 9, 14, 11,
           23, 13, 21, 15, 17, 19, 16, 18, 20, 2, 22, 0],
    "B": [5, 7, 2, 3, 4, 15, 6, 14, 8, 9, 10, 11,
          12, 13, 16, 18, 1, 17, 0, 19, 22, 20, 23, 21],
    "B'": [18, 16, 2, 3, 4, 0, 6, 1, 8, 9, 10, 11,
           12, 13, 7, 5, 14, 17, 15, 19, 21, 23, 20, 22]
}

'''
sticker indices:

        0  1
        2  3
16 17   8  9   4  5  20 21
18 19  10 11   6  7  22 23
       12 13
       14 15

face colors:

    0
  4 2 1 5
    3

rules:
[ U , U', R , R', F , F', D , D', L , L', B , B']
'''


class Cube:

    def __init__(self, config="WWWW RRRR GGGG YYYY OOOO BBBB"):

        # ============================================================================
        # tiles is a string without spaces in it that corresponds to config
        # ============================================================================
        self.config = config
        self.tiles = config.replace(" ", "")

        self.depth = 0
        self.rule = ""
        self.parent = None

    def __str__(self):
        # ============================================================================
        # separates tiles into chunks of size 4 and inserts a space between them
        # for readability
        # ============================================================================
        chunks = [self.tiles[i:i + 4] + " " for i in range(0, len(self.tiles), 4)]
        return "".join(chunks)

    def __eq__(self, state):
        return (self.tiles == state.tiles) or (self.config == state.config)

    def toGrid(self):
        # ============================================================================
        # produces a string portraying the cube in flattened display form, i.e.,
        #
        #	   RW
        #	   GG
        #	BR WO YO GY
        #	WW OO YG RR
        #	   BB
        #	   BY
        # ============================================================================

        def part(face, portion):
            # ============================================================================
            # This routine converts the string corresponding to a single face to a
            # 2x2 grid
            #    face is in [0..5] if it exists, -1 if not
            #    portion is either TOP (=0) or BOTTOM (=1)
            # Example:
            # If state.config is "RWGG YOYG WOOO BBBY BRWW GYRR".
            #   part(0,TOP) is GW , part(0,BOTTOM) is WR, ...
            #   part(5,TOP) is BR , part(5,BOTTOM) is BB
            # ============================================================================

            result = "   "
            if face >= 0:
                offset = 4 * face + 2 * portion
                result = self.tiles[offset] + self.tiles[offset + 1] + " "
            return result

        TOP = 0
        BOTTOM = 1

        str = ""
        for row in [TOP, BOTTOM]:
            str += part(-1, row) + part(0, row) + \
                   part(-1, row) + part(-1, row) + "\n"

        for row in [TOP, BOTTOM]:
            str += part(4, row) + part(2, row) + \
                   part(1, row) + part(5, row) + "\n"

        for row in [TOP, BOTTOM]:
            str += part(-1, row) + part(3, row) + \
                   part(-1, row) + part(-1, row) + "\n"

        return str

    def applicableRules(self):
        return list(RULES.keys())

    def applyRule(self, rule):
        transformation = RULES[rule]
        temp = self.tiles
        new_state = ""
        for i in range(len(transformation)):
            new_state += temp[transformation[i]]
        self.tiles = new_state
        return self

    def goal(self):
        for i in range(6):
            c = self.tiles[i * 4]
            if self.tiles[i * 4 + 1] != c or self.tiles[i * 4 + 2] != c or self.tiles[i * 4 + 3] != c:
                return False
        return True


def determine_value(state):
    if state.tiles in ONE_AWAY:
        return 0
    return 3


def graphsearch(state, greedy=False):
    start = time.time()
    solution = None
    generated = 1
    expanded = 0

    explored = [str(state)]
    queue = [[], [], [], [copy.copy(state)]]
    while len(queue[3]) > 0:
        for i in range(len(queue)):
            if len(queue[i]) > 0:
                node = queue[i].pop(0)
                break
        if node.goal() is True:
            solution = node
            break
        expanded += 1
        for i in range(len(RULES.keys())):
            cube = copy.copy(node)
            cube.applyRule(list(RULES.keys())[i])
            if str(cube) not in explored:
                generated += 1
                cube.rule += list(RULES.keys())[i] + " "
                explored.append(str(cube))
                if not greedy:
                    value = 3
                else:
                    value = determine_value(cube)
                queue[value].append(cube)
    end = time.time()
    print("Time Elapsed: " + str(end - start))
    print("Nodes Generated: " + str(generated))
    print("Nodes Expanded: " + str(expanded))
    print()
    return solution

def backtrack(state, greedy = False):
    MAX_DEPTH = 4
    start = time.time()
    solution = None
    generated = 1
    expanded = 0

    explored = [str(state)]
    queue = [[], [], [], [copy.copy(state)]]
    while len(queue[3]) > 0:
        for i in range(len(queue)):
            if len(queue[i]) > 0:
                node = queue[i].pop()
                break
        if node.goal() is True:
            solution = node
            break
        expanded += 1
        if node.depth < MAX_DEPTH:
            for i in range(len(RULES.keys())):
                cube = copy.copy(node)
                cube.applyRule(list(RULES.keys())[i])
                cube.depth += 1
                if str(cube) not in explored:
                    generated += 1
                    cube.rule += list(RULES.keys())[i] + " "
                    explored.append(str(cube))
                    if not greedy:
                        value = 3
                    else:
                        value = determine_value(cube)
                    queue[value].append(cube)
    end = time.time()
    print("Time Elapsed: " + str(end - start))
    print("Nodes Generated: " + str(generated))
    print("Nodes Expanded: " + str(expanded))
    print()
    return solution



# --------------------------------------------------------------------------------
#  MAIN PROGRAM
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    CONFIG = get_arg(1)

    VERBOSE = get_arg(2)
    VERBOSE = (VERBOSE == "verbose" or VERBOSE == "v")
    if VERBOSE:
        print("Verbose mode:")

    random.seed(2) # use clock to randomize RNG

    # Randomize the cube
    state = Cube()
    for i in range(8):
        state = state.applyRule(list(RULES.keys())[random.randrange(12)])

    print(state.toGrid())

    solution = backtrack(state)
    if solution is not None:
        for r in solution.rule.strip().split(" "):
            print("Move: " + r)
            state.applyRule(r)
            print(state.toGrid())
    else:
        print("Solution Not Found")