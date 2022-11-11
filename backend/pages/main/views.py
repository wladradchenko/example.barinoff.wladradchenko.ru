"""Views of main pages."""
import time
import random
import asyncio
from aiohttp import web, ClientSession
import aiohttp_jinja2
# from sqlalchemy.future import select
# import postgresql.model as model


class Handler(web.View):
    """
    Main page of Web-site. (can be personal)
    """
    __slots__ = ("name", "types")
    params = {"source": "python", "engine": "youtube", "async": "true"}

    def __init__(self, request: web.Request = None) -> None:
        """
        Initialization
        :param request: request from user
        """
        super().__init__(request)
        self.params = self.params

    @staticmethod
    async def shorts_filter(video_json: dict) -> bool:
        """
        Method to filter video by tag #shorts in title to increase chance get short video
        :param video_json: YouTube response from serp_api
        :return: bool
        """
        if video_json.get("title") and video_json.get("link"):
            return True if "#shorts" in video_json.get("title") else False
        return False

    @staticmethod
    async def api_ninjas_response(request: web.Request, client: ClientSession, phrase: str) -> list:
        """
        Client session with api_ninjas to get response synonyms
        :param request: request from user
        :param client: ClientSession to parse web
        :param phrase: user request phrase after between first and second slash
        :return: list of synonyms or initial phrase
        """
        async with client.get("https://api.api-ninjas.com/v1/thesaurus?word={}".format(phrase), headers={"X-Api-Key": request.app["config"]["thesaurus_api"]}) as response:
            synonyms = await response.json()
            return synonyms.get("synonyms") + [phrase] if synonyms.get("synonyms") else [phrase]

    async def serp_api_response(self, client: ClientSession, phrase: str) -> list:
        """
        Client session to parse YouTube by serp_api response and get video id
        :param client: ClientSession to parse web
        :param phrase: search phrase
        :return: empy list or list of videos id
        """
        params = self.params
        params["search_query"] = f"#shorts '{phrase.replace('_', ' ')}'"  # search with filter as shorts video

        async with client.get("https://serpapi.com/search/", params=params) as response:
            serp_api_search = await response.json()
            if serp_api_search.get("video_results"):
                videos_id = [video_json["link"].rsplit("?v=", 1)[-1] for video_json in serp_api_search.get("video_results") if await self.shorts_filter(video_json)]
                return videos_id
            return []

    async def get(self, request: web.Request) -> aiohttp_jinja2:
        """
        Method GET
        :param request: request from user
        :return: render page
        """
        phrase = request.match_info.get('name', "Hello Anonymous!")  # filter by word
        self.params["api_key"] = request.app["config"]["serp_api"]

        async with ClientSession() as client:
            # synonyms
            synonyms = await self.api_ninjas_response(request, client, phrase)
            # parse YouTube
            videos_id = await asyncio.gather(*[self.serp_api_response(client, random.choice(synonyms)) for _ in range(4)])
            videos_id = [[video_link] for video_link in set(sum(videos_id, []))]

        if videos_id:
            """How add multi data in Clickhouse by one SQL without loop"""
            # add video id data in DB ClickHouse
            shorts_video_record = list(zip([time.strftime("%Y.%m.%d")] * len(videos_id), sum(videos_id, [])))
            var_string = ', '.join(str(x) for x in shorts_video_record)
            query_string = 'INSERT INTO shorts_video VALUES %s;' % var_string
            await request.app["clickhouse"].client.execute(query_string, "")
            # optimization table to drop duplicates
            await request.app["clickhouse"].client.fetch("OPTIMIZE TABLE shorts_video DEDUPLICATE")
            """How add multi data in Clickhouse by one SQL without loop"""
        else:
            """Get data from Clickhouse tables by SQL"""
            videos_id = [[row] for row in await request.app["clickhouse"].client.fetch("SELECT video_id FROM shorts_video")]
            # key is finished or nothing found
            phrase = "Random!"
            """Get data from Clickhouse tables by SQL"""

        context = {'phrase': phrase, 'videos_id': videos_id}
        response = aiohttp_jinja2.render_template('/main/html/main.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request) -> aiohttp_jinja2:
        """
        Method POST
        :param request: request from user
        :return: render page
        """
        message = await request.post()
        if message.get("name"):
            return web.HTTPFound(f'/{message.get("name")}')
        return web.HTTPFound('/')


"""Product will be page only for music stations / Update GUI of radio / Parse news / Optimization GUI under mobile"""


class Product(web.View):
    """
    Product page of Web-site.
    """
    __slots__ = ("name", "types")

    def __init__(self, request: web.Request = None):
        super().__init__(request)

    @staticmethod
    async def get(request: web.Request):
        name = request.match_info.get('name', "Anonymous")    # filter by author name and product id
        product_id = request.match_info.get('product_id', "Zero")
        msg = [row for row in await request.app["clickhouse"].client.fetch("SELECT * FROM auction")]
        context = {'name': name, 'surname': product_id, 'msg': msg}
        response = aiohttp_jinja2.render_template('/main/html/product.html', request, context)
        response.headers['Content-Language'] = 'ru'

        return response

    @staticmethod
    async def post(request: web.Request):
        message = await request.post()
        # await request.app["clickhouse"].client.execute("INSERT INTO auction VALUES", (datetime.now(), message.get("message")), )
        print("clickhouse", message.get("message"))
        return web.HTTPFound(f'/{request.match_info.get("name")}/{request.match_info.get("product_id")}')
