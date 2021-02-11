from classes import Literal, Clause, Dataset
import test_cases
    
#sprawdza czy warunki zatrzymania zostaly spelnione
def check_constraints(dataset):
    terminate_program = False
    true_sentences = []

    clauses = dataset.clauses
    for i in range(0, len(clauses)):
        if len(clauses[i].literals) == 1:
            true_sentences.append(clauses[i].literals[0])
    
    truth_clause = Clause(true_sentences)
    truth_clause_without_duplicates = remove_duplicate_literals(truth_clause)
    truth_resolution = resolution(truth_clause_without_duplicates)
    if (len(truth_clause_without_duplicates.literals) != len(truth_resolution.literals)):
        terminate_program = True
        print("Nieobserwowalny fakt jest prawdziwy.")
        return terminate_program

    
    if len(clauses) == dataset.previous_clauses_number:
        terminate_program = True
        print("Nieobserwowalnego faktu nie da sie udowodnic.")
        return terminate_program
    else:
        dataset.previous_clauses_number = len(clauses)

    

    return terminate_program

#utworz nowa klauzule uzywajac rezolucji
def resolution(clause):
    resolved = []
    ls = clause.literals
    for i in range(0, len(ls)):
        for j in range(0, len(ls)):
            if(ls[i].resolve(ls[j])):
                resolved.append(i)
                resolved.append(j)

    literals = [element for i, element in enumerate(ls) if i not in resolved]
    new_clause = Clause(literals)

    return new_clause

#usun powtarzajace sie literaly z klauzulli
def remove_duplicate_literals(clause):
    literals = list(set(clause.literals))
    new_clause = Clause(literals)
    return new_clause

#usun powtarzajace sie klauzule ze zbioru klauzul
def remove_duplicate_clauses(dataset):
    new_clauses = list(set(dataset.clauses))
    new_dataset = Dataset(new_clauses)
    return new_dataset

#glowna funkcja sprawdzajaca, czy fakt obserwowalny daje sie udowodnic
def prove(dataset):
    terminate_program = False
    while (not terminate_program):
        clauses = dataset.clauses
        for i in range(0, len(clauses)-1):
            for j in range(i+1, len(clauses)):
                tmp_clause = clauses[i] + clauses[j]
                clause_without_duplicates = remove_duplicate_literals(tmp_clause)
                new_clause = resolution(clause_without_duplicates)
                
                #jesli znaleziono literaly o przeciwnych znakach, to dlugosci beda sie roznic
                if ((len(clause_without_duplicates.literals) != len(new_clause.literals)) and (len(new_clause.literals) != 0)):
                    clauses.append(new_clause)

        dataset = remove_duplicate_clauses(dataset)
        #print(dataset)
        terminate_program = check_constraints(dataset)

