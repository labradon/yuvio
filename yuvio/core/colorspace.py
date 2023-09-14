from typing import List, Tuple
import numpy as np
from . import Format


class Colorspace:
    def __init__(self, coefficients: List[float],
                 y_baserange: Tuple[int, int],
                 cbcr_baserange: Tuple[int, int],
                 video_basemargin: int):
        self._coefficients = coefficients
        self._y_baserange = y_baserange
        self._cbcr_baserange = cbcr_baserange
        self._video_basemargin = video_basemargin
        self._precompute_16bit_conversion_coefficients()

    def _precompute_16bit_conversion_coefficients(self):
        a, b, c, d, e = self._coefficients
        y_baselength = self._y_baserange[1] - self._y_baserange[0]
        cbcr_baselength = self._cbcr_baserange[1] - self._cbcr_baserange[0]

        y_scale_torgb_16bit = int(np.round((255 / y_baselength) * (2 ** 16)))
        d_torgb_16bit = int(np.round(d * (255 / cbcr_baselength) * (2 ** 16)))
        e_torgb_16bit = int(np.round(e * (255 / cbcr_baselength) * (2 ** 16)))
        ae_b_torgb_16bit = int(np.round((a * e / b) * (255 / cbcr_baselength) * (2 ** 16)))
        cd_b_torgb_16bit = int(np.round((c * d / b) * (255 / cbcr_baselength) * (2 ** 16)))
        self._to_rgb_coefficients = [y_scale_torgb_16bit,
                                     d_torgb_16bit, e_torgb_16bit,
                                     ae_b_torgb_16bit, cd_b_torgb_16bit]

        a_fromrgb_16bit = int(np.round(a * (2 ** 16)))
        b_fromrgb_16bit = int(np.round(b * (2 ** 16)))
        c_fromrgb_16bit = int(np.round(c * (2 ** 16)))
        inv_d_fromrgb_16bit = int(np.round((1 / d) * (2 ** 16)))
        inv_e_fromrgb_16bit = int(np.round((1 / e) * (2 ** 16)))
        y_scale_fromrgb_16bit = int(np.round((y_baselength / 255) * (2 ** 16)))
        cbcr_scale_fromrgb_16bit = int(np.round((cbcr_baselength / 255) * (2 ** 16)))
        self._from_rgb_coefficients = [a_fromrgb_16bit, b_fromrgb_16bit, c_fromrgb_16bit,
                                       inv_d_fromrgb_16bit, inv_e_fromrgb_16bit,
                                       y_scale_fromrgb_16bit, cbcr_scale_fromrgb_16bit]

    def to_rgb(self, y, u, v, yuv_format: Format) -> np.ndarray:
        if yuv_format.chroma_subsampling()[0] != 1 or yuv_format.chroma_subsampling()[1] != 1:
            raise ValueError("Color conversion is only possible for 444 yuv (ycbcr) formats (no chroma subsampling). "
                             f"'{yuv_format.identifier()}' entails chroma subsampling.")
        bitdepth = yuv_format.bitdepth()
        max_value = 2 ** bitdepth - 1
        dtype = y.dtype

        y = y.astype(np.int64)
        u = u.astype(np.int64)
        v = v.astype(np.int64)

        # Color conversion
        y_offset = self._y_baserange[0] << (bitdepth - 8)
        chroma_center = 128 << (bitdepth - 8)

        y = (y - y_offset)
        u = (u - chroma_center)
        v = (v - chroma_center)

        (y_scale_torgb_16bit,
         d_torgb_16bit, e_torgb_16bit,
         ae_b_torgb_16bit, cd_b_torgb_16bit) = self._to_rgb_coefficients
        y_16bit = y * y_scale_torgb_16bit
        r = (y_16bit + e_torgb_16bit * v) >> 16
        g = (y_16bit - ae_b_torgb_16bit * v - cd_b_torgb_16bit * u) >> 16
        b = (y_16bit + d_torgb_16bit * u) >> 16

        r = np.clip(r, 0, max_value).astype(dtype)
        g = np.clip(g, 0, max_value).astype(dtype)
        b = np.clip(b, 0, max_value).astype(dtype)

        return np.stack((r, g, b), axis=-1)

    def from_rgb(self, rgb_frame: np.ndarray, yuv_format: Format) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if yuv_format.chroma_subsampling()[0] != 1 or yuv_format.chroma_subsampling()[1] != 1:
            raise ValueError("Color conversion is only possible for 444 yuv (ycbcr) formats (no chroma subsampling). "
                             f"'{yuv_format.identifier()}' entails chroma subsampling.")
        bitdepth = yuv_format.bitdepth()
        rgb = rgb_frame.astype(np.int64)

        (a_fromrgb_16bit, b_fromrgb_16bit, c_fromrgb_16bit,
         inv_d_fromrgb_16bit, inv_e_fromrgb_16bit,
         y_scale_fromrgb_16bit, cbcr_scale_fromrgb_16bit) = self._from_rgb_coefficients

        y = a_fromrgb_16bit * rgb[..., 0] + b_fromrgb_16bit * rgb[..., 1] + c_fromrgb_16bit * rgb[..., 2]
        u = (((rgb[..., 2] << 16) - y) * inv_d_fromrgb_16bit) >> 16
        v = (((rgb[..., 0] << 16) - y) * inv_e_fromrgb_16bit) >> 16

        bitdepth_shift = bitdepth - 8
        y_low = self._y_baserange[0] << bitdepth_shift
        chroma_center = 128 << bitdepth_shift

        y = ((y * y_scale_fromrgb_16bit) >> 32) + y_low
        u = ((u * cbcr_scale_fromrgb_16bit) >> 32) + chroma_center
        v = ((v * cbcr_scale_fromrgb_16bit) >> 32) + chroma_center

        clip_low = self._video_basemargin << bitdepth_shift
        clip_high = (1 << bitdepth) - 1 - clip_low
        y = np.clip(y, clip_low, clip_high)
        u = np.clip(u, clip_low, clip_high)
        v = np.clip(v, clip_low, clip_high)

        return y, u, v


class ColorspaceManager:
    def __init__(self):
        # For colorspace parameters, see:
        # - BT.601: https://www.itu.int/rec/R-REC-BT.601
        # - BT.709: https://www.itu.int/rec/R-REC-BT.709
        # - BT.2020: https://www.itu.int/rec/R-REC-BT.2020
        # - BT.2100: https://www.itu.int/rec/R-REC-BT.2100
        self._conversions = {
            ('bt601', 'limited'): Colorspace([0.299, 0.587, 0.114, 1.772, 1.402], (16, 235), (16, 240), 1),
            ('bt601', 'full'): Colorspace([0.299, 0.587, 0.114, 1.772, 1.402], (0, 255), (1, 255), 1),
            ('bt709', 'limited'): Colorspace([0.2126, 0.7152, 0.0722, 1.8556, 1.5748], (16, 235), (16, 240), 1),
            ('bt709', 'full'): Colorspace([0.2126, 0.7152, 0.0722, 1.8556, 1.5748], (0, 255), (1, 255), 1),
            ('bt2020', 'limited'): Colorspace([0.2627, 0.6780, 0.0593, 1.8814, 1.4746], (16, 235), (16, 240), 1),
            ('bt2020', 'full'): Colorspace([0.2627, 0.6780, 0.0593, 1.8814, 1.4746], (0, 255), (1, 255), 1),
            ('bt2100', 'limited'): Colorspace([0.2627, 0.6780, 0.0593, 1.8814, 1.4746], (16, 235), (16, 240), 1),
            ('bt2100', 'full'): Colorspace([0.2627, 0.6780, 0.0593, 1.8814, 1.4746], (0, 255), (1, 255), 1)
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
