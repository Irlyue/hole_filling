import numpy as np
from time import time

from hf import fill_bg_with_fg
from test_hf import py_fill_bg_with_fg
from PIL import Image


def main():
    a = np.array(Image.open('images/2008_003255.png'), dtype=np.int32)
    print(f'Trying on {a.shape} mask!')

    tic = time()
    b = fill_bg_with_fg(a)
    toc = time()
    print(f'C extension code done in {toc - tic} seconds!')

    tic = time()
    c = py_fill_bg_with_fg(a)
    toc = time()
    print(f'Python code done in {toc - tic} seconds!')
    assert np.all(b == c)


if __name__ == '__main__':
    main()
