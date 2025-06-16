from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV444IBase(Format, ABC):
    """Base for all interleaved yuv444 formats."""
    @staticmethod
    def chroma_subsampling():
        return 1, 1

    def unpack(self, data):
        y = data['frame']['y']
        u = data['frame']['u']
        v = data['frame']['v']
        return y, u, v

    def pack(self, yuv):
        data = np.empty(yuv[0].shape[0], dtype=self.dtype)
        data['frame']['y'][:] = yuv[0]
        data['frame']['u'][:] = yuv[1]
        data['frame']['v'][:] = yuv[2]
        return data


class YUV444I(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u1"),
              ('u', "<u1"),
              ('v', "<u1")],
             (self._height, self._width))
        ])


class YUV444I10LE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u2"),
              ('u', "<u2"),
              ('v', "<u2")],
             (self._height, self._width))
        ])


class YUV444I10BE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', ">u2"),
              ('u', ">u2"),
              ('v', ">u2")],
             (self._height, self._width))
        ])


class YUV444I16LE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u2"),
              ('u', "<u2"),
              ('v', "<u2")],
             (self._height, self._width))
        ])


class YUV444I16BE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', ">u2"),
              ('u', ">u2"),
              ('v', ">u2")],
             (self._height, self._width))
        ])


class YUV444I9LE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u2"),
              ('u', "<u2"),
              ('v', "<u2")],
             (self._height, self._width))
        ])


class YUV444I9BE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', ">u2"),
              ('u', ">u2"),
              ('v', ">u2")],
             (self._height, self._width))
        ])


class YUV444I12LE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u2"),
              ('u', "<u2"),
              ('v', "<u2")],
             (self._height, self._width))
        ])


class YUV444I12BE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', ">u2"),
              ('u', ">u2"),
              ('v', ">u2")],
             (self._height, self._width))
        ])


class YUV444I14LE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', "<u2"),
              ('u', "<u2"),
              ('v', "<u2")],
             (self._height, self._width))
        ])


class YUV444I14BE(_YUV444IBase):
    @staticmethod
    def identifier():
        return "yuv444i14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y', ">u2"),
              ('u', ">u2"),
              ('v', ">u2")],
             (self._height, self._width))
        ])


pixel_formats.register(YUV444I)
pixel_formats.register(YUV444I10LE)
pixel_formats.register(YUV444I10BE)
pixel_formats.register(YUV444I16LE)
pixel_formats.register(YUV444I16BE)
pixel_formats.register(YUV444I9LE)
pixel_formats.register(YUV444I9BE)
pixel_formats.register(YUV444I12LE)
pixel_formats.register(YUV444I12BE)
pixel_formats.register(YUV444I14LE)
pixel_formats.register(YUV444I14BE)
