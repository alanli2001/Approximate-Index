# Approximate Index

Market indices often contain a large number of securities. This script takes in input n number of securities to pick, Historical price data for each security in the index, as well as for the index itself. and which produces as output a list of n of the index's constituents, along with weightings, which give a good approximation of the index's behavior.


# Running
C:/Users/Alan/AppData/Local/Programs/Python/Python38/python.exe c:/Users/Alan/Documents/Code/approximate_index.py 3 .DJI historical_prices.csv > approximation.csv
