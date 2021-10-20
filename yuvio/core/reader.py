from io import IOBase
from pathlib import Path
import psutil
import numpy as np
from . import YUVFrame
from . import Format


class Reader:

    def __init__(self, file, format: Format):
        if isinstance(file, IOBase):
            self._file = file
        else:
            self._file = open(Path(file).expanduser().resolve(), 'rb')
        self._format = format
        self._length = self._length_from_filesize()
        self._iter_idx = 0

    def __len__(self):
        return self._length

    def __iter__(self):
        for i in range(self._length):
            yield self.read(i, count=1)[0]

    def _length_from_filesize(self):
        return Path(self._file.name).stat().st_size // self._format.dtype.itemsize

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
            count = self._length
        if index + count > self._length:
            raise ValueError("Cannot read number of frames '{}' at index '{}' "
                             "from file '{}' with length '{}'.".format(count,
                                                                       index,
                                                                       self._file.name,
                                                                       self._length))
        self._validate_memory(count)
        self._file.seek(index * self._format.dtype.itemsize)
        unstructured_data = np.fromfile(self._file,
                                        self._format.dtype,
                                        count=count)
        y, u, v = self._format.unpack(unstructured_data)
        structured_data = np.empty(count,
                                   dtype=np.dtype([('y', y.dtype, y.shape[1:]),
                                                   ('u', u.dtype, u.shape[1:]),
                                                   ('v', v.dtype, v.shape[1:])]))
        structured_data['y'] = y
        structured_data['u'] = u
        structured_data['v'] = v
        yuv_frames = [YUVFrame(data, self._format.identifier()) for data in structured_data]
        return yuv_frames
