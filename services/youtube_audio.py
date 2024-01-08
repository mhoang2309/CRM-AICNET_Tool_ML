import json

from .youtube_download import YouTubeAudio
from .youtube.youtube_transcript import YouTubeTranscript

def load_audio_transcript(id_video:str):
    path_data = "data/pretreatment"

    yt = YouTubeAudio(id_video)
    path_audio = yt(name=id_video, destination=f"{path_data}/audio")
    data_transcript = YouTubeTranscript.get_transcript(id_video, languages=['vi'], json3=True)
    with open(f'{path_data}/transcript/{id_video}.json', 'w', encoding='utf-8') as f:
        json.dump(data_transcript, f, ensure_ascii=False, indent=4)