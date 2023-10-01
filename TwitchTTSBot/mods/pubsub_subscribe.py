from twitchbot import Mod
from twitchbot import PubSubTopics,get_pubsub,PubSubData,PubSubPointRedemption,PubSubModerationAction
import json
from typing import Tuple
from bot import TwitchTTSBot

class PubSubSubscriberMod(Mod):
    def __init__(self):
        self._last_request = None

    async def on_connected(self):
        access_token = PubSubSubscriberMod.__GetAccessToken()
        await get_pubsub().listen_to_channel(access_token[0], [ PubSubTopics.channel_points,PubSubTopics.community_channel_points ], access_token=access_token[1])

        self._redeem_name = PubSubSubscriberMod._GetRedeemName()

    @staticmethod
    def __GetAccessToken() -> Tuple[str,str]:
        config = None
        with open('configs/config.json') as f:
            config = json.load(f)

        return (config['channels'][0], config['pubsub'])

    @staticmethod
    def _GetRedeemName() -> str:
        config = None
        with open('configs/config.json') as f:
            config = json.load(f)

        return config['redeem']

    #async def on_pubsub_received(self, raw: PubSubData):
    #    print("+>> " + str(raw.raw_data))
    
    async def on_pubsub_custom_channel_point_reward(self, _: PubSubData, data: PubSubPointRedemption):
        print(f"[v] Point redeem call: {data.reward_title}, '{data.user_input}' (by {data.user_login_name})")

        if data.reward_title == self._redeem_name:
            if self._last_request is not None and self._last_request.user_login_name == data.user_login_name and self._last_request.user_input == data.user_input:
                return

            self._last_request = data
            await TwitchTTSBot.instance()._on_channel_points_redeemed(data.user_login_name, data.user_input)