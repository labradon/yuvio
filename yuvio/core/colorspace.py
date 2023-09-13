from typing import List, Tuple
import numpy as np
from . import Format


class Colorspace:
    def __init__(self, rgb_conversion_coefficients: List[int], y_baseoffset: int):
        self._rgb_coefficients = rgb_conversion_coefficients
        self._y_baseoffset = y_baseoffset

    def to_rgb(self, y, u, v, yuv_format: Format) -> np.ndarray:
        bitdepth = yuv_format.bitdepth()
        max_value = 2 ** bitdepth - 1
        dtype = y.dtype

        y = y.astype(np.int64)
        u = u.astype(np.int64)
        v = v.astype(np.int64)

        # Upsample if necessary (rough nearest neighbor for now -> needs improvement)
        factor_width, factor_height = yuv_format.chroma_subsampling()
        if factor_height > 1:
            u = np.repeat(u, factor_height, axis=0)
            v = np.repeat(v, factor_height, axis=0)
        if factor_width > 1:
            u = np.repeat(u, factor_width, axis=1)
            v = np.repeat(v, factor_width, axis=1)

        # Color conversion
        y_offset = self._y_baseoffset << (bitdepth - 8)
        c_zero = 128 << (bitdepth - 8)

        y_tmp = (y - y_offset) * self._rgb_coefficients[0]
        u_tmp = u - c_zero
        v_tmp = v - c_zero

        r_tmp = (y_tmp + v_tmp * self._rgb_coefficients[1]) >> 16
        g_tmp = (y_tmp + u_tmp * self._rgb_coefficients[2] + v_tmp * self._rgb_coefficients[3]) >> 16
        b_tmp = (y_tmp + u_tmp * self._rgb_coefficients[4]) >> 16

        r = np.clip(r_tmp, 0, max_value).astype(dtype)
        g = np.clip(g_tmp, 0, max_value).astype(dtype)
        b = np.clip(b_tmp, 0, max_value).astype(dtype)

        return np.stack((r, g, b), axis=-1)

    def from_rgb(self, rgb_frame: np.ndarray, yuv_format: Format) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        bitdepth = yuv_format.bitdepth()
        rgb = rgb_frame.astype(np.int64)

        a = int(np.round(0.2126 * (224/255) * (2**16)))
        b = int(np.round(0.7152 * (224/255) * (2**16)))
        c = int(np.round(0.0722 * (224/255) * (2**16)))
        d = int(np.round(1/1.8556 * (2**16)))
        e = int(np.round(1/1.5748 * (2**16)))
        scale = int(np.round((224/255) * (2**16)))

        y = a * rgb[..., 0] + b * rgb[..., 1] + c * rgb[..., 2]
        u = (rgb[..., 2] * scale - y) * d
        v = (rgb[..., 0] * scale - y) * e

        y_offset = self._y_baseoffset << (bitdepth - 8)
        c_zero = 128 << (bitdepth - 8)

        y = (y.astype(np.int64) >> 16) + y_offset
        u = (u.astype(np.int64) >> 32) + c_zero
        v = (v.astype(np.int64) >> 32) + c_zero

        return y, u, v


class ColorspaceManager:
    def __init__(self):
        self._conversions = {
            ('bt601', 'limited'): Colorspace([76309, 104597, -25675, -53279, 132201], 16),
            ('bt601', 'full'): Colorspace([65536, 91881, -22553, -46802, 116129], 0),
            ('bt709', 'limited'): Colorspace([76309, 117489, -13975, -34925, 138438], 16),
            ('bt709', 'full'): Colorspace([65536, 103206, -12276, -30679, 121608], 0),
            ('bt2020', 'limited'): Colorspace([76309, 110013, -12276, -42626, 140363], 16),
            ('bt2020', 'full'): Colorspace([65536, 96638, -10783, -37444, 123299], 0),
        }

    def __getitem__(self, key: Tuple[str, str]):
        identifier, value_range = key
        return self._conversions[(identifier, value_range)]

    def __str__(self):
        return ", ".join(list(map(
            lambda key: f"({key[0]}, {key[1]})",
            self._conversions.keys()
        )))


colorspaces = ColorspaceManager()
