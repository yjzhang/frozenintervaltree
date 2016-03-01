from intervaltree import Interval, IntervalTree
import tqdm
import random
import time

if __name__=='__main__':
    t = IntervalTree()
    intervals = []
    values = []
    t0 = time.time()
    n_intervals=1000000
    print('# Intervals: {0}'.format(n_intervals))
    for i in tqdm.tqdm(range(n_intervals)):
        interval_start = random.randint(-100000,10000000)
        interval_length = random.randint(1,1000)
        t[interval_start:interval_start+interval_length] = i
        intervals.append((interval_start, interval_start+interval_length))
        values.append(i)
    t1 = time.time()
    print('Interval Tree Construction Time: {0}'.format(t1-t0))
    for i,v in tqdm.tqdm(zip(intervals, values)):
        midpoint = float((i[0]+i[1])/2)
        value = t[midpoint]
    print('Interval Tree Query Time: {0}'.format(time.time()-t1))
    t1 = time.time()
    for i,v in tqdm.tqdm(zip(intervals, values)):
        value = t[i[0]:i[1]]
    print('Interval Tree Range Time: {0}'.format(time.time()-t1))
