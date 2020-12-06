import sys
import csv
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from itertools import combinations
import random
from math import comb
# C:/Users/Alan/AppData/Local/Programs/Python/Python38/python.exe c:/Users/Alan/Documents/Code/approximate_index.py 3 .DJI historical_prices.csv > approximation.csv

# Read script arguments
args = sys.argv
num_stocks = int(sys.argv[1])
index = sys.argv[2]
input_csv = sys.argv[3]

# Read historical prices file
# Assign ticker symbol to price history list in prices{} dictionary
prices = {}
with open(input_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        name = row[0]
        price = float(row[2])
        if name in prices:
            temp = prices[name]
            temp.append(price)
            prices[name] = temp
        else:
            prices[name] = [price]

index_history = prices[index]
y = np.array(index_history)
del prices[index]

symbol_list = list(prices.keys())

# key = rms, value = {stock:weight, stock:weight, ...}
results = {}


def regression(combinations):  # Multiple regression for each combination
    for combination in combinations:
        x = []
        for symbol in combination:
            x.append(prices[symbol])
        # Converts list of columns to list of rows
        x = list(map(list, zip(*x)))

        X = np.array(x)

        # Want to match index price, fit_intercept = False
        # Want to match index behavior, fit_intercept = True
        reg = linear_model.LinearRegression(fit_intercept=False).fit(X, y)

        # Calculate rms, we will use this as our performance indicator
        y_predicted = reg.predict(X)
        rms = mean_squared_error(index_history, y_predicted, squared=False)

        # Store analysis in results dictionary
        coefficients = list(reg.coef_)
        results[rms] = {combination[i]: coefficients[i]
                        for i in range(len(combination))}


# Because we only need a "good enough solution", sample 1000 random combinations.
# If the total number of combinations is less than 1000, test every combination.
if comb(len(prices), num_stocks) < 1000:
    # Generates list of all combinations of n elements of symbol list
    # Generating this list takes too much memory as number of combinations increase
    combinations = list(combinations(symbol_list, num_stocks))
    regression(combinations)
else:
    # select 1000 combinations randomly
    sample = []
    for i in range(1000):
        sample.append(random.sample(symbol_list, num_stocks))
    regression(sample)

# Write output in csv
print("Symbol, Weight")
# Find the weights with the smallest rms
scores = sorted(results.keys())
best_score = scores[0]
coeff_dict = results[best_score]
for stock in coeff_dict.keys():
    print(stock + ", " + str(round(coeff_dict[stock], 3)))
