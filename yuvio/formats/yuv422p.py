from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV422PBase(Format, ABC):
    """Base for all yuv422 formats."""
    @staticmethod
    def chroma_subsampling():
        return 2, 1

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


class YUV422P(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u1', (self._height, self._width)),
            ('u', '<u1', (self._height, self._width // 2)),
            ('v', '<u1', (self._height, self._width // 2))
        ])


class YUV422P10LE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width // 2)),
            ('v', '<u2', (self._height, self._width // 2))
        ])


class YUV422P10BE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width // 2)),
            ('v', '>u2', (self._height, self._width // 2))
        ])


class YUV422P16LE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width // 2)),
            ('v', '<u2', (self._height, self._width // 2))
        ])


class YUV422P16BE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width // 2)),
            ('v', '>u2', (self._height, self._width // 2))
        ])


class YUV422P9LE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width // 2)),
            ('v', '<u2', (self._height, self._width // 2))
        ])


class YUV422P9BE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width // 2)),
            ('v', '>u2', (self._height, self._width // 2))
        ])


class YUV422P12LE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width // 2)),
            ('v', '<u2', (self._height, self._width // 2))
        ])


class YUV422P12BE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width // 2)),
            ('v', '>u2', (self._height, self._width // 2))
        ])


class YUV422P14LE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u2', (self._height, self._width)),
            ('u', '<u2', (self._height, self._width // 2)),
            ('v', '<u2', (self._height, self._width // 2))
        ])


class YUV422P14BE(_YUV422PBase):
    @staticmethod
    def identifier():
        return "yuv422p14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('y', '>u2', (self._height, self._width)),
            ('u', '>u2', (self._height, self._width // 2)),
            ('v', '>u2', (self._height, self._width // 2))
        ])


pixel_formats.register(YUV422P)
pixel_formats.register(YUV422P10LE)
pixel_formats.register(YUV422P10BE)
pixel_formats.register(YUV422P16LE)
pixel_formats.register(YUV422P16BE)
pixel_formats.register(YUV422P9LE)
pixel_formats.register(YUV422P9BE)
pixel_formats.register(YUV422P12LE)
pixel_formats.register(YUV422P12BE)
pixel_formats.register(YUV422P14LE)
pixel_formats.register(YUV422P14BE)
