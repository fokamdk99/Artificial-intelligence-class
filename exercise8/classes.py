#Literal - klasa opisujaca pojedynczy literal, sklada sie z dwoch parametrow: nazwa oraz negated(czy literal jest zanegowany)
class Literal:
    def __init__(self, variable, negated):
        self.variable = variable
        self.negated = negated
    
    def __neg__(self):
        return Literal(self.variable, not self.negated)

    def __eq__(self, other):
        return (self.variable, self.negated) == (other.variable, other.negated)

    def __hash__(self):
        return hash((self.variable, self.negated))

    def __str__(self):
        if self.negated:
            return f"-{self.variable}"
        else:
            return f"{self.variable}"

    def resolve(self, other):
        if (self.variable == other.variable and self.negated != other.negated):
            return True
        else:
            return False

#Clause - klasa zawierajaca literaly nalezace do jednej klauzuli
class Clause:
    #id - identyfikator danej klauzuli
    id = 0

    #literals - tablica zawierajaca obiekty typu Literal
    def __init__(self, literals):
        self.literals = literals
        self.id = Clause.id
        Clause.id += 1

    def __str__(self):
        string = ""
        for i in range(0, len(self.literals)):
            string += str(self.literals[i])
            string += ", "

        string = string[:-2]
        return string

    def __add__(self, other):
        new_literals = self.literals + other.literals
        return Clause(new_literals)

    def __eq__(self, other):
        literals = self.literals + other.literals
        new_literals = list(set(literals))
        if (len(new_literals) == len(self.literals)):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.id)

#Dataset - klasa zawierajaca zbior klauzul dotyczacych danego problemu
class Dataset:
    #clauses - lista obiektow typu Clause
    def __init__(self, clauses):
        self.clauses = clauses
        self.previous_clauses_number = len(self.clauses)

    def __str__(self):
        string = ""
        for i in range(0, len(self.clauses)):
            tmp = str(self.clauses[i])
            string += tmp
            string += "\n"
        string += "\n"

        return string
