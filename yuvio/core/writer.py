from typing import Union, List
from io import IOBase
from pathlib import Path
import numpy as np
from . import YUVFrame
from . import Format


class Writer:

    def __init__(self, file, format: Format):
        if isinstance(file, IOBase):
            self._close = False
            self._file = file
        else:
            self._close = True
            self._file = open(Path(file).expanduser().resolve(), 'wb')
        self._format = format

    def __del__(self):
        if self._close:
            self._file.close()

    def write(self, yuv_frames: Union[List[YUVFrame], YUVFrame]):
        if isinstance(yuv_frames, YUVFrame):
            yuv_frames = [yuv_frames]
        frame_count = len(yuv_frames)
        if frame_count == 0:
            return

        if self._format.chroma_subsampling() != (0, 0):
            y = np.empty((frame_count, yuv_frames[0].y.shape[0], yuv_frames[0].y.shape[1]),
                         dtype=yuv_frames[0].y.dtype)
            u = np.empty((frame_count, yuv_frames[0].u.shape[0], yuv_frames[0].u.shape[1]),
                         dtype=yuv_frames[0].u.dtype)
            v = np.empty((frame_count, yuv_frames[0].v.shape[0], yuv_frames[0].v.shape[1]),
                         dtype=yuv_frames[0].v.dtype)
            for i, yuv_frame in enumerate(yuv_frames):
                y[i] = yuv_frame[0]
                u[i] = yuv_frame[1]
                v[i] = yuv_frame[2]
            data = self._format.pack((y, u, v))
        else:
            y = np.empty((frame_count, yuv_frames[0].y.shape[0], yuv_frames[0].y.shape[1]),
                         dtype=yuv_frames[0].y.dtype)
            for i, yuv_frame in enumerate(yuv_frames):
                y[i] = yuv_frame[0]
            data = self._format.pack((y, None, None))

        self._file.write(data.data)
