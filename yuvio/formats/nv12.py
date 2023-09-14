import numpy as np
from .. import pixel_formats
from ..core import Format


class NV12(Format):
    """NV12 A plane of 8bit Y samples follows by an interleaved plane of 8bit U/V yuv 420 format."""
    @staticmethod
    def identifier():
        return "nv12"

    @staticmethod
    def chroma_subsampling():
        return 2, 2

    @staticmethod
    def bitdepth():
        return 8

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u1', (self._height, self._width)),
            ('uv', '<u1', (self._height // 2, self._width))
        ])

    def unpack(self, data):
        y = data['y']
        u = data['uv'][:, :, ::2]
        v = data['uv'][:, :, 1::2]
        return y, u, v

    def pack(self, yuv):
        data = np.empty(yuv[0].shape[0], dtype=self.dtype)
        data['y'][:] = yuv[0]
        data['uv'][:, :, ::2] = yuv[1]
        data['uv'][:, :, 1::2] = yuv[2]
        return data


pixel_formats.register(NV12)
