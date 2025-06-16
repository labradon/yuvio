[![License](https://img.shields.io/github/license/labradon/yuvio)](https://opensource.org/licenses/MIT)
![GitHub top language](https://img.shields.io/github/languages/top/labradon/yuvio)
[![GitHub stars](https://img.shields.io/github/stars/labradon/yuvio)](https://github.com/labradon/yuvio/stargazers)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yuvio)
![PyPI](https://img.shields.io/pypi/v/yuvio)

<div align="center">
    <img align="center" src="https://github.com/labradon/yuvio/blob/main/logo.png?raw=true" width="520" alt=“YUVIO” />
</div>

Welcome to **yuvio**, a python package for reading and writing uncompressed yuv
image and video data. **yuvio** supports all common yuv pixel formats specified by ffmpeg and [more](#formats).
Its modular design allows fast and easy extension to add support for your own pixel formats.
If you believe an important pixel format is missing, feel free to open an issue.

**NEW**: Added support for colorspace conversion (YCbCr to/from RGB). For usage, see [below](#colorspace-conversion). Supported specifications are
* `'bt601'`: [Rec. ITU-R BT.601](https://www.itu.int/rec/R-REC-BT.601)
* `'bt709'`: [Rec. ITU-R BT.709](https://www.itu.int/rec/R-REC-BT.709)
* `'bt2020'`: [Rec. ITU-R BT.2020](https://www.itu.int/rec/R-REC-BT.2020)
* `'bt2100'`: [Rec. ITU-R BT.2100](https://www.itu.int/rec/R-REC-BT.2100)

## Install

`yuvio` is easily installed using python's `pip` package manager.

```sh
pip install yuvio
```

## Usage
To read and write yuv files, `yuvio` provides the functions `imread`, `imwrite`, `mimread` and
`mimwrite` for single and multiple frames, respectively. Both require the specification of a
pixel format to use for the yuv data.

```python
import yuvio

yuv_frame = yuvio.imread("example_yuv420p.yuv", 1920, 1080, "yuv420p")
yuvio.imwrite("example_yuv420p_copy.yuv", yuv_frame)

yuv_frames = yuvio.mimread("example_yuv420p.yuv", 1920, 1080, "yuv420p")
yuvio.mimwrite("example_yuv420p_copy.yuv", yuv_frames)
```

Thereby, `yuvio` is not restricted to file objects and can read and write from/to other `io` 
streams as well. For example, this allows to conveniently unpack the individual yuv planes from 
interleaved yuv data available in memory.

```python
import io
import yuvio

data = ...  # e.g. np.ndarray
buffer = io.BytesIO(data)
yuv_frame = yuvio.imread(buffer, 1920, 1080, "v210")
y = yuv_frame.y
u = yuv_frame.u
v = yuv_frame.v
```

For advanced use cases, `yuvio` also provides direct access to the `Reader` and `Writer` objects.
This allows sequential reading and writing from/to yuv files and may be beneficial for iterating
over large files without keeping all frames in memory.

```python
import yuvio

reader = yuvio.get_reader("example_yuv420p.yuv", 1920, 1080, "yuv420p")
writer = yuvio.get_writer("example_yuv420p_copy.yuv", 1920, 1080, "yuv420p")

for yuv_frame in reader:
    writer.write(yuv_frame)
```

To create custom yuv data, `yuvio` provides access to convenient yuv frame
initializers `empty`, `zeros` and `ones` similar to numpys convenience array
initializers.

```python
import yuvio

empty = yuvio.empty(1920, 1080, "yuv420p")
zeros = yuvio.zeros(1920, 1080, "yuv420p")
ones = yuvio.ones(1920, 1080, "yuv420p")
```

For advanced use cases, `yuvio` also allows direct yuv frame initialization
from custom data using the `frame` initializer.
```python
import yuvio
import numpy as np

y = 255 * np.ones((1920, 1080), dtype=np.uint8)
u = np.zeros((960, 540), dtype=np.uint8)
v = np.zeros((960, 540), dtype=np.uint8)
frame_420 = yuvio.frame((y, u, v), "yuv420p")

frame_400 = yuvio.frame((y, None, None), "gray")
```

### Colorspace conversion

Colorspace conversion from RGB to YCbCr colorspace and from YCbCr to RGB colorspace is possible using the `from_rgb(rgb, pixel_format, specification, value_range)` and `to_rgb(yuv, specification, value_range)` functions.
```python
import yuvio

yuv_frame = ...
rgb = yuvio.to_rgb(yuv_frame, specification='bt709', value_range='limited')
yuv_frame = yuvio.from_rgb(rgb, 'yuv444p', specification='bt709', value_range='limited')
```

> [!IMPORTANT]  
> Color conversion is only supported for '444' chroma subsampling, i.e., no chroma subsampling. Support for chroma subsampling is planned for a future release.

## Formats

Print a complete list of available pixel formats using `print(yuvio.pixel_formats)`.
To get detailed information on the IO format of a specific `pix_fmt` use
`print(yuvio.pixel_formats[pix_fmt].io_info())`.

Currently, the following pixel formats (`pix_fmt`) are available:

**Grayscale/YUV 4:0:0**
* `'gray'`
* `'gray10le'`
* `'gray10be'`
* `'gray16le'`
* `'gray16be'`
* `'gray9le'`
* `'gray9be'`
* `'gray12le'`
* `'gray12be'`
* `'gray14le'`
* `'gray14be'`

**Planar YUV 4:2:0**
* `'yuv420p'`
* `'yuv420p10le'`
* `'yuv420p10be'`
* `'yuv420p16le'`
* `'yuv420p16be'`
* `'yuv420p9le'`
* `'yuv420p9be'`
* `'yuv420p12le'`
* `'yuv420p12be'`
* `'yuv420p14le'`
* `'yuv420p14be'`

**Semi-planar YUV 4:2:0**
* `'nv12'`

**Planar YUV 4:2:2**
* `'yuv422p'`
* `'yuv422p10le'`
* `'yuv422p10be'`
* `'yuv422p16le'`
* `'yuv422p16be'`
* `'yuv422p9le'`
* `'yuv422p9be'`
* `'yuv422p12le'`
* `'yuv422p12be'`
* `'yuv422p14le'`
* `'yuv422p14be'`

**Planar YUV 4:4:4**
* `'yuv444p'`
* `'yuv444p10le'`
* `'yuv444p10be'`
* `'yuv444p16le'`
* `'yuv444p16be'`
* `'yuv444p9le'`
* `'yuv444p9be'`
* `'yuv444p12le'`
* `'yuv444p12be'`
* `'yuv444p14le'`
* `'yuv444p14be'`

**Interleaved YUV 4:2:0**
(*Even lines carry luma and chroma [y0 u0 y1 v0 ...], odd lines carry only luma [y0 y1 ...]*)
* `'yuv420i'`
* `'yuv420i10le'`
* `'yuv420i10be'`
* `'yuv420i16le'`
* `'yuv420i16be'`
* `'yuv420i9le'`
* `'yuv420i9be'`
* `'yuv420i12le'`
* `'yuv420i12be'`
* `'yuv420i14le'`
* `'yuv420i14be'`

**Interleaved YUV 4:2:2**
* `'yuv422i'`
* `'yuv422i10le'`
* `'yuv422i10be'`
* `'yuv422i16le'`
* `'yuv422i16be'`
* `'yuv422i9le'`
* `'yuv422i9be'`
* `'yuv422i12le'`
* `'yuv422i12be'`
* `'yuv422i14le'`
* `'yuv422i14be'`
* `'yuyv422'`: Same as `'yuv422i'`
* `'uyvy422'`
* `'yvyu422'`

**Interleaved YUV 4:4:4**
* `'yuv444i'`
* `'yuv444i10le'`
* `'yuv444i10be'`
* `'yuv444i16le'`
* `'yuv444i16be'`
* `'yuv444i9le'`
* `'yuv444i9be'`
* `'yuv444i12le'`
* `'yuv444i12be'`
* `'yuv444i14le'`
* `'yuv444i14be'`

**Special formats**
* `'v210'`
