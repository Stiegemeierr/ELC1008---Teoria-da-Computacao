import tkinter as tk
from tkinter import messagebox
from mt_reversivel import RTM
import re

TAPE_VIEW_LENGTH = 20

def parse_transition(line):
    match = re.match(r'\((\d+),([^\)]+)\)=\((\d+),([^\),]+),([^\)]+)\)', line)
    if not match:
        raise ValueError(f"Formato inválido: {line}")
    return int(match.group(1)), match.group(2), int(match.group(3)), match.group(4), match.group(5)


def load_machine(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    n_transitions = int(lines[0].split()[3])
    states = list(map(int, lines[1].split()))
    input_alphabet = lines[2].split()
    tape_alphabet = lines[3].split()
    transitions = lines[4:4 + n_transitions]
    input_str = lines[4 + n_transitions]

    tm = RTM()
    tm.setup(states, input_alphabet, tape_alphabet, states[0], states[-1])
    for line in transitions:
        tm.add_transition(*parse_transition(line))
    tm.define_input(input_str)
    return tm


class RTMSimulatorGUI:
    def __init__(self, root):
        self.setup(root)


    def setup(self, root):
        self.root = root
        self.root.title("Máquina de Turing Reversível")
        self.tm = load_machine("input.txt")
        self.tm.set_message_callback(self.show_message)

        self.state_label = tk.Label(root, text="Estado atual: q0", font=("Arial", 14, "bold"))
        self.state_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))

        self.tape_frames = {}
        self.tape_labels = {}

        for idx, name in enumerate(["Input", "History", "Output"]):
            frame = tk.LabelFrame(root, text=name, padx=5, pady=5, font=("Arial", 10, "bold"))
            frame.grid(row=idx + 1, column=0, columnspan=4, padx=10, pady=5, sticky="w")
            self.tape_frames[name] = frame
            self.tape_labels[name] = []
            for j in range(TAPE_VIEW_LENGTH):
                label = tk.Label(frame, text=" ", width=3, height=2, relief="ridge", borderwidth=2, font=("Courier", 14), bg="white")
                label.grid(row=0, column=j, padx=1, pady=1)
                self.tape_labels[name].append(label)

        self.btn_next = tk.Button(root, text="Next", width=12, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=self.step)
        self.btn_next.grid(row=5, column=0, padx=10, pady=15)

        self.btn_undo = tk.Button(root, text="Undo", width=12, bg="#2196F3", fg="white", font=("Arial", 11, "bold"), command=self.undo)
        self.btn_undo.grid(row=5, column=1, padx=10, pady=15)

        self.btn_run = tk.Button(root, text="Run", width=12, bg="#FF9800", fg="white", font=("Arial", 11, "bold"), command=self.run_all)
        self.btn_run.grid(row=5, column=2, padx=10, pady=15)

        self.btn_exit = tk.Button(root, text="Exit", width=12, bg="#f44336", fg="white",  font=("Arial", 11, "bold"), command=root.destroy)
        self.btn_exit.grid(row=5, column=3, padx=10, pady=15)

        self.message_label = tk.Label(root, text="", font=("Arial", 12), fg="red", anchor="w", justify="left")
        self.message_label.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="w")

        self.update_view()


    def show_message(self, message):
        self.message_label.config(text=message)


    def update_view(self):
        self.state_label.config(text=f"Estado atual: q{self.tm.current_state}")

        tapes = {
            "Input": (self.tm.input_tape.content, self.tm.input_tape.head_position),
            "History": (self.tm.history_tape.content, self.tm.history_tape.head_position),
            "Output": (self.tm.output_tape.content, self.tm.output_tape.head_position)
        }

        for name, (content, head_pos) in tapes.items():
            for i in range(TAPE_VIEW_LENGTH):
                value = content[i] if i < len(content) else ' '
                label = self.tape_labels[name][i]
                label['text'] = value
                if i == head_pos:
                    label['bg'] = "#D1C4E9"
                    label['relief'] = "solid"
                else:
                    label['bg'] = "white"
                    label['relief'] = "ridge"


    def step(self):
        if self.tm.finished_stage1:
            self.show_message("Todos os passos ja foram executados.")
            return
        self.tm.step()
        if self.tm.finished_stage1:
            self.tm.stage2()
            self.tm.stage3()
        self.update_view()


    def undo(self):
        self.tm.undo()
        self.update_view()


    def run_all(self):
        if self.tm.finished_stage1:
            self.show_message("Todos os passos ja foram executados.")
            return
        self.tm.run_all()
        self.update_view()


if __name__ == "__main__":
    root = tk.Tk()
    app = RTMSimulatorGUI(root)
    root.mainloop()
