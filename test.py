import frozenintervaltree
import tqdm
import random
import time

def timing_test():
    intervals = []
    values = []
    n_intervals = 1000000
    print('# Intervals: {0}'.format(n_intervals))
    for i in tqdm.tqdm(range(n_intervals)):
        interval_start = random.randint(-100000, 10000000)
        interval_length = random.randint(1, 1000)
        intervals.append((interval_start, interval_start + interval_length))
        values.append(i)
    t0 = time.time()
    t = frozenintervaltree.FrozenIntervalTree(list(intervals), list(values))
    t1 = time.time()-t0
    print('Interval Tree Construction Time: {0}'.format(t1))
    t0 = time.time()
    for i,v in tqdm.tqdm(zip(intervals,values)):
        midpoint = float((i[0]+i[1])/2)
        value = t.search_point(midpoint)
        if v not in value[1]:
            print i
            print midpoint
            print value
            print v
    print('Interval Tree Point Query Time: {0}'.format(time.time()-t0))
    t0 = time.time()
    for i,v in tqdm.tqdm(zip(intervals,values)):
        value = t.search_range(i)
        if v not in value[1]:
            print i
            print midpoint
            print value
            print v
    print('Interval Tree Range Query Time: {0}'.format(time.time()-t0))



if __name__=='__main__':
    intervals = [(0,1),(1,2),(2,3),(3,4)]
    values = [1,2,3,4]
    t = frozenintervaltree.FrozenIntervalTree(intervals, values)
    assert(t.search_point(0.5)[1]==[1])
    assert(t.search_point(3.9)[1]==[4])
    assert(t.search_point(5)[1]==[])
    assert(t.search_point(1.5)[1]==[2])
    assert(sorted(t.search_range((0.5,1.5))[1])==[1,2])
    print t.search_range((0.5,3.5))
    assert(sorted(t.search_range((0.5,3.5))[1])==[1,2,3,4])
    i2 = [(0,10),(1,2),(5,8),(9,100),(3,10),(-1,11)]
    v2 = [1,2,3,4,5,6]
    t2 = frozenintervaltree.FrozenIntervalTree(i2,v2)
    r0 = t2.search_point(0)[1]
    assert(6 in r0 and 1 in r0)
    r1 = t2.search_point(99)[1]
    assert(r1==[4])
    r2 = t2.search_point(6)[1]
    assert(1 in r2 and 3 in r2 and 5 in r2 and 6 in r2)
    r3 = t2.search_range((2.1,3.5))[1]
    print r3
    assert(1 in r3 and 5 in r3 and 6 in r3)
    timing_test()
