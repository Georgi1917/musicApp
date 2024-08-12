import mutagen
from mutagen.mp3 import MP3

def get_song_length_in_seconds(filepath):

    audio = MP3(filepath)

    return str(int(audio.info.length))


def get_song_length(filepath):
    
    audio = MP3(filepath)

    hours = str(int(audio.info.length // 3600))
    minutes = str(int((audio.info.length % 3600) // 60))
    seconds = str(int((audio.info.length % 3600) % 60))

    return f"{hours}:{minutes}:{seconds}"


def remove_unwanted_symbols(sequence):
    forbidden_symbols = ["\'"]
    sequence = list(sequence)

    for i in range(0, len(sequence) - 1):
        if sequence[i] in forbidden_symbols:
            sequence[i] = ""

    return "".join(sequence)
