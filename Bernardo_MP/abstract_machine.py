from memory_models import Stack, Queue, Tape, Tape2D
import re

class AbstractMachine:
    def __init__(self, definition):
        self.definition = definition
        self.stacks = {}
        self.queues = {}
        self.tapes = {}
        self.states = {}
        self.current_state = None

    def parse_definition(self):
        lines = self.definition.split('\n')
        data_section = False
        logic_section = False
        for line in lines:
            if line.strip() == '.DATA':
                data_section = True
                logic_section = False
            elif line.strip() == '.LOGIC':
                data_section = False
                logic_section = True
            elif data_section:
                self.parse_data_line(line)
            elif logic_section:
                self.parse_logic_line(line)

    def parse_data_line(self, line):
        if line.startswith('STACK'):
            stack_name = line.split()[1]
            self.stacks[stack_name] = Stack(stack_name)
        elif line.startswith('QUEUE'):
            queue_name = line.split()[1]
            self.queues[queue_name] = Queue(queue_name)
        elif line.startswith('TAPE'):
            tape_name = line.split()[1]
            self.tapes[tape_name] = Tape(tape_name)
        elif line.startswith('2D_TAPE'):
            tape_name = line.split()[1]
            self.tapes[tape_name] = Tape2D(tape_name)

    def parse_logic_line(self, line):
        parts = line.split(']')
        state_name = parts[0].strip()
        commands = parts[1].strip()
        self.states[state_name] = commands

    def execute(self, input_string):
        # Initialize the first tape with the input string
        if self.tapes:
            input_tape_name = list(self.tapes.keys())[0]
            self.tapes[input_tape_name].write_input(input_string)
        else:
            self.tapes["Input"] = Tape("Input")
            self.tapes["Input"].write_input(input_string)

        # Set the initial state
        self.current_state = list(self.states.keys())[0]

        print(input_string)
        while True:
            #print(self.tapes["Input"].read(), self.current_state)
            #print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items)
            print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items, self.stacks["S2"].items)
            #print(''.join(self.tapes[input_tape_name].tape[key] for key in sorted(self.tapes[input_tape_name].tape)), self.current_state)
            command = self.states[self.current_state]
            if command.startswith('SCAN RIGHT'):
                self.scan_right(command)
            elif command.startswith('SCAN LEFT'):
                self.scan_left(command)
            elif command.startswith('SCAN'):
                self.scan_right(command)
            elif command.startswith('PRINT'):
                self.print(command)
            elif command.startswith('READ'):
                self.read(command)
            elif command.startswith('WRITE'):
                self.write(command)
            elif command.startswith('RIGHT'):
                self.right(command)
            elif command.startswith('LEFT'):
                self.left(command)
            elif command.startswith('UP'):
                self.up(command)
            elif command.startswith('DOWN'):
                self.down(command)

            if self.current_state in ['accept', 'reject']:
                print(self.current_state)
                break

    def scan_right(self, command):
        # Extract the symbol and state transitions from the command
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions]
        transitions = [[x.strip() for x in pair] for pair in transitions]
        
        # Read the current symbol from the input tape
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_right()
        current_symbol = self.tapes[input_tape_name].read()

        # Find the matching transition for the current symbol
        for transition in transitions:
            symbol = transition[0].strip()
            next_state = transition[1].strip()
            if symbol == current_symbol:
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'

    def scan_left(self, command):
        # Extract the symbol and state transitions from the command
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions]
        transitions = [[x.strip() for x in pair] for pair in transitions]
        
        # Read the current symbol from the input tape
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_left()
        current_symbol = self.tapes[input_tape_name].read()

        # Find the matching transition for the current symbol
        for transition in transitions:
            symbol = transition[0].strip()
            next_state = transition[1].strip()
            if symbol == current_symbol:
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'


    def print(self, command):
        # Extract the symbol to print from the command
        symbol_to_print = command.replace('PRINT(', '').replace(')', '')

        # Print the symbol (for now, just output to console)
        print(symbol_to_print)

    def read(self, command):
        # Extract the memory object from the command
        memory_object = command.split('(')[1].split(')')[0].strip()

        # Read a symbol from the specified memory object
        if memory_object in self.stacks:
            symbol = self.stacks[memory_object].pop()
        elif memory_object in self.queues:
            symbol = self.queues[memory_object].dequeue()
        else:
            symbol = None

        # Update the current state based on the symbol read
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions[1:]]
        transitions = [[x.strip() for x in pair] for pair in transitions]
        for transition in transitions:
            read_symbol = transition[0].strip()
            next_state = transition[1].strip()

            if read_symbol == symbol:
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'

    def write(self, command):
        # Extract the memory object from the command
        memory_object = command.split('(')[1].split(')')[0].strip()

        # Extract the symbol to write and the next state
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions[1:]]
        transitions = [[x.strip() for x in pair] for pair in transitions]

        write_symbol = transitions[0][0].strip()
        next_state = transitions[0][1].strip()

        #Write the symbol to the specified memory object
        if memory_object in self.stacks:
            self.stacks[memory_object].push(write_symbol)
        elif memory_object in self.queues:
            self.queues[memory_object].enqueue(write_symbol)

        # Update the current state
        self.current_state = next_state
        return

    def right(self, command):
        # Extract the tape name from the command
        tape_name = command.split('(')[1].split(')')[0].strip()

        # Read the current symbol from the tape
        self.tapes[tape_name].move_right()
        current_symbol = self.tapes[tape_name].read()

        # Extract the symbol/replacement and state transitions
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions[1:]]
        transitions = [[x.strip() for x in pair] for pair in transitions]
        for transition in transitions:
            symbol, replacement = transition[0].split('/')
            symbol = symbol.strip()
            replacement = replacement.strip()
            next_state = transition[1].strip()

            if current_symbol == symbol:
                # Write the replacement symbol and move the tape head right
                self.tapes[tape_name].write(replacement)
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'

    def left(self, command):
        # Extract the tape name from the command
        tape_name = command.split('(')[1].split(')')[0].strip()

        # Read the current symbol from the tape
        self.tapes[tape_name].move_left()
        current_symbol = self.tapes[tape_name].read()

        # Extract the symbol/replacement and state transitions
        transitions = re.findall(r'\((.*?)\)', command)
        transitions = [item.split(',') for item in transitions[1:]]
        transitions = [[x.strip() for x in pair] for pair in transitions]
        for transition in transitions:
            symbol, replacement = transition[0].split('/')
            symbol = symbol.strip()
            replacement = replacement.strip()
            next_state = transition[1].strip()

            if current_symbol == symbol:
                # Write the replacement symbol and move the tape head right
                self.tapes[tape_name].write(replacement)
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'

    def up(self, command):
        # Extract the 2D tape name from the command
        tape_name = command.split('(')[1].split(')')[0]

        # Extract the symbol/replacement and state transitions
        transitions = command.split(')')[1].split(',')
        for transition in transitions:
            symbol_replacement, next_state = transition.split(',')
            symbol, replacement = symbol_replacement.split('/')
            symbol = symbol.strip()
            replacement = replacement.strip()
            next_state = next_state.strip()

            # Read the current symbol from the 2D tape
            current_symbol = self.tapes[tape_name].read()

            if current_symbol == symbol:
                # Write the replacement symbol and move the tape head up
                self.tapes[tape_name].write(replacement)
                self.tapes[tape_name].move_up()
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'

    def down(self, command):
        # Extract the 2D tape name from the command
        tape_name = command.split('(')[1].split(')')[0]

        # Extract the symbol/replacement and state transitions
        transitions = command.split(')')[1].split(',')
        for transition in transitions:
            symbol_replacement, next_state = transition.split(',')
            symbol, replacement = symbol_replacement.split('/')
            symbol = symbol.strip()
            replacement = replacement.strip()
            next_state = next_state.strip()

            # Read the current symbol from the 2D tape
            current_symbol = self.tapes[tape_name].read()

            if current_symbol == symbol:
                # Write the replacement symbol and move the tape head down
                self.tapes[tape_name].write(replacement)
                self.tapes[tape_name].move_down()
                self.current_state = next_state
                return

        # If no matching transition is found, reject the input
        self.current_state = 'reject'