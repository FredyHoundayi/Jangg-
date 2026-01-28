from gtts import gTTS
import uuid
import os

AUDIO_FOLDER = "app/static/audio"


def text_to_audio(text: str):

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    tts = gTTS(text=text, lang="en")
    tts.save(filepath)

    return f"/static/audio/{filename}"
