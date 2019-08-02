import logging
import subprocess


def merge_audio_and_video(audio_file_location, video_file_location, output_file_name):
    logger = logging.getLogger(__name__)
    logger.debug(f"merging audio: {audio_file_location} video: {video_file_location} to {output_file_name}")
    try:
        subprocess.call(
            ["ffmpeg",
             "-i", audio_file_location, "-i", video_file_location,
             "-c:v", "copy", "-c:a", "copy",
             output_file_name])
    except OSError as e:
        logger.exception(e.strerror)
    logger.debug(f"merged audio: {audio_file_location} video: {video_file_location} to {output_file_name}")


def save_audio(audio_file_location, output_file_name):
    logger = logging.getLogger(__name__)
    logger.debug(f"saving audio: {audio_file_location} to {output_file_name}")
    try:
        subprocess.call(
            ["ffmpeg",
             "-i", audio_file_location,
             "-vn",
             "-ar", "48000",
             "-ac", "2",
             "-b:a", "320k",
             output_file_name])
    except OSError as e:
        logger.exception(e.strerror)
    logger.debug(f"saved audio: {audio_file_location} to {output_file_name}")
