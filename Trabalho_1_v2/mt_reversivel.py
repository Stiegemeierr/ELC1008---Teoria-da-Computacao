from tape import Tape
from transition import Transition

class RTM:
    def __init__(self):
        self.message_callback = None
        self.undo_stack = []
        self.saved_history = []
        self.saved_history_head = 0
        self.stage = 1
        self.finished_stage1 = False

    def setup(self, states, input_alphabet, tape_alphabet, start_state, accept_state):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.current_state = start_state
        self.accept_state = accept_state

        self.input_tape = Tape()
        self.history_tape = Tape()
        self.output_tape = Tape()

        self.input_tape.setup()
        self.history_tape.setup()
        self.output_tape.setup()

        self.transitions = {}
        self.input_string = ""

    def set_message_callback(self, callback):
        self.message_callback = callback

    def define_input(self, input_str):
        self.input_string = input_str
        for i, char in enumerate(input_str):
            self.input_tape.content[i] = char

    def add_transition(self, from_state, read_symbol, to_state, write_symbol, move_direction):
        transition = Transition()
        transition.setup(to_state, write_symbol, move_direction)
        self.transitions[(from_state, read_symbol)] = transition

    def get_key(self):
        return (self.current_state, self.input_tape.content[self.input_tape.head_position])

    def get_transition(self, key):
        return self.transitions.get(key, Transition())

    def step(self):
        if self.stage != 1 or self.finished_stage1:
            self._notify("Cannot execute more steps.")
            return

        key = self.get_key()
        transition = self.get_transition(key)

        if getattr(transition, "direction", 'N') == 'N':
            self._notify("Error: no valid transition.")
            self.finished_stage1 = True
            return

        self._apply_transition(key, transition)
        self._notify(f"Current state: {self.current_state}")

        if self.current_state == self.accept_state:
            self.finished_stage1 = True
            self._notify("Stage 1 completed.")

    def undo(self):
        if not self.undo_stack:
            self._notify("Nothing to undo.")
            return

        if all(cell == 'B' for cell in self.history_tape.content) and self.saved_history:
            self.history_tape.content = self.saved_history.copy()
            self.history_tape.head_position = self.saved_history_head

        state, pos, original_symbol, output_snapshot = self.undo_stack.pop()

        self.input_tape.head_position = pos
        self.input_tape.content[pos] = original_symbol
        self.output_tape.content = output_snapshot.copy()
        self.current_state = state

        self.history_tape.head_position -= 2
        self.history_tape.content[self.history_tape.head_position] = 'B'
        self.history_tape.content[self.history_tape.head_position + 1] = 'B'

        self.finished_stage1 = False
        self._notify("Step undone.")

    def run_all(self):
        if self.finished_stage1:
            self._notify("All steps already executed.")
            return

        self.stage1()
        self.stage2()
        self.stage3()

    def stage1(self):
        while self.current_state != self.accept_state:
            key = self.get_key()
            transition = self.get_transition(key)

            if getattr(transition, "direction", 'N') == 'N':
                self._notify("Error during transition.")
                break

            self._apply_transition(key, transition)

        self.finished_stage1 = True
        self._notify(f"Stage 1 completed. Final state: {self.current_state}")

    def stage2(self):
        self.output_tape.content = self.input_tape.content.copy()
        self._notify("Stage 2 completed: Output copied.")

    def stage3(self):
        self._notify("Stage 3: Reversing transitions...")

        self.saved_history = self.history_tape.content.copy()
        self.saved_history_head = self.history_tape.head_position

        for i in range(self.history_tape.head_position - 2, -1, -2):
            from_state = int(self.history_tape.content[i])
            read_symbol = self.history_tape.content[i + 1]
            key = (from_state, read_symbol)

            reversed_transition = self._reverse_transition(key)

            if reversed_transition:
                self._apply_reverse_transition(reversed_transition)
                self.current_state = from_state

            self.history_tape.content[i] = 'B'
            self.history_tape.content[i + 1] = 'B'

    def _apply_transition(self, key, transition):
        self.undo_stack.append((
            self.current_state,
            self.input_tape.head_position,
            key[1],
            self.output_tape.content.copy()
        ))

        self.history_tape.content[self.history_tape.head_position] = str(key[0])
        self.history_tape.head_position += 1
        self.history_tape.content[self.history_tape.head_position] = key[1]
        self.history_tape.head_position += 1

        self.input_tape.content[self.input_tape.head_position] = transition.write_symbol

        if transition.direction == 'R':
            self.input_tape.head_position += 1
        elif transition.direction == 'L':
            self.input_tape.head_position -= 1

        self.current_state = transition.next_state

    def _reverse_transition(self, key):
        transition = self.get_transition(key)

        if getattr(transition, "direction", 'N') == 'N':
            return None

        rev_direction = 'L' if transition.direction == 'R' else 'R'
        rev_transition = (transition.next_state, transition.write_symbol, key[0], rev_direction)

        return rev_transition

    def _apply_reverse_transition(self, rev_transition):
        from_state, write_symbol, to_state, move_dir = rev_transition

        if move_dir == 'R':
            self.input_tape.head_position += 1
        elif move_dir == 'L':
            self.input_tape.head_position -= 1

        self.input_tape.content[self.input_tape.head_position] = write_symbol
        self._notify(f"Reversed transition: wrote {write_symbol}.")

    def _notify(self, message):
        if self.message_callback:
            self.message_callback(message)
