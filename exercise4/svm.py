import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.optimize import minimize
from sklearn.metrics import accuracy_score
from operator import add

#return data in format pandas.dataframe
def read_data(file_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file_name)
    df = pd.read_csv(filename, header=None)
    return df

#add column with values of vector b from equation: f(x) = sign(w.dot(x) + b) <-- SVM model
def clean_data(df):
    df.columns = ["sepal length in cm", "sepal width in cm","petal length in cm","petal width in cm", "class"]
    df.insert(loc=len(df.columns), column = 'intercept', value = 1)
    df = df[["sepal length in cm", "sepal width in cm","petal length in cm","petal width in cm", "intercept", "class"]]
    return df

#normalize data to values in range [-0,1]
#map classes to values 1 or -1
#split dataset into X and Y sets
#return sets X and Y that contain sets for each pair
def normalize_data(pairs):
    setosa_versicolor_map = {"Iris-setosa":1, "Iris-versicolor":-1}
    versicolor_virginica_map = {"Iris-versicolor":1, "Iris-virginica":-1}
    setosa_virginica_map = {"Iris-setosa":1, "Iris-virginica":-1}

    maps = []
    maps.append(setosa_versicolor_map)
    maps.append(versicolor_virginica_map)
    maps.append(setosa_virginica_map)

    X = []
    Y = []
    for i in range(0, len(pairs)):
        pairs[i]["class"] = pairs[i]["class"].map(maps[i])
        #fit transform zwraca ndarray, czyli numpy
        pairs[i].iloc[:, 0:4] = (pairs[i].iloc[:, 0:4]-pairs[i].iloc[:, 0:4].min())/(pairs[i].iloc[:, 0:4].max()-pairs[i].iloc[:, 0:4].min())
        y = pairs[i].iloc[:,5]
        X.append(pairs[i].iloc[:, 0:5])
        Y.append(y)

    Y = [y.values.reshape((100,1)) for y in Y]
    return X, Y

#create dataset for each pair of classes
#return sets X and Y that contain sets for each pair
def make_pairs(df):
    mask1 = df['class'] == "Iris-setosa"
    mask2 = df['class'] == "Iris-versicolor"
    mask3 = df['class'] == "Iris-virginica"

    setosa_versicolor = df[mask1 | mask2].copy(deep=True)
    versicolor_virginica = df[mask2 | mask3].copy(deep=True)
    setosa_virginica = df[mask1 | mask3].copy(deep=True)
    
    pairs = []
    pairs.append(setosa_versicolor)
    pairs.append(versicolor_virginica)
    pairs.append(setosa_virginica)

    X, Y = normalize_data(pairs)
    return X, Y

#calculate value of the cost function
#return cost of the function
def cost_function(W, X, Y, lmbda):
    W = W.reshape((1,5))

    #W is of shape (1,5). Four values indicate four different parameters (petal length etc.), fifth value indicates bias
    #distances = 1 - Y * (np.dot(W, X.T).T)#X.shape - (80,5); Y.shape - (80,1); W.shape - (5,)
    distances = 1 - np.multiply(Y, np.dot(W, X.T).T)
    distances[distances < 0] = 0
    N = X.shape[0]
    hinge_loss = (np.sum(distances)/N)
    cost = lmbda / 2 * np.dot(W, W.T) + hinge_loss
    return cost

def split_train_test(X, Y, left_scope, right_scope):
    x_test = X.iloc[left_scope:right_scope,:]
    x_train = X.drop(X.index[left_scope:right_scope])
    y_test = Y[left_scope:right_scope]
    y_train= np.delete(Y, slice(left_scope,right_scope)).reshape((80,1))
    
    x_train = x_train.to_numpy()
    x_test = x_test.to_numpy()
    return x_train, x_test, y_train, y_test

#optimize weights of all pairs
#X - list of X sets for each pair
#Y - list of Y sets for each pair 
def optimize_lambda(X, Y):
    lambdas = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 100, 1000]
    qualities = []
    for i in range(0, len(X)):
        pair_qualities = []
        #print(f"pair nr {i}")
        for j in range(0,5):
            left_scope = j*20
            right_scope = (j+1)*20
            x_train, x_test, y_train, y_test = split_train_test(X[i], Y[i], left_scope, right_scope)
            cv_qualities = []
            for l in range(0, len(lambdas)):
                weights, iterations = optimize(x_train, y_train, lambdas[l]) 
                accuracy = test_model(weights, x_test, y_test)
                quality = [l, accuracy] #index of lambda in 'lambdas' list, accuracy
                cv_qualities.append(quality)

            best_of_cv_qualities = sorted(cv_qualities, key = lambda x: x[1], reverse = True)[0]
            pair_qualities.append(best_of_cv_qualities)
        best_of_pair_qualities = sorted(pair_qualities, key = lambda x: x[1], reverse = True)[0]
        qualities.append(best_of_pair_qualities)
    best_quality = sorted(qualities, key = lambda x: x[1], reverse = True)[0]
    print(f"best C: {lambdas[best_quality[0]]}")
    return best_quality

def optimize_weights(X, Y, lmbda):
    W = [0,0,0,0,0]
    for i in range(0, len(X)):
        for j in range(0,5):
            left_scope = j*20
            right_scope = (j+1)*20
            x_train, x_test, y_train, y_test = split_train_test(X[i], Y[i], left_scope, right_scope)
            weights, iterations = optimize(x_train, y_train, lmbda) #weights - (5,) zwykla lista
            accuracy = test_model(weights, x_test, y_test)
            W = list(map(add, W, weights))
    W = [w/15 for w in W]
    return W
                
                
def check_accuracy(X, Y, weights):
    weights = np.array(weights)
    for i in range(0, len(X)):
        x_train, x_test, y_train, y_test = train_test_split(X[i], Y[i], test_size = 0.2, random_state=300501)
        accuracy = test_model(weights, x_test, y_test)
        print(f"pair {i+1} - accuracy: {accuracy}")

        
        
#optimize weight of a given pair
#X - X set for a given pair
#Y - Y set for a given pair
#X, Y - pandas.DataFrame
def optimize(x_train, y_train, lmbda):
    weights = np.zeros((1,5))
    res = minimize(cost_function, weights, method='Nelder-Mead', args=(x_train,y_train,0.01))
    return res.x, res.nfev
    
#test model accuracy
def test_model(W, x_test, y_test):
    W = W.reshape((1,5))
    y_pred = np.sign(np.dot(W, x_test.T).T)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

print("starting program...")
df = read_data("iris.data")
df = clean_data(df)
X, Y = make_pairs(df)
lmbda = optimize_lambda(X, Y)
weights = optimize_weights(X, Y, lmbda)
check_accuracy(X, Y, weights)