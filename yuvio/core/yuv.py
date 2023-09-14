from typing import Union, Tuple, Optional
import numpy as np
from . import Format
from . import colorspaces


class YUVFrame:
    """YUVFrame provides convenient data access to a single yuv/ycbcr frame."""

    def __init__(self, y: np.ndarray,
                 u: Optional[np.ndarray],
                 v: Optional[np.ndarray],
                 yuv_format: Format):
        self._y = y
        self._u = u
        self._v = v
        self._yuv_format = yuv_format

    @property
    def pixel_format(self):
        return self._yuv_format.identifier()

    @property
    def yuv_format(self):
        return self._yuv_format

    @property
    def resolution(self):
        return self._y.shape[1], self._y.shape[0]

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: np.ndarray):
        self._y = value

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, value: Optional[np.ndarray]):
        self._u = value

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value: Optional[np.ndarray]):
        self._v = value

    @property
    def cb(self):
        return self._u

    @cb.setter
    def cb(self, value: np.ndarray):
        self._u = value

    @property
    def cr(self):
        return self._v

    @cr.setter
    def cr(self, value: np.ndarray):
        self._v = value

    def __getitem__(self, key: Union[str, int]):
        if isinstance(key, str):
            if key == 'y':
                key = 0
            elif key == 'u' or key == 'cb':
                key = 1
            elif key == 'v' or key == 'cr':
                key = 2

        return [self._y, self._u, self._v][key]

    def __setitem__(self, key: Union[str, int], value: np.ndarray):
        if isinstance(key, str):
            if key == 'y':
                key = 0
            elif key == 'u' or key == 'cb':
                key = 1
            elif key == 'v' or key == 'cr':
                key = 2

            [self._y, self._u, self._v][key] = value

    def set(self, yuv: Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]):
        self._y = yuv[0]
        self._u = yuv[1]
        self._v = yuv[2]

    def split(self):
        return self._y, self._u, self._v
