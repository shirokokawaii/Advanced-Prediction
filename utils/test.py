from utils.get_data import get_data
from utils.get_time import get_time_from_file, get_timepoint

start = '14 Jun, 2012'
end = '19 Jun, 2021'
get_data(start, end, '4h', True)
get_time_from_file('hist_data', '%Y-%m-%d %H:%M:%S')
get_timepoint('hist_data', 5)
