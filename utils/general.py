import sys
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from re import findall 
from utils.discord import DiscordInteraction
from twitchdl.entities import Video

class StdoutWrapper:
    def __init__(self, webhooks: list[DiscordWebhook], index: int, vod_number: int, avatar_url: str, video_infos: Video):
        self.progress = 0
        self.original = sys.__stdout__
        self.webhooks = webhooks
        self.index = index
        self.vod_number = vod_number
        self.avatar_url = avatar_url
        self.video_infos = video_infos
        self.has_been_skipped = False
    
    def _handle_percent(self, text: str):
        percent = findall(r"\d{1,3}%", text)
        if len(percent) == 0:
            return
        percent = int(percent[0].replace("%", ""))
        if (self.progress == percent):
            return
        self.progress = percent
        for webhook in self.webhooks:
            DiscordInteraction.send_webhook_updating_download(webhook, self.index, self.vod_number, self.avatar_url, self.video_infos, self.progress)
    
    def _handle_skip(self, text: str):
        if self.has_been_skipped:
            return
        self.has_been_skipped = "skipping download" in text

    def write(self, text: str):
        self.original.write(text)
        self._handle_percent(text)
        self._handle_skip(text)

    def flush(self):
        self.original.flush()

    def isatty(self):
        return self.original.isatty()

    @property
    def encoding(self):
        return self.original.encoding
   

class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class EnvManager():
    def __init__(self):
        load_dotenv()
        self.WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
        self.MAX_DOWNLOAD_SPEED = int(os.environ.get("MAX_DOWNLOAD_SPEED"))
        self.DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH")
