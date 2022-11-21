from pathlib import Path
from gridfs import GridFS
from pika.adapters.blocking_connection import BlockingChannel
from models.message import Message
from bson.objectid import ObjectId
import moviepy.editor as mp
import tempfile
import pika
import logging


def get_audio_clip(video_fid, videos_fs) -> mp.AudioClip:
    video_tf = tempfile.NamedTemporaryFile()
    # download video
    video_tf.write(
        videos_fs.get(
            ObjectId(video_fid),
        ).read(),
    )
    audio = mp.VideoFileClip(filename=video_tf.name).audio
    video_tf.close()

    return audio


def save_audio_to_temp_file(video_fid, audio_clip: mp.AudioClip) -> Path:
    mp3_tf_path = Path(tempfile.gettempdir()) / f"{video_fid}.mp3"
    audio_clip.write_audiofile(mp3_tf_path)
    audio_clip.close()

    return mp3_tf_path


def save_audio_to_fs(audio_temp_path: Path, video_fid: str, mp3_fs: GridFS) -> str:
    audio_bytes = audio_temp_path.read_bytes()
    mp3_fid = mp3_fs.put(
        data=audio_bytes,
    )
    audio_temp_path.unlink()
    return str(mp3_fid)


def publish_message(message: Message, pika_channel: BlockingChannel, mp3_queue: str):
    pika_channel.basic_publish(
        exchange="",
        routing_key=mp3_queue,
        body=message.to_json(),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent.value,
        ),
    )


def convert_to_mp3(message: Message, videos_fs: GridFS, mp3_fs: GridFS, pika_channel: BlockingChannel, mp3_queue: str):
    try:
        audio_clip = get_audio_clip(message.video_fid, videos_fs)
        audio_temp_path = save_audio_to_temp_file(message.video_fid, audio_clip)
        mp3_fid = save_audio_to_fs(audio_temp_path, message.video_fid, mp3_fs)
        message.mp3_fid = mp3_fid

        exc = publish_message(message, pika_channel, mp3_queue)
        return exc
    except Exception as e:
        logging.exception(e)
        return e
