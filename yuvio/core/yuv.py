from typing import Union, Tuple
import numpy as np


class YUVFrame:
    """YUVFrame provides convenient data access to a single yuv/ycbcr frame."""

    def __init__(self, data, pixel_format: str):
        self._data = data
        self._pixel_format = pixel_format

    @property
    def pixel_format(self):
        return self._pixel_format

    @property
    def y(self):
        return self._data['y']

    @y.setter
    def y(self, value: np.ndarray):
        self._data['y'] = value

    @property
    def u(self):
        return self._data['u']

    @u.setter
    def u(self, value: np.ndarray):
        self._data['u'] = value

    @property
    def v(self):
        return self._data['v']

    @v.setter
    def v(self, value: np.ndarray):
        self._data['v'] = value

    @property
    def cb(self):
        return self._data['u']

    @cb.setter
    def cb(self, value: np.ndarray):
        self._data['u'] = value

    @property
    def cr(self):
        return self._data['v']

    @cr.setter
    def cr(self, value: np.ndarray):
        self._data['v'] = value

    def __getitem__(self, item: Union[str, int]):
        if isinstance(item, int):
            item = ('y', 'u', 'v')[item]
        elif isinstance(item, str):
            if item == 'cb':
                item = 'u'
            elif item == 'cr':
                item = 'v'
        return self._data[item]

    def __setitem__(self, key: Union[str, int], value: np.ndarray):
        if isinstance(key, int):
            key = ('y', 'u', 'v')[key]
        elif isinstance(key, str):
            if key == 'cb':
                key = 'u'
            elif key == 'cr':
                key = 'v'
        self._data[key] = value

    def set(self, yuv: Tuple[np.ndarray, np.ndarray, np.ndarray]):
        self._data['y'] = yuv[0]
        self._data['u'] = yuv[1]
        self._data['v'] = yuv[2]

    def split(self):
        return self._data['y'], self._data['u'], self._data['v']
