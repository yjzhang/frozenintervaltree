from operator import itemgetter

cdef class Node:
    """
    Interval Tree node
    """

    cdef list left_intervals, right_intervals
    cdef double median_value
    cdef object left, right

    def __init__(self, list intervals_left_sorted, list intervals_right_sorted,
            median_value = 0, left = None, right = None):
        self.left_intervals = intervals_left_sorted
        self.right_intervals = intervals_right_sorted
        self.median_value = median_value
        self.left = left
        self.right = right

    def point_in_node(self, point):
        """
        Returns the intervals that the point is contained in if it is contained
        in this node. Returns an empty list if no intervals are contained.
        """
        intervals = []
        if point==self.median_value:
            return self.left_intervals
        for interval in self.left_intervals:
            if point<=interval[1] and point>=interval[0]:
                intervals.append(interval)
        return intervals

    def search_recursive(self, point):
        intervals = self.point_in_node(point)
        if self.left is not None and point < self.median_value:
            intervals += self.left.search_recursive(point)
        elif self.right is not None and point > self.median_value:
            intervals += self.right.search_recursive(point)
        return intervals

def median(list intervals):
    if len(intervals)==0:
        return 0
    intervals.sort(key=itemgetter(1))
    if len(intervals)%2:
        return (intervals[len(intervals)/2][1] + intervals[len(intervals)/2-1][0])/2
    else:
        return (intervals[len(intervals)/2][0] + intervals[len(intervals)/2][1])/2


def divide_intervals(list intervals):
    """
    Returns an interval tree representing the given intervals.
    Does this using recursive partitioning by medians.
    """
    if len(intervals)==0:
        return None
    m = median(intervals)
    left = []
    right = []
    center = []
    for interval in intervals:
        if interval[1] < m:
            left.append(interval)
        elif interval[0] > m:
            right.append(interval)
        else:
            center.append(interval)
    center_right_sorted = sorted(center,key=itemgetter(1))
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

    cdef object interval_values, root

    def __init__(self, intervals, values):
        """
        Interval tree that is constructed from a list of intervals and a list
        of their associated values. The tree is fixed at construction and
        shouldn't be modified.
        """
        # step 1: sort intervals by endpoints 
        self.interval_values = {interval:v for interval,v in zip(intervals, values)}
        self.root = divide_intervals(intervals)

    def search_value(self, value):
        intervals = self.root.search_recursive(value)
        return intervals, [self.interval_values[i] for i in intervals]
