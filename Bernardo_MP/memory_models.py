class Stack:
    def __init__(self, name):
        self.name = name
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

class Queue:
    def __init__(self, name):
        self.name = name
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

class Tape:
    def __init__(self, name):
        self.name = name
        self.tape = {}
        self.head_position = 0

    def read(self):
        return self.tape.get(self.head_position, '_')

    def write(self, symbol):
        self.tape[self.head_position] = symbol

    def move_left(self):
        self.head_position -= 1

    def move_right(self):
        self.head_position += 1

    def write_input(self, input_string):
        for i, char in enumerate(input_string):
            self.tape[i] = char

class Tape2D(Tape):
    def __init__(self, name):
        super().__init__(name)
        self.current_row = 0

    def move_up(self):
        self.current_row -= 1

    def move_down(self):
        self.current_row += 1
