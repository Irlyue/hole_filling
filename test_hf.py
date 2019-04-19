import unittest
import numpy as np

from hf import fill_bg_with_fg
from collections import defaultdict, deque


def py_fill_bg_with_fg(mask):
    """
    1. Get the connected components labeled as background;
    2. Test each connected components following:
        - If the component is strictly surrounded by one class, label it as that
        class;
        - Otherwise, do nothing

    :param mask: np.array, shape(h, w)
    :return:
        mask: a copy of the input but with some background regions filled
              with foreground class.
    """
    mask = mask.copy()
    neighbor, visited = calc_bg_neighbors(mask)
    for idx, classes in neighbor.items():
        if len(classes) == 1:
            mask[visited == idx] = list(classes)[0]
    return mask


def calc_bg_neighbors(mask):
    """
    Calculate how many neighbors are there for each connected background area. Each
    connected component will be labeled with different integer(see the return values
    for details).

    <<WARN>> This implementation is really inefficient since a 300 by 500 mask needs
    about 0.8 seconds to process.

    Examples
    --------
    >>> a = (np.array([
    ...   [0, 0, 0, 0, 0],
    ...   [0, 1, 1, 1, 0],
    ...   [0, 1, 0, 1, 0],
    ...   [0, 1, 1, 1, 0],
    ...   [0, 0, 0, 0, 0]]))
    >>> neighbor, visited = calc_bg_neighbors(a)
    >>> neighbor
    defaultdict(<class 'set'>, {1: {1, -1}, 2: {1}})
    >>> print(visited)
    [[1 1 1 1 1]
     [1 0 0 0 1]
     [1 0 2 0 1]
     [1 0 0 0 1]
     [1 1 1 1 1]]

    :param mask: np.array, shape(h, w)
    :return:
        neighbor: dict, integer->set of neighboring classes, image boundary is also
                  considered as one class and is labelled as -1.
        visited: np.array, same shape as `mask`, given the connected components.
    """
    def in_range(pi, pj):
        return (0 <= pi < h) and (0 <= pj < w)

    def visit_from(pi, pj):
        q = deque()
        q.append((pi, pj))
        visited[pi, pj] = counter
        while len(q) != 0:
            topi, topj = q.popleft()
            for dx, dy in zip([1, 0, -1, 0], [0, 1, 0, -1]):
                nexti, nextj = topi + dx, topj + dy
                if in_range(nexti, nextj):
                    if mask[nexti, nextj] == 0 and visited[nexti, nextj] == 0:
                        q.append((nexti, nextj))
                        visited[nexti, nextj] = counter
                    if mask[nexti, nextj] != 0:
                        neighbor[counter].add(mask[nexti, nextj])
                else:
                    neighbor[counter].add(-1)
    neighbor = defaultdict(set)
    counter = 0
    h, w = mask.shape
    visited = np.zeros((h, w), dtype=np.int32)
    for i, j in ((i, j) for i in range(h) for j in range(w)):
        if visited[i, j] == 0 and mask[i, j] == 0:
            counter += 1
            visit_from(i, j)
    return neighbor, visited


class TestHoleFilling(unittest.TestCase):
    def test_all_background(self):
        a = np.zeros((4, 5), dtype=np.int32)
        b = np.zeros((4, 5), dtype=np.int32)
        self.assertTrue(np.all(fill_bg_with_fg(a) == b))

    def test_small_one(self):
        a = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]], dtype=np.int32)
        b = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ])
        self.assertTrue(np.all(fill_bg_with_fg(a) == b))

    def test_small_against_python_version(self):
        np.random.seed(2)
        for i in range(10):
            a = np.random.randint(21, size=(40, 60), dtype=np.int32)
            b = py_fill_bg_with_fg(a)
            c = fill_bg_with_fg(a)
            self.assertTrue(np.all(b == c))

    def test_big_against_python_version(self):
        np.random.seed(2)
        for i in range(10):
            a = np.random.randint(21, size=(400, 600), dtype=np.int32)
            b = py_fill_bg_with_fg(a)
            c = fill_bg_with_fg(a)
            self.assertTrue(np.all(b == c))
