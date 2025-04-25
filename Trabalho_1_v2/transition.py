class Transition:
    def setup(self, next_state, write_symbol, direction):
        self.next_state = next_state
        self.write_symbol = write_symbol
        self.direction = direction
