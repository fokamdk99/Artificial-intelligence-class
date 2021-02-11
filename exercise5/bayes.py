import os
import pandas as pd
import numpy as np
from itertools import combinations

#read data from file
#return data in format pandas.dataframe
def read_data(file_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file_name)
    df = pd.read_csv(filename, header=None)
    return df

#add column names
def clean_data(df):
    columns = ["class", "alcohol", "malic acid", "ash", "alcalinity of ash", "magnesium", "total phenols", "flavanoids", "nonflavanoid phenols", "proanthocyanins", "color intensity", "hue", "od280/od315 of diluted wines", "proline"]
    df.columns = columns

    return df

#return list containing 3 elements. Each element stores rows that corespond to a given group
def separate_classes(df):
    classes = []
    class1 = df[df['class'] == 1]
    class2 = df[df['class'] == 2]
    class3 = df[df['class'] == 3]

    classes.append(class1)
    classes.append(class2)
    classes.append(class3)
    return classes

#return list containing 3 elements
#each element  is a list of 5 subsets of a given class
def get_groups(classes):
    classes_chunks = []
    for i in range(0, len(classes)):
        class_chunks = []
        length = len(classes[i])
        lin = np.linspace(0, length+1, 6).astype('int32') #create 5 groups
        for j in range(0,len(lin)-1):
            tmp = classes[i].iloc[lin[j]:lin[j+1]]
            class_chunks.append(tmp)
        classes_chunks.append(class_chunks)
    return classes_chunks

#return train and test sets
#index - value between 0 and 4 (inclusive) 
#column1 and column2 - parameters that we want to investigate
def get_train_test_data(classes_chunks, index, column1, column2):
    x_trains = []
    x_tests = []
    ind0 = (index) % 5
    ind1 = (index+1) % 5
    ind2 = (index+2) % 5
    ind3 = (index+3) % 5
    ind4 = (index+4) % 5 #test chunk
    for i in range(len(classes_chunks)):
        x_train = pd.concat([classes_chunks[i][ind0][[column1, column2]], classes_chunks[i][ind1][[column1, column2]], classes_chunks[i][ind2][[column1, column2]], classes_chunks[i][ind3][[column1, column2]]], axis=0)
        x_test = classes_chunks[i][ind4][[column1, column2, "class"]]
        x_trains.append(x_train)
        x_tests.append(x_test)
    
    return x_trains, x_tests

    
#returns a list of dictionaries
#dictionary has parameters: data(values of alcohol parameters), class(class number), mean(mean values for each column in class), std_deviation(std deviation for each column in class)
def get_mean_and_deviation2(x_trains, max_len):
    values = []
    for i in range(0, len(x_trains)):
        mean = x_trains[i].mean(axis=0)
        std_deviation = x_trains[i].std(axis=0)

        percentage = len(x_trains[i])
        
        value_dict = {}
        value_dict["data"] = x_trains[i]
        value_dict["class"] = i+1
        value_dict["mean"] = mean
        value_dict["std_deviation"] = std_deviation
        value_dict["percentage"] = percentage/max_len

        values.append(value_dict)

    return values

#x - dataframe of shape (k, 2); mean - series, std_deviation - series, percentage - float
#returns probability that a given row belongs to a particular class
def get_probability3(x, mean, std_deviation, percentage):
    x = x.iloc[:,:-1]
    tmp1 = (x.sub(mean))**2
    tmp2 = (2*std_deviation**2)
    tmp3 = tmp1.divide(tmp2)
    numerator = np.exp(-tmp3)

    denominator = np.sqrt(2*np.pi)*std_deviation

    components = numerator.divide(denominator)

    probability = components.product(axis=1)
    probability *= percentage

    return probability

#predict probabilities for each class and assign row to a class with highest probability
def predict(values, x_test):
    probabilities = []
    for i in range(0, len(values)):
        
        p = get_probability3(x_test, values[i]["mean"], values[i]["std_deviation"], values[i]["percentage"])
        probabilities.append(p)

    probs = pd.concat([probabilities[0], probabilities[1], probabilities[2]],axis=1)
    probs.columns = [1,2,3]
    maxy = probs.idxmax(axis=1)
    errors = maxy.compare(x_test.iloc[:,-1], keep_shape = False)
    accuracy = (maxy.shape[0] - errors.shape[0])/maxy.shape[0]*100

    return accuracy

#select a pair of parameters that ensure the best probability of assigning a particular row to the corresponding class
def get_best_parameters(accuracies):
    output = [[(accuracies[i][j][0][0] + accuracies[i][j][1][0] + accuracies[i][j][2][0])/3, accuracies[i][j][0][3], accuracies[i][j][0][4]] for i in range(0,len(accuracies)) for j in range(0,len(accuracies[i]))]
    best = max(output, key = lambda x: x[0])
    print("accuracy: ", best[0])
    print("attributes:", best[1], ", ", best[2])
    return best

#calculate results for each combination of train/test datasets and for each pair of parameters
def cross_validation(classes, df, classes_chunks):
    columns2 = ["alcohol", "malic acid", "ash", "alcalinity of ash", "magnesium", "total phenols", "flavanoids", "nonflavanoid phenols", "proanthocyanins", "color intensity", "hue", "od280/od315 of diluted wines", "proline"]
    all_accuracies = []
    for i in range(0, 5):
        pairs_accuracies = []
        pairs = combinations(columns2, 2)
        for m in pairs:
            chunks_accuracy = []
            x_trains, x_tests = get_train_test_data(classes_chunks, i, m[0], m[1])
            values = get_mean_and_deviation2(x_trains, df.shape[0])
            for j in range(0, len(x_tests)):
                accuracy = predict(values, x_tests[j])
                scores = [accuracy, i, j, m[0], m[1]]
                chunks_accuracy.append(scores)
            pairs_accuracies.append(chunks_accuracy)
        all_accuracies.append(pairs_accuracies)
    best = get_best_parameters(all_accuracies)
    return best

def main():
    df = read_data("wine.data")
    df = clean_data(df)
    classes = separate_classes(df)
    classes_chunks = get_groups(classes)
    cross_validation(classes, df, classes_chunks)

main()
