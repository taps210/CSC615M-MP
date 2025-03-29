class Stack:
    def __init__(self, name):
        self.name = name
        self.items = []

    def get_head(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self, name):
        self.name = name
        self.items = []

    def get_head(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return None
        
    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

class Tape:
    def __init__(self, name):
        self.name = name
        self.tape = {0: '#', 1: '#'}
        self.head_position = 0

    def read(self):
        return self.tape.get(self.head_position, '_')

    def read_right(self):
        right_position = self.head_position + 1
        return self.tape.get(right_position, '_')
    
    def read_left(self):
        left_position = self.head_position - 1
        return self.tape.get(left_position, '_')

    def write(self, symbol):
        self.tape[self.head_position] = symbol
        max_index = max(self.tape.keys())
        if self.head_position == max_index:
            self.tape[max_index + 1] = '#'

    def move_left(self):
        self.head_position -= 1

    def move_right(self):
        self.head_position += 1

    def write_input(self, input_string):
        for i, char in enumerate(input_string):
            self.tape[i+1] = char
        self.tape[max(self.tape.keys()) + 1] = '#'

class Tape2D(Tape):
    def __init__(self, name):
        super().__init__(name)
        self.current_row = 0

    def move_up(self):
        self.current_row -= 1

    def move_down(self):
        self.current_row += 1
