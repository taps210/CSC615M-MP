from abstract_machine import AbstractMachine
# Example usage
machine_definition = """.DATA
STACK S1
STACK S2
.LOGIC
A] WRITE(S1) (#,B), (#,O)
B] WRITE(S2) (#,C)
C] WRITE(S1) (X,D)
D] READ(S1) (X,E), (#,G)
E] WRITE(S2) (X,F)
F] SCAN (1,D)
G] SCAN (1,H), (#,accept)
H] WRITE(S1) (#,I)
I] READ(S2) (X,J), (#,L)
J] WRITE(S1) (X,I)
L] WRITE(S2) (#,M)
M] WRITE(S2) (X,N)
N] WRITE(S2) (X,F)
O] SCAN (#,P)
P] READ(S1) (#,accept)"""
input_string = "1"

def main():
    machine = AbstractMachine(machine_definition)
    machine.parse_definition()
    machine.execute(input_string)

if __name__ == "__main__":
    main()
