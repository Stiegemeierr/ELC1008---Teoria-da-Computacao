from tape import Tape
from transition import Transition


class R_turing_machine:
    def setup(self, states, input_alphabet, tape_alphabet, start_state, accept_state):
        self.stage = 1
        self.finished_stage1 = False
        self.undo_pointer = None
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.current_state = start_state
        self.final_state = accept_state

        self.input_tape = Tape()
        self.input_tape.setup()

        self.history_tape = Tape()
        self.history_tape.setup()

        self.output_tape = Tape()
        self.output_tape.setup()

        self.transitions = {}
        self.input = ""


    def define_input(self, input_str):
        self.input = input_str
        for i, char in enumerate(input_str):
            self.input_tape.content[i] = char


    def add_transition(self, state, read_symbol, next_state, write_symbol, direction):
        t = Transition()
        t.setup(next_state, write_symbol, direction)
        self.transitions[(state, read_symbol)] = t


    def get_actual_key(self):
        read_symbol = self.input_tape.content[self.input_tape.head_position]
        return (self.current_state, read_symbol)


    def get_transition(self, key):
        return self.transitions.get(key, Transition())


    def step(self):
        if self.stage != 1 or self.finished_stage1:
            print("Não é possível executar mais passos.")
            return False

        key = self.get_actual_key()
        t = self.get_transition(key)
        if getattr(t, "direction", 'N') == 'N':
            print("Erro: transição não existente.")
            self.finished_stage1 = True
            return False

        self.history_tape.content[self.history_tape.head_position] = str(key[0])
        self.history_tape.head_position += 1
        self.history_tape.content[self.history_tape.head_position] = key[1]
        self.history_tape.head_position += 1

        self.input_tape.content[self.input_tape.head_position] = t.write_symbol
        self.undo_pointer = (self.current_state, self.input_tape.head_position, key[1])

        if t.direction == 'R':
            self.input_tape.head_position += 1
        elif t.direction == 'L':
            self.input_tape.head_position -= 1

        self.current_state = t.next_state
        print(f"Estado atual: {self.current_state}")
        if self.current_state == self.final_state:
            print("Estágio 1 finalizado.")
            self.finished_stage1 = True
        return True


    def undo(self):
        if self.undo_pointer is None:
            print("Nada para desfazer.")
            return

        state, pos, original_symbol = self.undo_pointer
        self.input_tape.head_position = pos
        self.input_tape.content[pos] = original_symbol
        self.current_state = state
        self.history_tape.head_position -= 2
        self.history_tape.content[self.history_tape.head_position] = 'B'
        self.history_tape.content[self.history_tape.head_position + 1] = 'B'
        self.finished_stage1 = False
        self.undo_pointer = None
        print("Última transição desfeita.")


    def run_all(self):
        self.stage1()
        self.stage2()
        self.stage3()


    def stage1(self):
        while self.current_state != self.final_state:
            symbol = self.input_tape.content[self.input_tape.head_position]
            print(f"\nEstado atual: {self.current_state}, Simbolo lido: {symbol}")
            success = self.apply_transition(self.breaks_quintuple_apart(
                self.get_actual_key(), self.get_transition(self.get_actual_key())))
            if not success:
                print("Erro durante a aplicação da transição.")
                break
        print(f"\nFinal do estagio 1. Estado final: {self.current_state}")
        self.print_tape()


    def stage2(self):
        self.output_tape.content = self.input_tape.content[:]
        print("Final do estagio 2. Saída copiada para fita 3.")
        self.print_tape()


    def stage3(self):
        print("Estágio 3: Inversão das transições.")
        for i in range(self.history_tape.head_position - 2, -1, -2):
            key_state = int(self.history_tape.content[i])
            key_symbol = self.history_tape.content[i + 1]
            key = (key_state, key_symbol)
            reversed_transition = self.reverts_quadruple(
                self.breaks_quintuple_apart(key, self.get_transition(key)))
            print(f"\nEstado atual: {self.current_state}, Próximo Estado: {key_state}")
            print(f"Símbolo lido: {self.input_tape.content[self.input_tape.head_position]}")
            self.apply_reversed_transition(reversed_transition)
            self.current_state = key_state
            self.history_tape.content[i] = 'B'
            self.history_tape.content[i + 1] = 'B'
        self.print_tape()


    def breaks_quintuple_apart(self, current, t):
        first = (current[0], current[1], t.next_state, t.write_symbol)
        second = (t.next_state, t.write_symbol, t.next_state, t.direction)
        return first, second


    def reverts_quadruple(self, quads):
        first, second = quads
        rev_first = (second[2], second[1], second[0], 'L' if second[3] == 'R' else 'R')
        rev_second = (first[2], first[1], first[0], first[3])
        return rev_first, rev_second


    def apply_transition(self, transition):
        if not (0 <= self.input_tape.head_position < len(self.input_tape.content)):
            print("Erro: Cabeçote fora dos limites da fita!")
            return False
        if transition[0][3] == 'N':
            print("Erro: transição não existente.")
            return False

        key_move = self.get_actual_key()
        self.history_tape.content[self.history_tape.head_position] = str(key_move[0])
        self.history_tape.head_position += 1
        self.history_tape.content[self.history_tape.head_position] = key_move[1]
        self.history_tape.head_position += 1

        first, second = transition
        self.input_tape.content[self.input_tape.head_position] = first[3]

        if second[3] == 'L':
            self.input_tape.head_position -= 1
        elif second[3] == 'R':
            self.input_tape.head_position += 1

        self.current_state = second[2]
        print(f"Símbolo escrito: {self.input_tape.content[self.input_tape.head_position]}, Próximo Estado: {self.current_state}")
        return True


    def apply_reversed_transition(self, transition):
        first, second = transition
        if first[3] == 'L':
            self.input_tape.head_position -= 1
        elif first[3] == 'R':
            self.input_tape.head_position += 1

        self.input_tape.content[self.input_tape.head_position] = second[1]
        print(f"Símbolo escrito: {self.input_tape.content[self.input_tape.head_position]}")
        return True


    def print_tape(self):
        print("\nInput:  ", ''.join(c for c in self.input_tape.content if c != 'B'))
        print("History:", ''.join(c for c in self.history_tape.content if c != 'B'))
        print("Output: ", ''.join(c for c in self.output_tape.content if c != 'B'))
        print()
