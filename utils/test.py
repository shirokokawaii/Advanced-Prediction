from utils.get_data import read_data, convert2csv

data = read_data(1, 10, 2, "1d")
print(convert2csv(data))