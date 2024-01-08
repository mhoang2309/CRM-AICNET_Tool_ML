import os
from typing import Any, Callable, Dict, Optional

import pydub
from pytube import YouTube
from moviepy.editor import *


class Audio:
    def __init__(self, path:str) -> None:
        self.base, self.ext = os.path.splitext(path) 
        self.sound:pydub.AudioSegment = pydub.AudioSegment.from_file(path, format=self.ext.split(".")[-1])
    
    def convert(self, format="mp3"):
        self.sound.export(f"{self.base}.mp3", format=format)
    
    @classmethod
    def MP4ToMP3(cls, path_mp4, path_mp3):
        FILETOCONVERT = AudioFileClip(path_mp4)
        FILETOCONVERT.write_audiofile(path_mp3)
        FILETOCONVERT.close()

    

class YouTubeAudio(YouTube, Audio):
    def __init__(self, 
                url: str, 
                on_progress_callback: Callable[[Any, bytes, int], None] | None = None, 
                on_complete_callback: Callable[[Any, str | None], None] | None = None, 
                proxies: Dict[str, str] = None, 
                use_oauth: bool = False, 
                allow_oauth_cache: bool = True,):
        url = f"v={url}"
        super().__init__(url, on_progress_callback, on_complete_callback, proxies, use_oauth, allow_oauth_cache)
    
    def __call__(self, name:str, destination:str="data", only_audio:bool=False) -> str:
        try:
            self.video = self.streams.filter(only_audio=only_audio).first() 
            out_file = self.video.download(output_path=destination) 
            new_file = destination + "/" + name + '.mp3'
            self.MP4ToMP3(out_file, new_file)
            os.remove(out_file)
            # os.rename(out_file, new_file) 
            return new_file
        except:
            raise "Download audio false"
    
    