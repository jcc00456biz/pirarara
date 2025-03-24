#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import subprocess

import ffmpeg

logger = logging.getLogger(__name__)


def is_ffmpeg_installed():
    """
    "ffmpeg"がインストールされているかどうかを確認する関数。

    Returns:
        bool: "ffmpeg"がインストールされている場合はTrue、それ以外はFalse。
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode == 0:
            return True
        return False
    except FileNotFoundError:
        return False


def get_media_type(file_path: str) -> str:
    """
    メディアファイルの種類を取得する。

    指定されたファイルの拡張子に基づいて、そのメディアタイプを判別します。
    動画、音楽、文章などのカテゴリに分類されます。

    Args:
        file_path (str): 判別対象のファイルのパス。

    Returns:
        str: メディアタイプを示す文字列。該当するタイプがない場合は空文字を返します。

    Note:
        対応する拡張子とメディアタイプの対応表は、`media_type_dict` に定義されています。
        未対応の拡張子については、空文字が返されます。

    Examples:
        >>> get_media_type("example.mp4")
        'movie'
        >>> get_media_type("example.pdf")
        'doc'
        >>> get_media_type("unknown.xyz")
        ''
    """
    media_type_dict = {
        # 動画
        ".mp4": "movie",
        ".avi": "movie",
        ".mov": "movie",
        ".wmv": "movie",
        ".flv": "movie",
        ".webm": "movie",
        ".mpg": "movie",
        ".mkv": "movie",
        ".asf": "movie",
        ".vob": "movie",
        ".ts": "movie",
        ".m2ts": "movie",
        # 音楽
        ".wave": "music",
        ".alf": "music",
        ".mp3": "music",
        ".aac": "music",
        ".m4a": "music",
        # 文章
        ".epub": "doc",
        ".pdf": "doc",
        ".azw": "doc",
    }

    # ファイル拡張子を小文字で取得
    file_ext = os.path.splitext(file_path)[1].lower()
    return media_type_dict.get(file_ext, "")


def get_media_info(file_path: str, file_hash_data: str) -> dict:
    """
    メディアファイルの情報を取得する関数。

    Args:
        file_path (str): メディアファイルのパス。
        file_hash_data (str): ファイルのハッシュデータ。

    Returns:
        dict: メディアファイルの情報を格納した辞書。
    """
    info = {
        "title": os.path.basename(file_path),
        "media_type": get_media_type(file_path),
        "video_codec_name": "",
        "video_width": "",
        "video_height": "",
        "audio_codec_name": "",
        "audio_sample_rate": "",
        "duration": "",
        "file_name": os.path.basename(file_path),
        "file_hash_algorithm": "sha256",
        "file_hash_data": file_hash_data,
    }

    if info["media_type"] != "movie":
        return info

    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next(
            (
                stream
                for stream in probe["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        audio_stream = next(
            (
                stream
                for stream in probe["streams"]
                if stream["codec_type"] == "audio"
            ),
            None,
        )

        if video_stream:
            duration = float(probe["format"]["duration"])
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            str_duration = (
                f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            )
            info.update(
                {
                    "video_codec_name": video_stream["codec_name"],
                    "video_width": str(video_stream["width"]),
                    "video_height": str(video_stream["height"]),
                    "duration": str_duration,
                }
            )

        if audio_stream:
            duration = float(probe["format"]["duration"])
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            str_duration = (
                f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            )
            info.update(
                {
                    "audio_codec_name": audio_stream["codec_name"],
                    "audio_sample_rate": audio_stream["sample_rate"],
                    "duration": str_duration,
                }
            )
    except ffmpeg.Error:
        pass

    return info


def capture_frame(file_path, output_image_path, time="00:00:01") -> bool:
    """
    動画ファイルの特定時刻のフレームをキャプチャして画像として保存する。

    指定された動画ファイルから、指定時刻のフレームをキャプチャして
    画像ファイルとして保存します。

    Args:
        file_path (str): 動画ファイルのパス。
        output_image_path (str): 保存先の画像ファイルのパス。
        time (str, optional): キャプチャするフレームの時刻（デフォルトは "00:00:01"）。

    Returns:
        bool: キャプチャが成功した場合はTrue、エラーが発生した場合はFalse。

    Raises:
        ffmpeg.Error: ffmpegによるエラーが発生した場合。

    Examples:
        >>> capture_frame("example.mp4", "output.jpg")
        True
        >>> capture_frame("invalid.mp4", "output.jpg")
        False

    Note:
        この関数は、`ffmpeg` パッケージがインストールされている必要があります。
        キャプチャが失敗した場合、エラーログが記録されます。
    """
    try:
        (
            ffmpeg
            .input(file_path, ss=time)
            .output(output_image_path, vframes=1)
            .run(overwrite_output=True)
        )
        return True
    except ffmpeg.Error as e:
        logger.error(f"Error capturing frame: {e}")
        return False
