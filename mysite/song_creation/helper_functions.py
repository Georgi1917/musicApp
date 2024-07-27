from pydub import AudioSegment

def get_duration_of_song(song_filepath):
    song = AudioSegment.from_file('D:\Music\rock\KISS - I was made for lovin you.mp3')

    return len(song)