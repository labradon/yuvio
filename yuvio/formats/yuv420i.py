from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _YUV420IBase(Format, ABC):
    """Base for all interleaved yuv420 formats."""
    @staticmethod
    def chroma_subsampling():
        return 2, 2

    def unpack(self, data):
        even_lines = data['frame']['even_line']
        odd_lines = data['frame']['odd_line']

        frames = even_lines.shape[0]
        y = np.empty((frames, self._height, self._width), dtype=even_lines['y0'].dtype)

        y[:, 0::2, 0::2] = even_lines['y0']
        y[:, 0::2, 1::2] = even_lines['y1']
        y[:, 1::2, :] = odd_lines
        u = even_lines['u0']
        v = even_lines['v0']
        return y, u, v

    def pack(self, yuv):
        y, u, v = yuv
        data = np.empty(y.shape[0], dtype=self.dtype)
        data['frame']['even_line']['y0'][:] = y[:, 0::2, 0::2]
        data['frame']['even_line']['y1'][:] = y[:, 0::2, 1::2]
        data['frame']['odd_line'][:] = y[:, 1::2, :]
        data['frame']['even_line']['u0'][:] = u
        data['frame']['even_line']['v0'][:] = v
        return data


class YUV420I(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u1"), ('u0', "<u1"), ('y1', "<u1"), ('v0', "<u1")], (self._width // 2)),
                ('odd_line', "<u1", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I10LE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i10le"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u2"), ('u0', "<u2"), ('y1', "<u2"), ('v0', "<u2")], (self._width // 2)),
                ('odd_line', "<u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I10BE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i10be"

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', ">u2"), ('u0', ">u2"), ('y1', ">u2"), ('v0', ">u2")], (self._width // 2)),
                ('odd_line', ">u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I16LE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i16le"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u2"), ('u0', "<u2"), ('y1', "<u2"), ('v0', "<u2")], (self._width // 2)),
                ('odd_line', "<u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I16BE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i16be"

    @staticmethod
    def bitdepth():
        return 16

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', ">u2"), ('u0', ">u2"), ('y1', ">u2"), ('v0', ">u2")], (self._width // 2)),
                ('odd_line', ">u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I9LE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i9le"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u2"), ('u0', "<u2"), ('y1', "<u2"), ('v0', "<u2")], (self._width // 2)),
                ('odd_line', "<u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I9BE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i9be"

    @staticmethod
    def bitdepth():
        return 9

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', ">u2"), ('u0', ">u2"), ('y1', ">u2"), ('v0', ">u2")], (self._width // 2)),
                ('odd_line', ">u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I12LE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i12le"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u2"), ('u0', "<u2"), ('y1', "<u2"), ('v0', "<u2")], (self._width // 2)),
                ('odd_line', "<u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I12BE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i12be"

    @staticmethod
    def bitdepth():
        return 12

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', ">u2"), ('u0', ">u2"), ('y1', ">u2"), ('v0', ">u2")], (self._width // 2)),
                ('odd_line', ">u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I14LE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i14le"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', "<u2"), ('u0', "<u2"), ('y1', "<u2"), ('v0', "<u2")], (self._width // 2)),
                ('odd_line', "<u2", self._width)
             ],
             (self._height // 2))
        ])


class YUV420I14BE(_YUV420IBase):
    @staticmethod
    def identifier():
        return "yuv420i14be"

    @staticmethod
    def bitdepth():
        return 14

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [
                ('even_line', [('y0', ">u2"), ('u0', ">u2"), ('y1', ">u2"), ('v0', ">u2")], (self._width // 2)),
                ('odd_line', ">u2", self._width)
             ],
             (self._height // 2))
        ])


pixel_formats.register(YUV420I)
pixel_formats.register(YUV420I10LE)
pixel_formats.register(YUV420I10BE)
pixel_formats.register(YUV420I16LE)
pixel_formats.register(YUV420I16BE)
pixel_formats.register(YUV420I9LE)
pixel_formats.register(YUV420I9BE)
pixel_formats.register(YUV420I12LE)
pixel_formats.register(YUV420I12BE)
pixel_formats.register(YUV420I14LE)
pixel_formats.register(YUV420I14BE)
