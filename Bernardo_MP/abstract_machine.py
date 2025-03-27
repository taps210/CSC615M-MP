from memory_models import Stack, Queue, Tape, Tape2D
import re
import copy
from collections import Counter

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
        if self.tapes:
            input_tape_name = list(self.tapes.keys())[0]
            self.tapes[input_tape_name].write_input(input_string)
        else:
            self.tapes["Input"] = Tape("Input")
            self.tapes["Input"].write_input(input_string)

        self.current_state = list(self.states.keys())[0]

        print(input_string)
        self.execute_recursive()
        return
    
    def execute_recursive(self):
        #print(self.tapes["Input"].read(), self.current_state)
        #print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items)
        print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items, self.stacks["S2"].items)
        #print(''.join(self.tapes[input_tape_name].tape[key] for key in sorted(self.tapes[input_tape_name].tape)), self.current_state)

        if self.current_state in ['accept', 'reject', 'halt']:
            print(self.current_state)
            return
        
        command = self.states[self.current_state]
        logic = ''.join(command).split(' ')[0].split('(')[0]
        possible_transitions = self.get_transitions(command, logic)

        if len(possible_transitions) == 1:
            self.apply_transition(possible_transitions[0], logic, command)
            self.execute_recursive()
        else:
            for index, transition in enumerate(possible_transitions):
                if index == 0:
                    self.apply_transition(transition, logic, command)
                    self.execute_recursive()
                else:
                    # Create a copy of the current machine state
                    machine_copy = copy.deepcopy(self)
                    # Apply the transition
                    machine_copy.apply_transition(transition, logic, command)
                    # Recursively execute from the new state
                    machine_copy.execute_recursive()
        return
    
    def get_transitions(self, command, logic):
        # Extract the symbol and state transitions from the command
        transitions = re.findall(r'\((.*?)\)', command)
        if logic == 'SCAN' or logic == 'SCAN RIGHT' or logic == 'SCAN LEFT':
            transitions = [item.split(',') for item in transitions]
        else:
            transitions = [item.split(',') for item in transitions[1:]]
        transitions = [[x.strip() for x in pair] for pair in transitions]

        possible_transitions = []
        if logic == 'READ':
            memory_object = command.split('(')[1].split(')')[0].strip()
            for transition in transitions:
                if memory_object in self.stacks:
                    symbol = self.stacks[memory_object].get_head()
                elif memory_object in self.queues:
                    symbol = self.queues[memory_object].get_head()
                if transition[0] == symbol:
                    possible_transitions.append(transition)
        elif logic == 'WRITE' or logic == 'PRINT':
            for transition in transitions:
                possible_transitions.append(transition)
        else:
            input_tape_name = list(self.tapes.keys())[0]
            if logic == 'SCAN LEFT' or logic == 'LEFT':
                current_symbol = self.tapes[input_tape_name].read_left()
            elif logic == 'SCAN' or logic == 'SCAN RIGHT' or logic == 'RIGHT':
                current_symbol = self.tapes[input_tape_name].read_right()
            #elif command.startswith('UP'):
            #elif command.startswith('DOWN'):

            for transition in transitions:
                symbol = transition[0].strip()
                if symbol == current_symbol:
                    possible_transitions.append(transition)
            
        if not possible_transitions:
            self.current_state == 'reject'

        return possible_transitions

    def apply_transition(self, transition, logic, command):
        # Apply the given transition to the machine state
        if logic == 'SCAN LEFT':
            self.scan_left(transition)
        elif logic == 'SCAN' or logic == 'SCAN RIGHT':
            self.scan_right(transition)
        elif logic == 'WRITE':
            self.write(transition, command)
        elif logic == 'READ':
            self.read(transition, command)
        # Add similar cases for other commands
            
    def scan_right(self, transition):
        next_state = transition[1]
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_right()
        self.current_state = next_state
        return

    def scan_left(self, transition):
        next_state = transition[1]
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_left()
        self.current_state = next_state
        return

    def print(self, command):
        # Extract the symbol to print from the command
        symbol_to_print = command.replace('PRINT(', '').replace(')', '')

        # Print the symbol (for now, just output to console)
        print(symbol_to_print)
        return

    def read(self, transition, command):
        memory_object = command.split('(')[1].split(')')[0].strip()
        next_state = transition[1].strip()

        if memory_object in self.stacks:
            symbol = self.stacks[memory_object].pop()
        elif memory_object in self.queues:
            symbol = self.queues[memory_object].dequeue()

        self.current_state = next_state
        return

    def write(self, transition, command):
        memory_object = command.split('(')[1].split(')')[0].strip()
        write_symbol = transition[0].strip()
        next_state = transition[1].strip()

        if memory_object in self.stacks:
            self.stacks[memory_object].push(write_symbol)
        elif memory_object in self.queues:
            self.queues[memory_object].enqueue(write_symbol)

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