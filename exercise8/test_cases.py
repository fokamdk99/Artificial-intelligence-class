from classes import Literal, Clause, Dataset

def sentences():
    a = Literal("A", False)
    b = Literal("B", False)
    c = Literal("C", False)
    d = Literal("D", False)
    e = Literal("E", False)
    f = Literal("F", False)
    not_a = -a
    not_b = -b
    not_c = -c
    not_d = -d
    not_e = -e
    not_f = -f
    dt = dict()
    dt['a'] = a
    dt['b'] = b
    dt['c'] = c
    dt['d'] = d
    dt['e'] = e
    dt['f'] = f
    dt['not_a'] = not_a
    dt['not_b'] = not_b
    dt['not_c'] = not_c
    dt['not_d'] = not_d
    dt['not_e'] = not_e
    dt['not_f'] = not_f
    return dt

def create_clauses(literals):
    clauses = []
    for i in range(0, len(literals)):
        clause = Clause(literals[i])
        clauses.append(clause)

    return clauses

def test1():
    d = sentences()
    literals = []
    literals.append([d['not_a'], d['b']])
    clauses = create_clauses(literals)

    observable_fact = [d['a']]
    not_observable_fact = [d['not_b']]

    observable_clause = Clause(observable_fact)
    not_observable_clause = Clause(not_observable_fact)

    clauses.append(observable_clause)
    clauses.append(not_observable_clause)
    dataset = Dataset(clauses)
    return dataset

def test2():
    d = sentences()
    literals = []
    literals.append([d['not_a'], d['b']])
    clauses = create_clauses(literals)

    observable_fact = [d['not_a']]
    not_observable_fact = [d['not_b']]

    observable_clause = Clause(observable_fact)
    not_observable_clause = Clause(not_observable_fact)

    clauses.append(observable_clause)
    clauses.append(not_observable_clause)
    dataset = Dataset(clauses)
    return dataset

def test3():
    d = sentences()
    literals = []
    literals.append([d['not_a'], d['c']])
    literals.append([d['not_b'], d['c']])
    literals.append([d['a'], d['b']])
    clauses = create_clauses(literals)

    not_observable_fact = [d['not_c']]

    not_observable_clause = Clause(not_observable_fact)

    clauses.append(not_observable_clause)
    dataset = Dataset(clauses)
    return dataset





def test4():
    d = sentences()
    literals = []
    literals.append([d['not_a'], d['b'], d['c']])
    literals.append([d['not_b'], d['d']])
    literals.append([d['not_c'], d['not_d']])
    literals.append([d['c'], d['d']])
    literals.append([d['not_c'], d['e']])
    literals.append([d['not_d'], d['not_e']])
    clauses = create_clauses(literals)

    observable_fact = [d['e']]
    not_observable_fact = [d['b']]

    observable_clause = Clause(observable_fact)
    not_observable_clause = Clause(not_observable_fact)

    clauses.append(observable_clause)
    clauses.append(not_observable_clause)
    dataset = Dataset(clauses)
    return dataset

def test5():
    d = sentences()
    literals = []
    literals.append([d['a'], d['b'], d['c']])
    literals.append([d['not_a'], d['d']])
    literals.append([d['not_b'], d['d']])
    literals.append([d['not_c'], d['not_e'], d['f']])
    literals.append([d['d'], d['e'], d['f']])
    literals.append([d['a'], d['not_f']])
    literals.append([d['not_d'], d['not_e']])
    clauses = create_clauses(literals)

    observable_fact = [d['not_a'], d['b']]
    not_observable_fact = [d['not_c']]

    observable_clause = Clause(observable_fact)
    not_observable_clause = Clause(not_observable_fact)

    clauses.append(observable_clause)
    clauses.append(not_observable_clause)
    dataset = Dataset(clauses)
    return dataset