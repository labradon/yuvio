from abc import ABC
import numpy as np
from .. import pixel_formats
from ..core import Format


class _Interleaved422Base(Format, ABC):
    """Base for all interleaved 422 formats."""
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


class YUYV422(_Interleaved422Base):
    @staticmethod
    def identifier():
        return "yuyv422"

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


class UYVY422(_Interleaved422Base):
    @staticmethod
    def identifier():
        return "uyvy422"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('u0', "<u1"),
              ('y0', "<u1"),
              ('v0', "<u1"),
              ('y1', "<u1")],
             (self._height, self._width // 2))
        ])


class YVYU422(_Interleaved422Base):
    @staticmethod
    def identifier():
        return "yvyu422"

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('y0', "<u1"),
              ('v0', "<u1"),
              ('y1', "<u1"),
              ('u0', "<u1")],
             (self._height, self._width // 2))
        ])


pixel_formats.register(YUYV422)
pixel_formats.register(UYVY422)
pixel_formats.register(YVYU422)
