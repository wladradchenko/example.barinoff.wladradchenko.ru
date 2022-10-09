"""Setting of project by config file."""
import pathlib
import json
import aiofiles
import asyncio
import logging

BASE_DIR = pathlib.Path(__file__).parent.parent

"""
================
Config from file
================
"""
config_path = BASE_DIR / "settings" / "config.json"


async def get_config(path: pathlib.Path) -> dict:
    """
    Get config by aiofiles example use read/write from file
    P.S. read json can be without async but ones example how async work with file
    :param path: path to config
    :return: dict
    """
    async with aiofiles.open(path, mode='r') as file:
        contents = await file.read()

    return json.loads(contents)

config = asyncio.run(get_config(config_path))

"""
================
Loger
================
"""
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
