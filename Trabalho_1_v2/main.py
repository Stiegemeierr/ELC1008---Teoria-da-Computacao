import re
from mt_reversivel import R_turing_machine as TM


def parse_transition(line):
    match = re.match(r'\((\d+),([^\)]+)\)=\((\d+),([^\),]+),([^\)]+)\)', line)
    if not match:
        raise ValueError(f"Formato inválido: {line}")
    return int(match.group(1)), match.group(2), int(match.group(3)), match.group(4), match.group(5)


def load_machine(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    _, _, _, num_transitions = map(int, lines[0].split())
    states = list(map(int, lines[1].split()))
    input_alphabet = lines[2].split()
    tape_alphabet = lines[3].split()
    transitions = lines[4:4 + num_transitions]
    input_str = lines[4 + num_transitions]

    tm = TM()
    tm.setup(states, input_alphabet, tape_alphabet, states[0], states[-1])
    for line in transitions:
        tm.add_transition(*parse_transition(line))
    tm.define_input(input_str)
    return tm


def print_menu():
    print("\nComandos disponíveis:")
    print("  next   - Executar próximo passo")
    print("  undo   - Desfazer último passo")
    print("  run    - Executar tudo de uma vez")
    print("  exit   - Sair do programa")


def main():
    tm = load_machine('input.txt')
    print("Máquina de Turing carregada com sucesso.")
    print_menu()

    while True:
        cmd = input("\n>> ").strip().lower()
        if cmd == "next":
            tm.step()
        elif cmd == "undo":
            tm.undo()
        elif cmd == "run":
            tm.run_all()
        elif cmd == "exit":
            break
        else:
            print("Comando inválido.")
        tm.print_tape()


if __name__ == "__main__":
    main()
