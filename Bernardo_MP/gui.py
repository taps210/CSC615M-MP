import tkinter as tk
from tkinter import ttk, scrolledtext
from abstract_machine import AbstractMachine

class MachineGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Abstract Machine Interpreter")
        self.root.geometry("1000x800")
        
        # Machine Definition
        self.definition_label = tk.Label(self.root, text="Machine Definition:")
        self.definition_label.pack()
        self.definition_text = scrolledtext.ScrolledText(self.root, height=15, width=120)
        self.definition_text.pack()
        
        # Input String
        self.input_label = tk.Label(self.root, text="Input String:")
        self.input_label.pack()
        self.input_entry = tk.Entry(self.root, width=120)
        self.input_entry.pack()
        
        # Execute Button
        self.execute_btn = tk.Button(self.root, text="Execute", command=self.execute_machine)
        self.execute_btn.pack(pady=10)
        
        # Output Display
        self.output_notebook = ttk.Notebook(self.root)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Log Tab
        self.log_tab = tk.Frame(self.output_notebook)
        self.log_text = scrolledtext.ScrolledText(self.log_tab, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.output_notebook.add(self.log_tab, text="Execution Log")

    def clear_output(self):
        self.log_text.delete(1.0, tk.END)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def execute_machine(self):
        self.clear_output()
        
        machine_definition = self.definition_text.get("1.0", tk.END).strip()
        input_string = self.input_entry.get().strip()
        
        def output_handler(text):
            self.root.after(0, self.log_message, text)
            
        machine = AbstractMachine(machine_definition, output_handler)
        machine.parse_definition()
        machine.execute(input_string)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MachineGUI()
    app.run()