from asyncio import sleep


class FiniteAutomata:
    def __init__(self, file):
        self.setOfStates = []
        self.alphabet = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []
        self.file = file
        self.initialize()
        self.commands = {
            "1": self.print_states,
            "2": self.print_alphabet,
            "3": self.print_transitions,
            "4": self.print_initial_state,
            "5": self.print_final_states,
            "6": self.verify_dfa
        }

    def initialize(self):
        lines = open(self.file).readlines()
        self.setOfStates = lines[0].strip('\n').split(",")
        self.alphabet = lines[1].strip('\n').split(",")
        self.initial_state = lines[2].strip('\n')
        self.final_states = lines[3].strip('\n').split(" ")
        for i in range(4, len(lines)):
            splitLine = lines[i].strip('\n').split("=")
            key = splitLine[0]
            value = splitLine[1]
            key = key.strip("(").strip(")").split(",")
            self.transitions[(key[0], key[1])] = value

    def run_menu(self):
        while True:
            FiniteAutomata.printMenu()
            option = input(">>")
            if option == '0':
                print("Bye!")
                break
            elif option in self.commands:
                self.commands[option]()
            else:
                print("Invalid command")

    @staticmethod
    def printMenu():
        print('0.Exit')
        print('1.Print set of states')
        print('2.Print alphabet')
        print('3.Print transitions')
        print('4.Print initial state')
        print('5.Print set of final states')
        print('6.Verify dfa')

    def print_states(self):
        print("SET OF STATES:", self.setOfStates)

    def print_alphabet(self):
        print("ALPHABET:", self.alphabet)

    def print_transitions(self):
        print("TRANSITIONS:", self.transitions)

    def print_initial_state(self):
        print("INITIAL STATE:", self.initial_state)

    def print_final_states(self):
        print("SET OF FINAL STATES", self.final_states)

    def verify_dfa(self):
        array = input("Enter dfa:").strip('\n').split()
        state = self.initial_state
        for element in array:
            if (state,element) in self.transitions:
                state = self.transitions[(state,element)]
            else:
                print(False)
                return

        if state in self.final_states:
            print(True)
            return True

        print(False)
        return False


