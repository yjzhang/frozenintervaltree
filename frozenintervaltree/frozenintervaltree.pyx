"""
Frozen Interval Trees

"""

from operator import itemgetter

cdef class IntervalValue:

    cdef double left
    cdef double right
    cdef object value

    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

cdef interval_overlap(tuple interval, tuple i):
    if interval[1]<=i[1] and interval[1]>=i[0]:
        return True
    if interval[0]>=i[0] and interval[0]<=i[1]:
        return True
    if i[0]>=interval[0] and i[1]<=interval[1]:
        return True
    return False

cdef class Node:
    """
    Interval Tree node
    """

    cdef list left_intervals, right_intervals
    cdef double median_value
    cdef object left, right, value

    def __init__(self, list intervals_left_sorted, list intervals_right_sorted,
            median_value = 0, left = None, right = None, value = None):
        self.left_intervals = intervals_left_sorted
        self.right_intervals = intervals_right_sorted
        self.median_value = median_value
        self.left = left
        self.right = right
        self.value = value

    def point_in_node(self, point):
        """
        Returns the intervals that the point is contained in if it is contained
        in this node. Returns an empty list if no intervals are contained.
        """
        cdef list intervals
        intervals = []
        if point==self.median_value:
            return self.left_intervals
        elif point < self.median_value:
            for interval in self.left_intervals:
                if point<=interval[1] and point>=interval[0]:
                    intervals.append(interval)
                if point < interval[0]:
                    break
        else:
            for interval in self.right_intervals:
                if point<=interval[1] and point>=interval[0]:
                    intervals.append(interval)
                if point > interval[1]:
                    break
        return intervals

    def interval_in_node(self, interval):
        cdef list intervals = []
        if interval[1] < self.median_value:
            for i in self.left_intervals:
                if interval_overlap(i, interval):
                    intervals.append(i)
                if interval[1]<i[0]:
                    break
        else:
            for i in self.right_intervals:
                if interval_overlap(i, interval):
                    intervals.append(i)
                if interval[0]>i[1]:
                    break
        return intervals

    def search_recursive(self, point):
        cdef list intervals = self.point_in_node(point)
        if self.left is not None and point < self.median_value:
            intervals += self.left.search_recursive(point)
        elif self.right is not None and point > self.median_value:
            intervals += self.right.search_recursive(point)
        return intervals

    def search_range_recursive(self, interval):
        """
        Finds intervals overlapping the given interval.
        """
        cdef list intervals = self.interval_in_node(interval)
        if self.left is not None and interval[0] < self.median_value:
            intervals += self.left.search_range_recursive(interval)
        if self.right is not None and interval[1] > self.median_value:
            intervals += self.right.search_range_recursive(interval)
        return intervals

def median(list intervals):
    if len(intervals)==0:
        return 0
    intervals.sort(key=itemgetter(1))
    if len(intervals)%2:
        return (intervals[len(intervals)/2][1] + intervals[len(intervals)/2-1][0])/2
    else:
        return (intervals[len(intervals)/2][0] + intervals[len(intervals)/2][1])/2


def divide_intervals(list interval_values):
    """
    Returns an interval tree representing the given intervals.
    Does this using recursive partitioning by medians.
    """
    if len(interval_values)==0:
        return None
    m = median(interval_values)
    left = []
    right = []
    center = []
    for interval in interval_values:
        if interval[1] < m:
            left.append(interval)
        elif interval[0] > m:
            right.append(interval)
        else:
            center.append(interval)
    center_right_sorted = sorted(center,key=itemgetter(1), reverse=True)
    center_left_sorted = sorted(center,key=itemgetter(0))
    center_node = Node(center_left_sorted, center_right_sorted, m)
    left_node = None
    if len(left)>0:
        left_node = divide_intervals(left)
    right_node = None
    if len(right)>0:
        right_node = divide_intervals(right)
    center_node.left = left_node
    center_node.right = right_node
    return center_node

cdef class FrozenIntervalTree:
    """
    """

    cdef object root

    def __init__(self, intervals, values):
        """
        Interval tree that is constructed from a list of intervals and a list
        of their associated values. The tree is fixed at construction and
        shouldn't be modified.
        """
        # step 1: sort intervals by endpoints 
        iv = [(i[0], i[1], v) for i, v in zip(intervals, values)]
        self.root = divide_intervals(iv)

    def search_point(self, point):
        """
        Returns all intervals and their associated values overlapping with a
        given point.

        Input: point - number
        """
        intervals = self.root.search_recursive(point)
        return [(i[0], i[1]) for i in intervals], [i[2] for i in intervals]

    def search_range(self, interval):
        """
        Returns all intervals and their associated values overlapping a
        given range.

        Input: interval - tuple of two numbers, where the first number is
        less than the second number.
        """
        intervals = self.root.search_range_recursive(interval)
        return [(i[0], i[1]) for i in intervals], [i[2] for i in intervals]
