from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV422IBase(Format, ABC):
    """Base for all interleaved yuv422 formats."""
    @staticmethod
    def chroma_subsampling():
        return 2, 1

    def unpack(self, data):
        y = np.stack((data['frame']['y0'],
                      data['frame']['y1']), 3).reshape((-1, self._height, self._width))
        u = data['frame']['u0']
        v = data['frame']['v0']
        return y, u, v

    def pack(self, yuv):
        y, u, v = yuv
        data = np.empty(y.shape[0], dtype=self.dtype)
        y = y.reshape((-1, self._height, self._width // 2, 2))
        y0, y1 = y[:, :, :, 0], y[:, :, :, 1]
        data['frame']['y0'][:] = y0
        data['frame']['u0'][:] = u
        data['frame']['y1'][:] = y1
        data['frame']['v0'][:] = v
        return data


class YUV422I(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u1"),
              ('u0', "<u1"),
              ('y1', "<u1"),
              ('v0', "<u1")],
             (self._height, self._width // 2))
        ])


class YUV422I10LE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u2"),
              ('u0', "<u2"),
              ('y1', "<u2"),
              ('v0', "<u2")],
             (self._height, self._width // 2))
        ])


class YUV422I10BE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', ">u2"),
              ('u0', ">u2"),
              ('y1', ">u2"),
              ('v0', ">u2")],
             (self._height, self._width // 2))
        ])
    

class YUV422I16LE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u2"),
              ('u0', "<u2"),
              ('y1', "<u2"),
              ('v0', "<u2")],
             (self._height, self._width // 2))
        ])


class YUV422I16BE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', ">u2"),
              ('u0', ">u2"),
              ('y1', ">u2"),
              ('v0', ">u2")],
             (self._height, self._width // 2))
        ])


class YUV422I9LE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u2"),
              ('u0', "<u2"),
              ('y1', "<u2"),
              ('v0', "<u2")],
             (self._height, self._width // 2))
        ])


class YUV422I9BE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', ">u2"),
              ('u0', ">u2"),
              ('y1', ">u2"),
              ('v0', ">u2")],
             (self._height, self._width // 2))
        ])


class YUV422I12LE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u2"),
              ('u0', "<u2"),
              ('y1', "<u2"),
              ('v0', "<u2")],
             (self._height, self._width // 2))
        ])


class YUV422I12BE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', ">u2"),
              ('u0', ">u2"),
              ('y1', ">u2"),
              ('v0', ">u2")],
             (self._height, self._width // 2))
        ])


class YUV422I14LE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u2"),
              ('u0', "<u2"),
              ('y1', "<u2"),
              ('v0', "<u2")],
             (self._height, self._width // 2))
        ])


class YUV422I14BE(_YUV422IBase):
    @staticmethod
    def identifier():
        return "yuv422i14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', ">u2"),
              ('u0', ">u2"),
              ('y1', ">u2"),
              ('v0', ">u2")],
             (self._height, self._width // 2))
        ])


pixel_formats.register(YUV422I)
pixel_formats.register(YUV422I10LE)
pixel_formats.register(YUV422I10BE)
pixel_formats.register(YUV422I16LE)
pixel_formats.register(YUV422I16BE)
pixel_formats.register(YUV422I9LE)
pixel_formats.register(YUV422I9BE)
pixel_formats.register(YUV422I12LE)
pixel_formats.register(YUV422I12BE)
pixel_formats.register(YUV422I14LE)
pixel_formats.register(YUV422I14BE)
