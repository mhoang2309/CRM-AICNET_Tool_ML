import json
import requests
from html import unescape
import http.cookiejar as cookiejar

CHANNEL_URL = "https://www.youtube.com/@{channel_id}/videos"
YOUTUBE_BROWSE_URL = "https://www.youtube.com/youtubei/v1/browse?key={api_key}"

CookieLoadError = (FileNotFoundError, cookiejar.LoadError)


class CouldNotRetrieveTranscript(Exception):
    """
    Raised if a transcript could not be retrieved.
    """
    ERROR_MESSAGE = '\nCould not retrieve a transcript for the video {video_url}!'
    CAUSE_MESSAGE_INTRO = ' This is most likely caused by:\n\n{cause}'
    CAUSE_MESSAGE = ''

    def __init__(self, channel_id):
        self.channel_id = channel_id
        super(CouldNotRetrieveTranscript, self).__init__(self._build_error_message())

    def _build_error_message(self):
        cause = self.cause
        error_message = self.ERROR_MESSAGE.format(video_url=CHANNEL_URL.format(channel_id=self.channel_id))

        if cause:
            error_message += self.CAUSE_MESSAGE_INTRO.format(cause=cause)
        return error_message

    @property
    def cause(self):
        return self.CAUSE_MESSAGE


class YouTubeRequestFailed(CouldNotRetrieveTranscript):
    CAUSE_MESSAGE = 'Request to YouTube failed: {reason}'

    def __init__(self, channel_id, http_error):
        self.reason = str(http_error)
        super(YouTubeRequestFailed, self).__init__(channel_id)

    @property
    def cause(self):
        return self.CAUSE_MESSAGE.format(
            reason=self.reason,
        )


class ChannelList(object):
    def __init__(self, http_client: requests.Session):
        self._http_client = http_client
        
    def fetch(self, channel_id:str):
        return self._extract_channel_id(self._fetch_html(channel_id))
    
    def _fetch_html(self, channel_id:str):
        response = self._http_client.get(CHANNEL_URL.format(channel_id=channel_id), headers={'Accept-Language': 'en-US'})
        return unescape(self._raise_http_errors(response, channel_id).text)
    
    def _extract_channel_id(self, html:str):
        splitted_html = html.split('ytInitialData = ')
        ytcfg = json.loads(splitted_html[0].split("(function() {window.ytplayer={};\nytcfg.set(")[-1].split("); window.ytcfg.obfuscatedData_")[0])
        responseContext = json.loads(splitted_html[1].split(';</script>')[0].replace('\n', '')).get("contents", {})
        responseTabs = responseContext.get("twoColumnBrowseResultsRenderer").get("tabs")
        for tab in responseTabs:
            tabRenderer = tab.get("tabRenderer", {})
            if tabRenderer.get("title") == "Videos":
                contents = tabRenderer.get("content", {}).get("richGridRenderer", {}).get("contents", {})
                break
        video_ids = []
        def youtube_browse(clickTrackingParams, token):
            payload = json.dumps({
                "context":{
                    "client": {
                        "hl": ytcfg.get("INNERTUBE_CONTEXT").get("client").get("hl"),
                        "gl": ytcfg.get("INNERTUBE_CONTEXT").get("client").get("gl"),
                        "clientName": ytcfg.get("INNERTUBE_CONTEXT").get("client").get("clientName"),
                        "clientVersion": ytcfg.get("INNERTUBE_CONTEXT").get("client").get("clientVersion"),
                    },
                    "clickTracking": {
                        "clickTrackingParams": clickTrackingParams
                    }
                },
                "continuation": token
            })
            return json.loads(self._http_client.post(YOUTUBE_BROWSE_URL.format(api_key=ytcfg.get("INNERTUBE_API_KEY")), data=payload, headers={'content-type': 'application/json'}).text)
        
        def get_video_ids(contents):
            if contents:
                clickTrackingParams = {}
                token = {}
                for content in contents:
                    video_id = content.get("richItemRenderer", {}).get("content", {}).get("videoRenderer", {}).get("videoId", {})
                    if video_id:
                        video_ids.append(video_id)
                        continue
                    continuationEndpoint = content.get("continuationItemRenderer", {}).get("continuationEndpoint", {})
                    clickTrackingParams = continuationEndpoint.get("clickTrackingParams", {})
                    token = continuationEndpoint.get("continuationCommand", {}).get("token", {})
                    break
                if clickTrackingParams and token:
                    get_video_ids(youtube_browse(clickTrackingParams, token).get("onResponseReceivedActions", {})[0].get("appendContinuationItemsAction", {}).get("continuationItems", {}))
            return None
        
            
        get_video_ids(contents)
        
        return video_ids
      
    @staticmethod
    def _raise_http_errors(response: requests.Response, channel_id:str):
        try:
            response.raise_for_status()
            return response
        except requests.HTTPError as error:
            raise YouTubeRequestFailed(channel_id, error)
        

class YouTubeCrawl(object):
    
    def __init__(self):
        pass
    
    def __call__(self):
        pass
    
    @classmethod
    def list_channel_id(
        cls,
        channel_id:str,
        proxies=None, 
        cookies=None,
    ):
        with requests.Session() as http_client:
            if cookies:
                http_client.cookies = cls._load_cookies(cookies, channel_id)
            http_client.proxies = proxies if proxies else {}
            return ChannelList(http_client).fetch(channel_id)
    
    @classmethod
    def get_html(
        cls,
        channel_id:str,
        proxies=None, 
        cookies=None,
    ):
        assert isinstance(channel_id, str)
        return cls.list_channel_id(channel_id)
    
    @classmethod
    def _load_cookies(
        cls, 
        cookies, 
        channel_id
    ):
        try:
            cookie_jar = cookiejar.MozillaCookieJar()
            cookie_jar.load(cookies)
            if not cookie_jar:
                raise f'The cookies provided are not valid (may have expired) {channel_id}'
            return cookie_jar
        except CookieLoadError:
            raise f'The provided cookie file was unable to be loaded {channel_id}'