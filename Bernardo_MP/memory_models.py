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

    def read_right(self):
        right_position = self.head_position + 1
        return self.tape.get(right_position, '_')
    
    def read_left(self):
        left_position = self.head_position - 1
        return self.tape.get(left_position, '_')

    def move_left(self):
        self.head_position -= 1

    def move_right(self):
        self.head_position += 1

    def write(self, symbol):
        self.tape[self.head_position] = symbol
        max_index = max(self.tape.keys())
        if self.head_position == max_index:
            self.tape[max_index + 1] = '#'

    def write_input(self, input_string):
        for i, char in enumerate(input_string):
            self.tape[i+1] = char
        max_index = max(self.tape.keys())
        self.tape[max_index + 1] = '#'

class Tape2D:
    def __init__(self, name):
        self.name = name
        self.tape = {0: {0: '#', 1: '#'}, 
                     1: {0: '#', 1: '#'}}
        self.head_row = 0
        self.head_col = 0

    def read_right(self):
        right_position = self.head_col + 1
        return self.tape.get(self.head_row, {}).get(right_position, '_')
    
    def read_left(self):
        left_position = self.head_col - 1
        return self.tape.get(self.head_row, {}).get(left_position, '_')
    
    def read_up(self):
        up_position = self.head_row - 1
        return self.tape.get(up_position, {}).get(self.head_col, '_')
    
    def read_down(self):
        down_position = self.head_row + 1
        return self.tape.get(down_position, {}).get(self.head_col, '_')
    
    def move_right(self):
        self.head_col += 1

    def move_left(self):
        self.head_col -= 1

    def move_up(self):
        self.head_row -= 1

    def move_down(self):
        self.head_row += 1

    def write(self, symbol):
        self.tape[self.head_row][self.head_col] = symbol
        max_row = max(self.tape.keys())
        max_col = max(max(row.keys()) for row in self.tape.values())
        if self.head_row == max_row:
            self.tape[max_row + 1] = {col: '#' for col in range(max_col + 1)}
        if self.head_col == max_col:
            self.tape[self.head_row][max_col + 1] = '#'

    def write_input(self, input_string):
        for i, char in enumerate(input_string):
            self.tape[0][i+1] = char
        max_col = max(max(row.keys()) for row in self.tape.values())
        self.tape[max_col + 1] = '#'
