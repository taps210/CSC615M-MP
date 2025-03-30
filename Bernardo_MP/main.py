from abstract_machine import AbstractMachine
# Example usage
machine_definition = """.DATA
TAPE T1
TAPE T2
TAPE T3
.LOGIC
A] RIGHT(T1) (a/a,B), (b/b,C)
B] RIGHT(T2) (#/X,A)
C] RIGHT(T2) (#/#,D)
D] LEFT(T2) (X/#,E)
E] RIGHT(T3) (#/X,F)
F] RIGHT(T1) (b/b,E), (c/c,G)
G] RIGHT(T3) (#/#,H)
H] LEFT(T3) (X/#,I)
I] RIGHT(T3) (c/c,H), (#/#,J)
J] LEFT(T2) (#/#,K)
K] LEFT(T3) (#/#,accept)"""
input_string = "abbcc"

def main():
    machine = AbstractMachine(machine_definition)
    machine.parse_definition()
    machine.execute(input_string)

if __name__ == "__main__":
    main()
