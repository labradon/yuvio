from typing import Union, List
from io import IOBase
from pathlib import Path
import numpy as np
from . import YUVFrame
from . import Format


class Writer:

    def __init__(self, file, format: Format):
        if isinstance(file, IOBase):
            self._file = file
        else:
            self._file = open(Path(file).resolve(), 'wb')
        self._format = format

    def write(self, yuv_frames: Union[List[YUVFrame], YUVFrame]):
        if isinstance(yuv_frames, YUVFrame):
            yuv_frames = [yuv_frames]
        frame_count = len(yuv_frames)
        if frame_count == 0:
            return
        y = np.empty((frame_count, yuv_frames[0].y.shape[0], yuv_frames[0].y.shape[1]), dtype=yuv_frames[0].y.dtype)
        u = np.empty((frame_count, yuv_frames[0].u.shape[0], yuv_frames[0].u.shape[1]), dtype=yuv_frames[0].u.dtype)
        v = np.empty((frame_count, yuv_frames[0].v.shape[0], yuv_frames[0].v.shape[1]), dtype=yuv_frames[0].v.dtype)
        for i, yuv_frame in enumerate(yuv_frames):
            y[i] = yuv_frame.y
            u[i] = yuv_frame.u
            v[i] = yuv_frame.v
        data = self._format.pack((y, u, v))
        data.tofile(self._file)
