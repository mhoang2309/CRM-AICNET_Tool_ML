import requests
import http.cookiejar as cookiejar
from .transcripts import TranscriptListFetcher
from .errors import CookiePathInvalid, CookiesInvalid

CookieLoadError = (FileNotFoundError, cookiejar.LoadError)

class YouTubeTranscript(object):
    def __init__(self):
        pass

    def __call__(self):
        pass
    @classmethod
    def list_transcripts(
        cls, 
        video_id, 
        proxies=None, 
        cookies=None,
        json3=False
    ):
        with requests.Session() as http_client:
            if cookies:
                http_client.cookies = cls._load_cookies(cookies, video_id)
            http_client.proxies = proxies if proxies else {}
            return TranscriptListFetcher(http_client).fetch(video_id, json3)
                
    @classmethod
    def get_transcript(
        cls, 
        video_id, 
        languages: tuple = ("vi",),
        proxies=None, 
        cookies=None, 
        preserve_formatting=False,
        json3=False
    ):
        assert isinstance(video_id, str)
        
        return cls.list_transcripts(video_id, proxies, cookies, json3).find_transcript(languages).fetch(preserve_formatting=preserve_formatting, json3=json3)
        
    @classmethod
    def _load_cookies(
        cls, 
        cookies, 
        video_id
    ):
        try:
            cookie_jar = cookiejar.MozillaCookieJar()
            cookie_jar.load(cookies)
            if not cookie_jar:
                raise CookiesInvalid(video_id)
            return cookie_jar
        except CookieLoadError:
            raise CookiePathInvalid(video_id)

