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

    @property
    def dtype(self):
        return np.dtype([
            ('y', '<u1', (self._height, self._width)),
            ('uv', '<u1', (self._height // 2, self._width))
        ])

    def unpack(self, data):
        #I was getting some strange behaviours when I tried naming the variables y, u & v.
        #Renaming them to yy, uu, vv solved it which hints at a variable uniqueness issue.
        yy = data['y']
        uu = np.split(data['uv'].reshape((data['uv'].size // 2, 2)), 2, axis=1)[0].reshape((self._height // 2, self._width // 2))
        vv = np.split(data['uv'].reshape((data['uv'].size // 2, 2)), 2, axis=1)[1].reshape((self._height // 2, self._width // 2))

        return yy, uu, vv

    def pack(self, yuv):
        #I was getting some strange behaviours when I tried naming the variables y, u & v.
        #Renaming them to yy, uu, vv solved it which hints at a variable uniqueness issue.
        yy = yuv[0]
        uu = yuv[1]
        vv = yuv[2]

        data = np.empty(yy.shape[0], dtype=self.dtype)

        data['y'][:]  = yy
        data['uv'][:] = np.concatenate((uu.reshape((uu.size,1)),vv.reshape((vv.size,1))),axis=1).reshape((self._height // 2, self._width))

        return data


pixel_formats.register(NV12)
