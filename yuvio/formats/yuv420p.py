from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV420PBase(Format, ABC):
    """Base for all yuv420 formats."""
    @staticmethod
    def chroma_subsampling():
        return 2, 2

    def unpack(self, data):
        y = data['y']
        u = data['u']
        v = data['v']
        return y, u, v

    def pack(self, yuv):
        data = np.empty(yuv[0].shape[0], dtype=self.dtype)
        data['y'][:] = yuv[0]
        data['u'][:] = yuv[1]
        data['v'][:] = yuv[2]
        return data


class YUV420P(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u1', (self._height, self._width)),
            ('u', '<u1', (self._height // 2, self._width // 2)),
            ('v', '<u1', (self._height // 2, self._width // 2))
        ])


class YUV420P10LE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height // 2, self._width // 2)),
            ('v', '<u2', (self._height // 2, self._width // 2))
        ])


class YUV420P10BE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height // 2, self._width // 2)),
            ('v', '>u2', (self._height // 2, self._width // 2))
        ])


class YUV420P16LE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height // 2, self._width // 2)),
            ('v', '<u2', (self._height // 2, self._width // 2))
        ])


class YUV420P16BE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height // 2, self._width // 2)),
            ('v', '>u2', (self._height // 2, self._width // 2))
        ])


class YUV420P9LE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height // 2, self._width // 2)),
            ('v', '<u2', (self._height // 2, self._width // 2))
        ])


class YUV420P9BE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height // 2, self._width // 2)),
            ('v', '>u2', (self._height // 2, self._width // 2))
        ])

class YUV420P12LE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height // 2, self._width // 2)),
            ('v', '<u2', (self._height // 2, self._width // 2))
        ])


class YUV420P12BE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height // 2, self._width // 2)),
            ('v', '>u2', (self._height // 2, self._width // 2))
        ])


class YUV420P14LE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height // 2, self._width // 2)),
            ('v', '<u2', (self._height // 2, self._width // 2))
        ])


class YUV420P14BE(_YUV420PBase):
    @staticmethod
    def identifier():
        return "yuv420p14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height // 2, self._width // 2)),
            ('v', '>u2', (self._height // 2, self._width // 2))
        ])


pixel_formats.register(YUV420P)
pixel_formats.register(YUV420P10LE)
pixel_formats.register(YUV420P10BE)
pixel_formats.register(YUV420P16LE)
pixel_formats.register(YUV420P16BE)
pixel_formats.register(YUV420P9LE)
pixel_formats.register(YUV420P9BE)
pixel_formats.register(YUV420P12LE)
pixel_formats.register(YUV420P12BE)
pixel_formats.register(YUV420P14LE)
pixel_formats.register(YUV420P14BE)
