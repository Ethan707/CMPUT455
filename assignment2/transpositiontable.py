class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, code, result):
        # result is a tuple: (score, best_move)
        self.table[code] = result

    def lookup(self, code):
        return self.table.get(code)
