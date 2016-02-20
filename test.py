import intervaltree
import tqdm
import random
import time

def timing_test():
    intervals = []
    values = []
    for i in tqdm.tqdm(range(100000)):
        interval_start = random.randint(-100000, 10000000)
        interval_length = random.randint(1, 1000)
        intervals.append((interval_start, interval_start + interval_length))
        values.append(i)
    t0 = time.time()
    t = intervaltree.FrozenIntervalTree(list(intervals), list(values))
    t1 = time.time()-t0
    print('Interval Tree Construction Time: {0}'.format(t1))
    t0 = time.time()
    for i,v in tqdm.tqdm(zip(intervals,values)):
        midpoint = float((i[0]+i[1])/2)
        value = t.search_value(midpoint)
        if v not in value[1]:
            print i
            print midpoint
            print value
            print v
    print('Interval Tree Query Time: {0}'.format(time.time()-t0))



if __name__=='__main__':
    intervals = [(0,1),(1,2),(2,3),(3,4)]
    values = [1,2,3,4]
    t = intervaltree.FrozenIntervalTree(intervals, values)
    assert(t.search_value(0.5)[1]==[1])
    assert(t.search_value(3.9)[1]==[4])
    assert(t.search_value(5)[1]==[])
    assert(t.search_value(1.5)[1]==[2])
    i2 = [(0,10),(1,2),(5,8),(9,100),(3,10),(-1,11)]
    v2 = [1,2,3,4,5,6]
    t2 = intervaltree.FrozenIntervalTree(i2,v2)
    r0 = t2.search_value(0)[1]
    assert(6 in r0 and 1 in r0)
    r1 = t2.search_value(99)[1]
    assert(r1==[4])
    r2 =t2.search_value(6)[1]
    assert(1 in r2 and 3 in r2 and 5 in r2 and 6 in r2)
    timing_test()
