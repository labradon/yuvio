import numpy as np
from .. import pixel_formats
from ..core import Format


class V210(Format):
    """V210 interleaved 10bit yuv 422 format."""
    @staticmethod
    def identifier():
        return "v210"

    @staticmethod
    def chroma_subsampling():
        return 2, 1

    @staticmethod
    def bitdepth():
        return 10

    @property
    def dtype(self):
        return np.dtype([
            ('frame',
             [('word0', "<u4"),
              ('word1', "<u4"),
              ('word2', "<u4"),
              ('word3', "<u4")],
             ((self._height * self._width) // 6))
        ])

    def unpack(self, data):
        word0 = data['frame']['word0']
        cr0 = np.right_shift(np.bitwise_and(word0, (0x3ff << 20)), 20).astype(np.uint16)
        y0 = np.right_shift(np.bitwise_and(word0, (0x3ff << 10)), 10).astype(np.uint16)
        cb0 = np.bitwise_and(word0, 0x3ff).astype(np.uint16)

        word1 = data['frame']['word1']
        y2 = np.right_shift(np.bitwise_and(word1, (0x3ff << 20)), 20).astype(np.uint16)
        cb1 = np.right_shift(np.bitwise_and(word1, (0x3ff << 10)), 10).astype(np.uint16)
        y1 = np.bitwise_and(word1, 0x3ff).astype(np.uint16)

        word2 = data['frame']['word2']
        cb2 = np.right_shift(np.bitwise_and(word2, (0x3ff << 20)), 20).astype(np.uint16)
        y3 = np.right_shift(np.bitwise_and(word2, (0x3ff << 10)), 10).astype(np.uint16)
        cr1 = np.bitwise_and(word2, 0x3ff).astype(np.uint16)

        word3 = data['frame']['word3']
        y5 = np.right_shift(np.bitwise_and(word3, (0x3ff << 20)), 20).astype(np.uint16)
        cr2 = np.right_shift(np.bitwise_and(word3, (0x3ff << 10)), 10).astype(np.uint16)
        y4 = np.bitwise_and(word3, 0x3ff).astype(np.uint16)

        y = np.stack((y0, y1, y2, y3, y4, y5), 2).reshape((-1, self._height, self._width))
        u = np.stack((cb0, cb1, cb2), 2).reshape((-1, self._height, self._width // 2))
        v = np.stack((cr0, cr1, cr2), 2).reshape((-1, self._height, self._width // 2))

        return y, u, v

    def pack(self, yuv):
        y, u, v = yuv
        y = y.reshape((-1, (self._height * self._width) // 6, 6))
        u = u.reshape((-1, (self._height * self._width) // 6, 3))
        v = v.reshape((-1, (self._height * self._width) // 6, 3))
        y0, y1, y2, y3, y4, y5 = y[:, :, 0], y[:, :, 1], y[:, :, 2], y[:, :, 3], y[:, :, 4], y[:, :, 5]
        cb0, cb1, cb2 = u[:, :, 0], u[:, :, 1], u[:, :, 2]
        cr0, cr1, cr2 = v[:, :, 0], v[:, :, 1], v[:, :, 2]

        data = np.empty(y.shape[0], dtype=self.dtype)
        data['frame']['word0'] = np.left_shift(cr0.astype(np.uint32), 20) \
                                 + np.left_shift(y0.astype(np.uint32), 10) \
                                 + cb0.astype(np.uint32)
        data['frame']['word1'] = np.left_shift(y2.astype(np.uint32), 20) \
                                 + np.left_shift(cb1.astype(np.uint32), 10) \
                                 + y1.astype(np.uint32)
        data['frame']['word2'] = np.left_shift(cb2.astype(np.uint32), 20) \
                                 + np.left_shift(y3.astype(np.uint32), 10) \
                                 + cr1.astype(np.uint32)
        data['frame']['word3'] = np.left_shift(y5.astype(np.uint32), 20) \
                                 + np.left_shift(cr2.astype(np.uint32), 10) \
                                 + y4.astype(np.uint32)
        return data


pixel_formats.register(V210)
