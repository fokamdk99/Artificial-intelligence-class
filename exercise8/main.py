import test_cases
from prover1 import prove

def main():
    dataset = test_cases.test5()
    print("wczytane klauzule")
    print(dataset)
    prove(dataset)

main()