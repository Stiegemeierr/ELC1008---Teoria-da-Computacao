import tkinter as tk
from tkinter import messagebox
import re
from mt_reversivel import RTM

TAPE_VIEW_LENGTH = 20

def parse_transition(line):
    match = re.match(r'\((\d+),([^\)]+)\)=\((\d+),([^\),]+),([^\)]+)\)', line)
    if not match:
        raise ValueError(f"Invalid format: {line}")
    return int(match.group(1)), match.group(2), int(match.group(3)), match.group(4), match.group(5)

def load_machine(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    n_transitions = int(lines[0].split()[3])
    states = list(map(int, lines[1].split()))
    input_alphabet = lines[2].split()
    tape_alphabet = lines[3].split()
    transitions = lines[4:4 + n_transitions]
    input_string = lines[4 + n_transitions]

    tm = RTM()
    tm.setup(states, input_alphabet, tape_alphabet, states[0], states[-1])

    for transition in transitions:
        tm.add_transition(*parse_transition(transition))

    tm.define_input(input_string)
    return tm

class RTMSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversible Turing Machine")
        self.tm = load_machine("input.txt")
        self.tm.set_message_callback(self.display_message)
        self.create_widgets()
        self.update_view()

    def create_widgets(self):
        self.tape_frames = {}
        self.tape_labels = {}

        for idx, tape_name in enumerate(["Input", "History", "Output"]):
            frame = tk.LabelFrame(self.root, text=tape_name, padx=5, pady=5, font=("Arial", 10, "bold"))
            frame.grid(row=idx + 1, column=0, columnspan=4, padx=10, pady=5, sticky="w")
            self.tape_frames[tape_name] = frame
            self.tape_labels[tape_name] = []

            for i in range(TAPE_VIEW_LENGTH):
                label = tk.Label(frame, text=" ", width=3, height=2, relief="ridge", borderwidth=2,
                                 font=("Courier", 14), bg="white")
                label.grid(row=0, column=i, padx=1, pady=1)
                self.tape_labels[tape_name].append(label)

        buttons = [
            ("Next", self.step, "#4CAF50"),
            ("Undo", self.undo, "#2196F3"),
            ("Run", self.run_all, "#FF9800"),
            ("Exit", self.root.destroy, "#f44336")
        ]

        for idx, (text, command, color) in enumerate(buttons):
            btn = tk.Button(self.root, text=text, width=12, bg=color, fg="white", font=("Arial", 11, "bold"), command=command)
            btn.grid(row=5, column=idx, padx=10, pady=15)

        self.message_label = tk.Label(self.root, text="Current state: q0", font=("Arial", 14, "bold"))
        self.message_label.grid(row=0, column=0, columnspan=4, pady=(10, 5))

    def display_message(self, message):
        self.message_label.config(text=message)

    def update_view(self):
        tapes = {
            "Input": (self.tm.input_tape.content, self.tm.input_tape.head_position),
            "History": (self.tm.history_tape.content, self.tm.history_tape.head_position),
            "Output": (self.tm.output_tape.content, self.tm.output_tape.head_position)
        }

        for tape_name, (content, head_pos) in tapes.items():
            for i in range(TAPE_VIEW_LENGTH):
                label = self.tape_labels[tape_name][i]
                label['text'] = content[i] if i < len(content) else ' '
                if i == head_pos:
                    label.config(bg="#D1C4E9", relief="solid")
                else:
                    label.config(bg="white", relief="ridge")

    def step(self):
        if self.tm.finished_stage1:
            self.display_message("All steps already executed.")
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
            self.display_message("All steps already executed.")
            return
        self.tm.run_all()
        self.update_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = RTMSimulatorGUI(root)
    root.mainloop()
