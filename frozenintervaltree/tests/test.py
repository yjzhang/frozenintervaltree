import unittest

import frozenintervaltree
import random

class BasicTest(unittest.TestCase):

    def test_search_point_nonoverlap(self):
        intervals = [(0,1),(1,2),(2,3),(3,4)]
        values = [1,2,3,4]
        t = frozenintervaltree.FrozenIntervalTree(intervals, values)
        self.assertTrue(t.search_point(0.5)[1]==[1])
        self.assertTrue(t.search_point(3.9)[1]==[4])
        self.assertTrue(t.search_point(5)[1]==[])
        self.assertTrue(t.search_point(1.5)[1]==[2])
        self.assertTrue(sorted(t.search_range((0.5,1.5))[1])==[1,2])
        self.assertTrue(sorted(t.search_range((0.5,3.5))[1])==[1,2,3,4])

    def test_search_point_overlap(self):
        i2 = [(0,10),(1,2),(5,8),(9,100),(3,10),(-1,11)]
        v2 = [1,2,3,4,5,6]
        t2 = frozenintervaltree.FrozenIntervalTree(i2,v2)
        r0 = t2.search_point(0)[1]
        self.assertTrue(6 in r0 and 1 in r0 and len(r0)==2)
        r1 = t2.search_point(99)[1]
        self.assertTrue(r1==[4])
        r2 = t2.search_point(6)[1]
        self.assertTrue(1 in r2 and 3 in r2 and 5 in r2 and 6 in r2 and len(r2)==4)

    def test_search_range(self):
        i2 = [(0,10),(1,2),(5,8),(9,100),(3,10),(-1,11)]
        v2 = [1,2,3,4,5,6]
        t2 = frozenintervaltree.FrozenIntervalTree(i2,v2)
        r3 = t2.search_range((2.1,3.5))[1]
        self.assertTrue(1 in r3 and 5 in r3 and 6 in r3 and len(r3)==3)
        r4 = t2.search_range((-100, 100))[1]
        self.assertTrue(len(r4)==6)
        self.assertTrue(sorted(r4)==v2)

class RandomTest(unittest.TestCase):

    def test_random_point_range_search(self):
        intervals = []
        values = []
        n_intervals = 10000
        for i in range(n_intervals):
            interval_start = random.randint(-100000, 10000000)
            interval_length = random.randint(1, 1000)
            intervals.append((interval_start, interval_start + interval_length))
            values.append(i)
        t = frozenintervaltree.FrozenIntervalTree(list(intervals), list(values))
        for i,v in zip(intervals,values):
            midpoint = float((i[0]+i[1])/2)
            value = t.search_point(midpoint)
            self.assertTrue(v in value[1])
            self.assertTrue(i in value[0])
        for i,v in zip(intervals,values):
            value = t.search_range(i)
            self.assertTrue(v in value[1])
            self.assertTrue(i in value[0])


if __name__=='__main__':
    unittest.main()
