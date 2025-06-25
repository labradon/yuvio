from typing import Union
import io
from pathlib import Path
import psutil
import numpy as np
from . import YUVFrame
from . import Format


class Reader:

    def __init__(self, file: Union[Path, str, io.RawIOBase, io.BufferedIOBase], format: Format):
        if isinstance(file, io.RawIOBase) or isinstance(file, io.BufferedIOBase):
            self._owns = False
            self._file = file
        else:
            self._owns = True
            self._file = open(Path(file).expanduser().resolve(), 'rb')
            self._open = True
        self._format = format
        self._start_offset = self._file.tell()
        self._length = self._length_from_stream()
        self._iter_idx = 0

    def close(self):
        if not self._owns:
            raise RuntimeError("Cannot close unowned IO handle.")
        if not self._open:
            raise IOError("File is already closed.")
        self._file.close()
        self._open = False

    def __del__(self):
        if self._owns and self._open:
            self.close()

    def __len__(self):
        return self._length

    def __iter__(self):
        for i in range(self._length):
            yield self.read(i, count=1)[0]

    def _length_from_stream(self):
        self._file.seek(0, io.SEEK_END)
        num_bytes = self._file.tell() - self._start_offset
        self._file.seek(self._start_offset, io.SEEK_SET)
        return num_bytes // self._format.dtype.itemsize

    def _validate_memory(self, count):
        available = psutil.virtual_memory().available
        required = count * self._format.dtype.itemsize
        if required > available * 0.9:
            raise RuntimeError("The required memory ({}) to read '{}' frames "
                               "from file '{}' exceeds 90% of the available system "
                               "memory ({})".format(required,
                                                    count,
                                                    self._file.name,
                                                    available))

    def read(self, index, count=None):
        if count is None:
            count = self._length - index
        if index + count > self._length:
            raise ValueError("Cannot read number of frames '{}' at index '{}' "
                             "from file '{}' with length '{}'.".format(count,
                                                                       index,
                                                                       self._file.name,
                                                                       self._length))
        self._validate_memory(count)
        self._file.seek(self._start_offset + index * self._format.dtype.itemsize)
        data = np.empty(count, dtype=self._format.dtype)
        self._file.readinto(data.data)
        return self.unpack_data(data)

    def unpack_data(self, data):
        y_frames, u_frames, v_frames = self._format.unpack(data)

        yuv_frames = []
        if self._format.chroma_subsampling() != (0, 0):
            for y_frame, u_frame, v_frame in zip(y_frames, u_frames, v_frames):
                yuv_frames.append(YUVFrame(y_frame, u_frame, v_frame, self._format))
        else:
            for y_frame in y_frames:
                yuv_frames.append(YUVFrame(y_frame, None, None, self._format))
        return yuv_frames
