from memory_models import Stack, Queue, Tape, Tape2D
import re
import copy

class AbstractMachine:
    def __init__(self, definition):
        self.definition = definition
        self.stacks = {}
        self.queues = {}
        self.tapes = {}
        self.states = {}
        self.current_state = None
        self.machine_number = 1
        self.log = []

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
            self.tapes["input"] = Tape("input")
            self.tapes["input"].write_input(input_string)

        self.current_state = list(self.states.keys())[0]

        self.execute_loop()
        return
    
    def execute_loop(self):
        #input_tape_name = list(self.tapes.keys())[0]
        #print(self.tapes["Input"].read(), self.current_state)
        #print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items)
        #print(self.tapes["Input"].read(), self.current_state, self.stacks["S1"].items, self.stacks["S2"].items)
        #print(''.join(self.tapes[input_tape_name].tape[key] for key in sorted(self.tapes[input_tape_name].tape)), self.current_state)
        
        while True:
            self.log_step()

            if self.current_state in ['accept', 'reject', 'halt']:
                break
            
            command = self.states[self.current_state]
            logic = re.match(r'^[A-Z\s]+', command).group(0).strip()
            possible_transitions = self.get_transitions(command, logic)

            if self.current_state in ['accept', 'reject', 'halt']:
                break
            if len(possible_transitions) == 1:
                self.apply_transition(possible_transitions[0], logic, command)
            else:
                for index, transition in enumerate(possible_transitions):
                    if index == len(possible_transitions) - 1:
                        self.machine_number += index
                        self.apply_transition(transition, logic, command)
                    else:
                        machine_copy = copy.deepcopy(self)
                        machine_copy.apply_transition(transition, logic, command)
                        machine_copy.machine_number += index
                        machine_copy.execute_loop()
        print(f"Machine: {self.machine_number}")
        self.print_log()
        print(self.current_state)
        print('\n\n')

    def log_step(self):
        memory_contents = {}
        for tape_name, tape in self.tapes.items():
            memory_contents[tape_name] = ''.join(
                [tape.tape[i] for i in sorted(tape.tape.keys())]
            )
        for stack_name, stack in self.stacks.items():
            memory_contents[stack_name] = list(stack.items)
        for queue_name, queue in self.queues.items():
            memory_contents[queue_name] = list(queue.items)

        self.log.append({
            "state": self.current_state,
            "memory": memory_contents,
        })
    
    def get_transitions(self, command, logic):
        input_tape_name = list(self.tapes.keys())[0]
        tape_name = command.split('(')[1].split(')')[0].strip()
        transitions = re.findall(r'\((.*?)\)', command)
        if logic == 'PRINT' or logic == 'SCAN' or logic == 'SCAN RIGHT' or logic == 'SCAN LEFT':
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
        elif logic == 'SCAN' or logic == 'SCAN RIGHT' or logic == 'SCAN LEFT':
            if logic == 'SCAN LEFT':
                current_symbol = self.tapes[input_tape_name].read_left()
            else: #'SCAN', 'SCAN RIGHT'
                current_symbol = self.tapes[input_tape_name].read_right()
            for transition in transitions:
                symbol = transition[0].strip()
                if symbol == current_symbol:
                    possible_transitions.append(transition)
        else: #'RIGHT', 'LEFT', 'UP', 'DOWN'
            if logic == 'LEFT':
                current_symbol = self.tapes[tape_name].read_left()
            elif logic == 'RIGHT':
                current_symbol = self.tapes[tape_name].read_right()
            for transition in transitions:
                symbol, replacement = transition[0].split('/')
                if symbol == current_symbol:
                    possible_transitions.append(transition)

        if len(possible_transitions) == 0:
            self.current_state = 'reject'

        return possible_transitions

    def apply_transition(self, transition, logic, command):
        # Apply the given transition to the machine state
        if logic == 'SCAN LEFT':
            self.scan_left(transition)
        elif logic == 'SCAN' or logic == 'SCAN RIGHT':
            self.scan_right(transition)
        elif logic == 'PRINT':
            self.print(transition)
        elif logic == 'WRITE':
            self.write(transition, command)
        elif logic == 'READ':
            self.read(transition, command)
        elif logic == 'RIGHT':
            self.right(transition, command)
        elif logic == 'LEFT':
            self.left(transition, command)
        elif logic == 'UP':
            self.up(transition, command)
        elif logic == 'DOWN':
            self.down(transition, command)
        # Add similar cases for other commands

    def print_log(self):
        for step in self.log:
            print(f"State: {step['state']}")
            if step['memory']:
                print("Memory Contents:")
                for name, contents in step['memory'].items():
                    print(f"  {name}: {contents}")
            print("-" * 40)
            
    def scan_right(self, transition):
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_right()
        self.current_state = transition[1]
        return

    def scan_left(self, transition):
        input_tape_name = list(self.tapes.keys())[0]
        self.tapes[input_tape_name].move_left()
        self.current_state = transition[1]
        return

    def print(self, transition):
        if "output" not in self.tapes:
            self.tapes["output"] = Tape("output")
        self.tapes["output"].move_right()
        self.tapes["output"].write(transition[0])
        self.current_state = transition[1]
        return

    def read(self, transition, command):
        memory_object = command.split('(')[1].split(')')[0].strip()
        next_state = transition[1].strip()

        if memory_object in self.stacks:
            self.stacks[memory_object].pop()
        elif memory_object in self.queues:
            self.queues[memory_object].dequeue()

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

    def right(self, transition, command):
        # Extract the tape name from the command
        tape_name = command.split('(')[1].split(')')[0].strip()

        # Extract the symbol/replacement and state transitions
        symbol, replacement = transition[0].split('/')
        next_state = transition[1].strip()
        self.tapes[tape_name].move_right()
        self.tapes[tape_name].write(replacement.strip())
        self.current_state = next_state
        return

    def left(self, transition, command):
        # Extract the tape name from the command
        tape_name = command.split('(')[1].split(')')[0].strip()

        # Extract the symbol/replacement and state transitions
        symbol, replacement = transition[0].split('/')
        next_state = transition[1].strip()
        self.tapes[tape_name].move_left()
        self.tapes[tape_name].write(replacement.strip())
        self.current_state = next_state
        return

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