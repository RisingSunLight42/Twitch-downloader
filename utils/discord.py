import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import timedelta
from twitchdl.utils import format_time
from twitchdl.entities import Video

class DiscordInteraction:
    def send_webhook(content: str, webhook_urls: list, avatar_url: str = "", embed: DiscordEmbed = None) -> list[DiscordWebhook]:
        webhooks = []
        for webhook_url in webhook_urls:
            webhook = DiscordWebhook(
                url=webhook_url,
                content=content,
                avatar_url=avatar_url
            )
            if embed is not None:
                webhook.add_embed(embed)
            webhook.execute()
            webhooks.append(webhook)
        return webhooks


    def send_webhook_starting_download(content: str, vod_index: int, vod_number: int, avatar_url: str, video_infos: Video, webhook_urls: list):
        embed = DiscordEmbed(title=f"Download in progress (VOD {vod_index+1}/{vod_number})", color="3498db")
        embed.set_author(video_infos["creator"]["displayName"], icon_url=avatar_url)
        embed.add_embed_field(name="Title", value=video_infos["title"], inline=False)
        embed.add_embed_field(name="Game", value=video_infos["game"]["name"], inline=False)
        embed.add_embed_field(name="Date published", value=video_infos["publishedAt"].replace("T"," ").replace("Z", ""))
        embed.add_embed_field(name="Length", value=format_time(video_infos["lengthSeconds"]), inline=False)
        embed.set_footer(text=f"VOD id: {video_infos["id"]}")
        embed.set_timestamp()
        return DiscordInteraction.send_webhook(content, webhook_urls, avatar_url, embed)


    def send_webhook_updating_download(webhook: DiscordWebhook, vod_index: int, vod_number: int, avatar_url: str, video_infos: Video, progress: int):
        embed = DiscordEmbed(title=f"Download in progress (VOD {vod_index+1}/{vod_number})", color="e67e22")
        embed.set_author(video_infos["creator"]["displayName"], icon_url=avatar_url)
        embed.add_embed_field(name="Title", value=video_infos["title"], inline=False)
        embed.add_embed_field(name="Game", value=video_infos["game"]["name"])
        embed.add_embed_field(name="Date published", value=video_infos["publishedAt"].replace("T"," ").replace("Z", ""), inline=False)
        embed.add_embed_field(name="Length", value=format_time(video_infos["lengthSeconds"]))
        embed.add_embed_field(name="Progress", value=f"{progress}%")
        embed.set_footer(text=f"VOD id: {video_infos["id"]}")
        embed.set_timestamp()
        webhook.remove_embeds()
        webhook.add_embed(embed)
        webhook.edit()


    def send_webhook_ending_download(
            webhook: DiscordWebhook,
            vod_index: int,
            vod_number: int,
            avatar_url: str,
            video_infos: Video,
            file_path: str,
            time_elapsed: timedelta,
            has_been_skipped: bool = False,
        ):
        if has_been_skipped:
            webhook.content = f"VOD {video_infos["id"]} has been skipped because **{video_infos["creator"]["displayName"]}** is currently live."
            webhook.remove_embeds()
            webhook.edit()
            return
        embed = DiscordEmbed(title=f"Download successful (VOD {vod_index+1}/{vod_number})", color="57f287")
        embed.set_author(video_infos["creator"]["displayName"], icon_url=avatar_url)
        embed.add_embed_field(name="Title", value=video_infos["title"], inline=False)
        embed.add_embed_field(name="Game", value=video_infos["game"]["name"], inline=False)
        embed.add_embed_field(name="Date published", value=video_infos["publishedAt"].replace("T"," ").replace("Z", ""))
        embed.add_embed_field(name="Length", value=format_time(video_infos["lengthSeconds"]), inline=False)
        embed.add_embed_field(name="File size", value=f"{os.path.getsize(file_path)/(1<<30):,.0f} GB")
        embed.add_embed_field(name="Time elapsed", value=f"{time_elapsed}")
        embed.set_footer(text=f"VOD id: {video_infos["id"]}")
        embed.set_timestamp()
        webhook.remove_embeds()
        webhook.add_embed(embed)
        webhook.edit()
