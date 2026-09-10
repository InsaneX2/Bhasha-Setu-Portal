"""
Audio Conversion & Transcription Utility
Converts uploaded audio/video clips (MP3, MP4, M4A, WAV, FLAC, OGG, AAC, WebM) to 16kHz mono PCM WAV
and transcribes with chunking support for longer recordings.
"""

import io
import os
import tempfile
import subprocess
import speech_recognition as sr

def get_ffmpeg_binary() -> str:
    """Find a working ffmpeg binary from imageio_ffmpeg, PATH, or known Windows locations."""
    # 1. Try imageio_ffmpeg package
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except Exception:
        pass

    # 2. Try system PATH
    from shutil import which
    exe = which("ffmpeg")
    if exe and os.path.exists(exe):
        return exe

    # 3. Known fallback directories on Windows
    fallback_candidates = [
        r"C:\Users\INSANE\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
        r"C:\Users\INSANE\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
    ]
    for candidate in fallback_candidates:
        if os.path.exists(candidate):
            return candidate

    return ""


def convert_audio_to_pcm_wav(audio_bytes: bytes, file_name_hint: str = "clip.mp3") -> io.BytesIO:
    """
    Takes raw audio/video bytes (MP3, MP4, M4A, WAV, WebM, etc.) and converts them to 16kHz mono PCM WAV.
    Returns an in-memory io.BytesIO object suitable for speech_recognition.AudioFile.
    """
    if not audio_bytes:
        raise ValueError("Uploaded audio file is empty.")

    # Determine extension
    ext = os.path.splitext(file_name_hint)[1].lower() if file_name_hint else ".mp3"
    if not ext:
        ext = ".mp3"

    ffmpeg_bin = get_ffmpeg_binary()

    if not ffmpeg_bin:
        # If the input is already a WAV file, we can try to pass it directly
        if ext == ".wav":
            return io.BytesIO(audio_bytes)
        raise RuntimeError(
            "Audio conversion failed: FFmpeg binary not found. "
            "Please ensure imageio-ffmpeg is installed so MP3, MP4, and M4A files can be decoded."
        )

    # Write to a secure temporary input file
    temp_dir = tempfile.gettempdir()
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False, dir=temp_dir) as in_file:
        in_path = in_file.name
        in_file.write(audio_bytes)
        in_file.flush()

    out_path = in_path + "_converted.wav"
    try:
        # Run ffmpeg conversion:
        # -vn: disable video recording (crucial for MP4 videos and MP3 files with embedded album artwork)
        # -acodec pcm_s16le: 16-bit PCM
        # -ar 16000: 16kHz sample rate (ideal for SpeechRecognition / Google STT)
        # -ac 1: mono audio channel
        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", in_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            out_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            err_msg = res.stderr.decode("utf-8", errors="ignore")
            raise RuntimeError(f"FFmpeg decoding failed: {err_msg[:300]}")

        with open(out_path, "rb") as f:
            wav_bytes = f.read()

        return io.BytesIO(wav_bytes)

    finally:
        if os.path.exists(in_path):
            try:
                os.remove(in_path)
            except Exception:
                pass
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except Exception:
                pass


def transcribe_audio_file(
    audio_bytes: bytes,
    file_name: str,
    language_code: str = "en-IN",
    progress_callback=None
) -> str:
    """
    Converts audio/video to WAV, chunks it if longer than 30s, and transcribes using SpeechRecognition.
    Returns the concatenated transcribed text.
    """
    wav_io = convert_audio_to_pcm_wav(audio_bytes, file_name_hint=file_name)
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_io) as source:
        duration = getattr(source, "DURATION", 0.0)

        # If audio is short (<= 40 seconds), transcribe directly
        if duration <= 40.0:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language=language_code)
            except sr.UnknownValueError:
                return ""

        # For longer audio, transcribe in 30-second segments
        chunk_duration = 30.0
        chunks_count = int(duration // chunk_duration) + (1 if duration % chunk_duration > 0 else 0)
        # Limit chunks to up to 12 chunks (up to 6 minutes of audio)
        max_chunks = min(chunks_count, 12)

        transcribed_parts = []
        for i in range(max_chunks):
            if progress_callback:
                progress_callback(i + 1, max_chunks)

            chunk_data = recognizer.record(source, duration=chunk_duration)
            if not chunk_data.frame_data:
                break

            try:
                text = recognizer.recognize_google(chunk_data, language=language_code)
                if text and text.strip():
                    transcribed_parts.append(text.strip())
            except (sr.UnknownValueError, sr.RequestError):
                # Silence, background music, or unrecognizable speech segment - continue
                continue

        return " ".join(transcribed_parts)
