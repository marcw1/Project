import operator


class Move:
    # old and new positions as tuples
    old = None
    new = None
    full = None

    def __init__(self, old, new):
        self.old = old
        self.new = new
        self.full = (self.old, self.new)

    # "(old) -> (new)" in weird backwards format (col, row)
    def __str__(self):
        return "%s -> %s" % \
               (self.old, self.new)

    # returns all positions that are one step away (N, E, S, W),
    # or just the step in that particular direction 0-3
    @classmethod
    def oneStep(cls, loc, direc=None):
        steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if direc == None:
            moves = []
            for step in steps:
                # adds step to loc
                moves.append(tuple(map(operator.add, loc, step)))
            return moves
        else:
            move = tuple(map(operator.add, loc, steps[direc]))
            return move
