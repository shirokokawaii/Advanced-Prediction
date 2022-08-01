from utils.get_data import read_data, convert2csv, set_XY, set_data

data = read_data(1, 10, 2, "1d")
print(data)


print(set_XY(data))


print(convert2csv(data))

print(set_data())
