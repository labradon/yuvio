import numpy as np
from .. import pixel_formats
from . import Reader, Writer
from . import YUVFrame
from . import colorspaces


def imread(file, width, height, pixel_format, index=0):
    """
    Read the yuv frame from the given file.

    :param file: str, Path, file handle
    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :param index: frame index (default: 0)
    :return: yuv frame
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    reader = Reader(file, yuv_format)
    return reader.read(index, 1)[0]


def mimread(file, width, height, pixel_format, index=0, count=None):
    """
    Read the yuv frames from the given file.

    :param file: str, Path, file handle
    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :param index: first frame index (default: 0)
    :param count: frame count (read all if None)
    :return: list of yuv frames
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    reader = Reader(file, yuv_format)
    return reader.read(index, count)


def imwrite(file, yuv_frame):
    """
    Write the yuv frame to the given file.

    :param file: str, Path, file handle
    :param yuv_frame: list of yuv frames
    """
    yuv_format = pixel_formats[yuv_frame.pixel_format](yuv_frame.y.shape[1], yuv_frame.y.shape[0])
    writer = Writer(file, yuv_format)
    writer.write(yuv_frame)


def mimwrite(file, yuv_frames):
    """
    Write the yuv frames to the given file.

    :param file: str, Path, file handle
    :param yuv_frames: list of yuv frames
    """
    yuv_format = pixel_formats[yuv_frames[0].pixel_format](yuv_frames[0].y.shape[1], yuv_frames[0].y.shape[0])
    writer = Writer(file, yuv_format)
    writer.write(yuv_frames)


def get_reader(file, width, height, pixel_format):
    """
    Get a reader for the given file.

    :param file: str, Path, file handle
    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :return: reader
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    reader = Reader(file, yuv_format)
    return reader


def get_writer(file, width, height, pixel_format):
    """
    Get a writer for the given file.

    :param file: str, Path, file handle
    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :return: writer
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    writer = Writer(file, yuv_format)
    return writer


def frame(yuv, pixel_format):
    """
    Initialize a new yuv frame from the given y, u, v components.

    :param yuv: yuv components tuple
    :param pixel_format: ffmpeg pixel format specifier
    :return: yuv frame
    """
    y, u, v = yuv
    yuv_format = pixel_formats[pixel_format](y.shape[1], y.shape[0])
    sub_w, sub_h = yuv_format.chroma_subsampling()
    if sub_w == 0 and sub_h == 0:
        if u is not None or v is not None:
            raise RuntimeError("Chroma components must be 'None' for pixel format '{}'".format(pixel_format))
        expected_chroma_shape = (0, 0)
        u = np.empty(expected_chroma_shape, dtype=np.void)
        v = np.empty(expected_chroma_shape, dtype=np.void)
    else:
        expected_chroma_shape = (y.shape[0] / sub_h, y.shape[1] / sub_w)
    if u.shape != expected_chroma_shape or v.shape != expected_chroma_shape:
        raise RuntimeError("Invalid chroma shape for pixel format '{}'".format(pixel_format))
    yuv_frame = YUVFrame(y, u, v, yuv_format)
    return yuv_frame


def empty(width, height, pixel_format):
    """
    Initialize a new yuv frame where all components are empty.

    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :return: yuv frame
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    y, u, v = yuv_format.unpack(np.empty(1, dtype=yuv_format.dtype))
    return YUVFrame(y[0],
                    u[0] if u is not None else None,
                    v[0] if v is not None else None,
                    yuv_format)


def zeros(width, height, pixel_format):
    """
    Initialize a new yuv frame where all components are set to 0.

    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :return: yuv frame
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    y, u, v = yuv_format.unpack(np.zeros(1, dtype=yuv_format.dtype))
    return YUVFrame(y[0],
                    u[0] if u is not None else None,
                    v[0] if v is not None else None,
                    yuv_format)


def ones(width, height, pixel_format):
    """
    Initialize a new yuv frame where all components are set to 1.

    :param width: frame width
    :param height: frame height
    :param pixel_format: ffmpeg pixel format specifier
    :return: yuv frame
    """
    yuv_format = pixel_formats[pixel_format](width, height)
    y, u, v = yuv_format.unpack(np.ones(1, dtype=yuv_format.dtype))
    return YUVFrame(y[0],
                    u[0] if u is not None else None,
                    v[0] if v is not None else None,
                    yuv_format)


def to_rgb(yuv, specification='bt709', value_range='limited'):
    """
    Convert yuv data to rgb.

    :param yuv: yuv frame
    :param specification: specification identifier (default: 'bt709')
    :param value_range: yuv value range (default: 'limited')
    :return: rgb data
    """
    return colorspaces[specification, value_range].to_rgb(*yuv.split(), yuv.yuv_format)


def from_rgb(rgb, pixel_format, specification='bt709', value_range='limited'):
    """
    Initialize a new yuv frame from rgb data.

    :param rgb: rgb data
    :param pixel_format: ffmpeg pixel format specifier
    :param specification: specification identifier (default: 'bt709')
    :param value_range: yuv value range (default: 'limited')
    :return: yuv frame
    """
    yuv_format = pixel_formats[pixel_format](rgb.shape[1], rgb.shape[0])
    y, u, v = colorspaces[specification, value_range].from_rgb(rgb, yuv_format)
    return YUVFrame(y, u, v, yuv_format)
