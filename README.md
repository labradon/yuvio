<div align="center">
    <img align="center" src="logo.png" width="520" alt=“YUVIO” />
</div>

Welcome to **yuvio**, a python package for reading and writing uncompressed yuv
image and video data. **yuvio** supports many pixel formats specified by ffmpeg.
And if it doesn't, it's fast and easy to add support for your own pixel formats.

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
v = np.zeros((560, 540), dtype=np.uint8)
frame_420 = yuvio.frame((y, u, v), "yuv420p")

frame_400 = yuvio.frame((y, None, None), "gray")
```

## Formats

Print a complete list of available pixel formats using `print(yuvio.pixel_formats)`.
To get detailed information on the IO format of a specific `pix_fmt` use
`print(yuvio.pixel_formats[pix_fmt].io_info())`.

Currently, the following pixel formats (`pix_fmt`) are available:
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
* `'yuyv422'`
* `'uyvy422'`
* `'yvyu422'`
