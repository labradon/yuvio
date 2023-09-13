from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV444PBase(Format, ABC):
    """Base for all yuv444 formats."""
    @staticmethod
    def chroma_subsampling():
        return 1, 1

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


class YUV444P(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u1', (self._height, self._width)),
            ('u', '<u1', (self._height, self._width)),
            ('v', '<u1', (self._height, self._width))
        ])


class YUV444P10LE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width)),
            ('v', '<u2', (self._height, self._width))
        ])


class YUV444P10BE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width)),
            ('v', '>u2', (self._height, self._width))
        ])


class YUV444P16LE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width)),
            ('v', '<u2', (self._height, self._width))
        ])


class YUV444P16BE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width)),
            ('v', '>u2', (self._height, self._width))
        ])


class YUV444P9LE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width)),
            ('v', '<u2', (self._height, self._width))
        ])


class YUV444P9BE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width)),
            ('v', '>u2', (self._height, self._width))
        ])


class YUV444P12LE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width)),
            ('v', '<u2', (self._height, self._width))
        ])


class YUV444P12BE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width)),
            ('v', '>u2', (self._height, self._width))
        ])


class YUV444P14LE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width)),
            ('v', '<u2', (self._height, self._width))
        ])


class YUV444P14BE(_YUV444PBase):
    @staticmethod
    def identifier():
        return "yuv444p14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width)),
            ('v', '>u2', (self._height, self._width))
        ])


pixel_formats.register(YUV444P)
pixel_formats.register(YUV444P10LE)
pixel_formats.register(YUV444P10BE)
pixel_formats.register(YUV444P16LE)
pixel_formats.register(YUV444P16BE)
pixel_formats.register(YUV444P9LE)
pixel_formats.register(YUV444P9BE)
pixel_formats.register(YUV444P12LE)
pixel_formats.register(YUV444P12BE)
pixel_formats.register(YUV444P14LE)
pixel_formats.register(YUV444P14BE)
