import aiohttp
import asyncio
import os
from source import scrape_comments

class Activity_Crawler:
    def __init__(self) -> None:
        self.scraper = scrape_comments.Database_Collector()


    async def get_recent_post(self, token, xuid, my_xuid):
        headers = {
            'Authorization': token,
            'X-XBL-Contract-Version': '12',
            'Accept-Language': 'en-US',
            'Accept': 'application/json'
        }

        session = aiohttp.ClientSession()
        try:
            async with session.get(f'https://avty.xboxlive.com/users/xuid({xuid})/Activity/History?numItems=1&excludeTypes=Played;BroadcastStart;BroadcastEnd', headers=headers) as recent_activity:
                if recent_activity.status in [200, 201, 202, 204]:
                    data = await recent_activity.json()

                    if len(data['activityItems']) >= 1:
                        print(f' \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] Retrieved \x1b[1;36m{xuid}\x1b[1;37m\'s Recent Activity!')

                        post_link = data['activityItems'][0]['feedItemId']

                        await asyncio.shield(self.like_post(token, post_link, my_xuid, xuid))
                    else:
                        print(f' \x1b[1;37m[\x1b[1;33m!\x1b[1;37m] \x1b[1;36m{xuid} \x1b[1;37mHas No Activity Feed Posts! Skipping This Profile..')
                elif recent_activity.status == 429:
                    print(f' \x1b[1;37m[\x1b[1;35m!\x1b[1;37m] Rate Limited, Sleeping for 2 Minutes!')
                    await asyncio.sleep(120)
                elif recent_activity.status == 401:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] Authorization Token Invalid! Exiting..')
                    os._exit(0)
                else:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] Failed to retrieve \x1b[1;36m{xuid}\x1b[1;37m\'s activity. Status: \x1b[1;33m{recent_activity.status}')
            await session.close()

        except ConnectionResetError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;33mConnectionResetError\x1b[1;37m')
            pass
        except OSError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;31mOSError\x1b[1;37m')
            pass
        except TimeoutError: 
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;31mTimeoutError\x1b[1;37m')
            pass
        
    
    async def like_post(self, token, post_link, my_xuid, xuid):
        headers = {
            'Authorization': token,
            'X-XBL-Contract-Version': '3',
            'Accept-Language': 'en-US',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }

        session = aiohttp.ClientSession()
        try:
            async with session.put(f'https://comments.xboxlive.com/{post_link}/likes/xuid({my_xuid})', headers=headers) as like_request:
                if like_request.status in [200, 201, 202, 204]:
                    print(f' \x1b[1;37m[\x1b[1;32m+\x1b[1;37m] Liked \x1b[1;36m{xuid}\x1b[1;37m\'s Post Successfully!')
                elif like_request.status == 429:
                    print(f' \x1b[1;37m[\x1b[1;35m!\x1b[1;37m] Rate Limited, Sleeping for 2 Minutes!')
                    await asyncio.sleep(120)
                elif like_request.status == 401:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] Authorization Token Invalid! Exiting..')
                    os._exit(0)
                else:
                    print(f' \x1b[1;37m[\x1b[1;31m!\x1b[1;37m] Failed to like \x1b[1;36m{xuid}\x1b[1;37m\'s post. Status: \x1b[1;33m{like_request.status}')


            await asyncio.shield(self.scraper.get_comment_xuids(token, post_link, xuid))
            await session.close()

        except ConnectionResetError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;33mConnectionResetError\x1b[1;37m')
            pass
        except OSError:
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;31mOSError\x1b[1;37m')
            pass
        except TimeoutError: 
            print(' \x1b[1;37m[\x1b[1;33m>\x1b[1;37m] Excepted \x1b[1;31mTimeoutError\x1b[1;37m')
            pass