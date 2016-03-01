import random
import time
import frozenintervaltree

def timing():
    intervals = []
    values = []
    n_intervals = 100000
    print('# Intervals: {0}'.format(n_intervals))
    for i in range(n_intervals):
        interval_start = random.randint(-100000, 10000000)
        interval_length = random.randint(1, 1000)
        intervals.append((interval_start, interval_start + interval_length))
        values.append(i)
    t0 = time.time()
    t = frozenintervaltree.FrozenIntervalTree(list(intervals), list(values))
    t1 = time.time()-t0
    print('Interval Tree Construction Time: {0}'.format(t1))
    t0 = time.time()
    for i,v in zip(intervals,values):
        midpoint = float((i[0]+i[1])/2)
        value = t.search_point(midpoint)
        if v not in value[1]:
            print i
            print midpoint
            print value
            print v
    print('Interval Tree Point Query Time: {0}'.format(time.time()-t0))
    t0 = time.time()
    for i,v in zip(intervals,values):
        value = t.search_range(i)
        if v not in value[1]:
            print i
            print midpoint
            print value
            print v
    print('Interval Tree Range Query Time: {0}'.format(time.time()-t0))

