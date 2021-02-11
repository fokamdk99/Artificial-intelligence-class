#Autor: Stanislaw Skrzypek
import numpy as np
import time


def check_determinancy(hessian):
    matrix = hessian
    det = []
    for i in range(1, hessian.shape[0]+1):
        det.append(np.linalg.det(matrix))
        matrix = matrix[:-1,:-1]

    ujemne = [number for number in det if number < 0]
    if len(ujemne) == 0:
        return 1
    
    if len(det) % 2 == 1:
        nieparzyste = det[::2]
        dodatnie = [number for number in nieparzyste if number > 0]
        if len(dodatnie) == 0:
            return -1
    else:
        nieparzyste = det[1::2]
        dodatnie = [number for number in nieparzyste if number > 0]
        if len(dodatnie) == 0:
            return -1

    return 1


def calculate_hessian_matrix(index, point):
    ident = np.identity(point.shape[0],dtype=float)
    if index == 0:
        hessian = ident * (-2)
    else:
        hessian = (-2) * ident - 2.2 * ident * np.sin(point.T.dot(point)) - 2.2 * point.dot(point.T) * np.cos(point.T.dot(point))

    return hessian


def calculate_inversed_hessian_matrix(hessian):
    return np.linalg.inv(hessian)


def calculate_gradient(index, point):
    if index == 0:
        return (-2) * point
    else:
        return (-2) * point - 2.2 * point * np.sin(point.T.dot(point))


def calculate_step(hessian, inv_h, grad):
    znak = check_determinancy(hessian)
    step = znak * inv_h.dot(grad)
    return step


def generate_start_points(dimension, quantity):
    x = []   
    for i in range(1, quantity + 1):
        x.append(np.random.uniform(-1, 1, (dimension, 1)) * 10 * i)

    return x


def generate_fixed_start_point(dimension):
    x = []
    x.append(np.ones((dimension,1)))
    return x
    

def main():
    beta = 0.2

    dimension = input("podaj wymiar wektora: ")
    try:
        dimension = int(dimension)
    except ValueError:
        print('podaj liczbe naturalna')
        raise ValueError('niepoprawna wartosc')

    quantity = input("podaj ilosc punktow startowych: ")
    try:
        quantity = int(quantity)
    except ValueError:
        print('podaj liczbe naturalna')
        raise ValueError('niepoprawna wartosc')

    function = input("podaj funkcje badana: 0 lub 1 ")
    try:
        function = int(function)
    except ValueError:
        print('wpisz 0 lub 1')
        raise ValueError('niepoprawna wartosc')
    
    #x = generate_start_points(dimension, quantity)
    x = generate_fixed_start_point(dimension)

    start = time.time()
    for ind, value in enumerate (x):
        #print(f"\n\n\npunkt startowy nr {ind}: {value}")
        for i in range (1,100):  
            tmp = x[ind]
            hessian = calculate_hessian_matrix(function, x[ind])
            inv_h = calculate_inversed_hessian_matrix(hessian)
            grad = calculate_gradient(ind, x[ind])  
            d = calculate_step(hessian, inv_h, grad)
            x[ind] = x[ind] + beta * d
            tmp = tmp - x[ind]
            if max(abs(tmp)) < 0.00001:
                #print(f"znaleziony punkt spelnia zalozenie")
                break
        print(f"wynik:\n{x[ind]}")
    end = time.time()
    print(f"czas: {end - start}")


main()