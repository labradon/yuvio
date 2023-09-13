from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
import numpy as np


class Format(ABC):

    def __init__(self, width, height):
        self._width = width
        self._height = height

    @classmethod
    def io_info(cls) -> str:
        """IO format info as
        '(component1 -> (height1, width1), component2 -> (height2, width2), ...)'"""
        sub_w, sub_h = cls.chroma_subsampling()
        if sub_w == 0 and sub_h == 0:
            return "y -> (height, width)"
        else:
            return "y -> (height, width), " \
                   "u/Cb -> (height / {1}, width / {0}), " \
                   "v/Cr -> (height / {1}, width / {0})".format(sub_w, sub_h)

    @staticmethod
    @abstractmethod
    def chroma_subsampling():
        """Return chroma subsampling as '(factor width, factor height)'."""
        pass

    @staticmethod
    @abstractmethod
    def bitdepth():
        """Return bitdepth of this format."""
        pass

    @staticmethod
    @abstractmethod
    def identifier():
        """Return the unique identifier for this format."""
        pass

    @property
    @abstractmethod
    def dtype(self) -> np.dtype:
        """Numpy dtype describing exactly one frame."""
        pass

    @abstractmethod
    def unpack(self, data: np.ndarray) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """Unpack the data described by dtype into raw components."""
        pass

    @abstractmethod
    def pack(self, raw: Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]) -> np.ndarray:
        """Pack the raw components into data described by dtype."""
        pass


class FormatManager:

    def __init__(self):
        self._formats: Dict[str, Format] = {}

    def register(self, format_cls: Format, overwrite: bool = False):
        pix_fmt = format_cls.identifier()
        if pix_fmt in self._formats and not overwrite:
            raise KeyError("Another format with identifier '{}' is registered already.".format(pix_fmt))
        self._formats[pix_fmt] = format_cls

    def __iter__(self):
        return iter(self._formats)

    def __len__(self):
        return len(self._formats)

    def __getitem__(self, key):
        return self._formats[key]

    def __setitem__(self, key, value):
        self.register(value, key)

    def __contains__(self, item):
        return item in self._formats

    def __str__(self):
        return ", ".join(list(self._formats.keys()))

    def io_description(self, pix_fmt: str):
        return self[pix_fmt].io_info()
