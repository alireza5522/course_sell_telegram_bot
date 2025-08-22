import redis.asyncio as redis
from plugins.log import logger


class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None
        self.isconnected = False

    async def connect(self):
        try:
            self.client = await redis.from_url(
                f'redis://{self.host}:{self.port}/{self.db}', 
                encoding='utf-8', decode_responses=True
            )
            self.isconnected = True
            logger.info(f"✅ Connected to Redis at {self.host}:{self.port}, DB={self.db}")
        except Exception as e:
            logger.error("❌ Error connecting to Redis", exc_info=True)
            raise e

    async def select_db(self, db_index):
        try:
            await self.client.execute_command('SELECT', db_index)
            logger.info(f"Switched to Redis DB {db_index}")
        except Exception as e:
            logger.error(f"❌ Error selecting DB {db_index}", exc_info=True)
            raise e

    async def set_key(self, key, value, ex=900):
        try:
            await self.client.set(name=key, value=value, ex=ex)
            logger.info(f"SET key='{key}' | TTL={ex}")
        except Exception as e:
            logger.error(f"❌ Error setting key '{key}'", exc_info=True)
            raise e

    async def get_key(self, key):
        try:
            value = await self.client.get(key)
            logger.info(f"GET key='{key}'")
            return value
        except Exception as e:
            logger.error(f"❌ Error getting key '{key}'", exc_info=True)
            raise e

    async def delete_key(self, key):
        try:
            await self.client.delete(key)
            logger.info(f"DEL key='{key}'")
        except Exception as e:
            logger.error(f"❌ Error deleting key '{key}'", exc_info=True)
            raise e

    async def scan_keys(self, pattern='*'):
        keys = []
        cursor = '0'
        try:
            while cursor != 0:
                cursor, new_keys = await self.client.scan(cursor=cursor, match=pattern)
                keys.extend(new_keys)
            logger.info(f"SCAN keys with pattern='{pattern}' | found={len(keys)}")
            return keys
        except Exception as e:
            logger.error(f"❌ Error scanning keys with pattern='{pattern}'", exc_info=True)
            raise e

    async def close(self):
        try:
            await self.client.aclose()
            logger.info("Closed Redis connection")
        except Exception as e:
            logger.error("❌ Error closing Redis connection", exc_info=True)
            raise e
        
    async def flushdb(self):
        try:
            await self.client.flushdb()
            logger.info("✅ Flushed current Redis DB")
        except Exception as e:
            logger.error("❌ Error flushing current Redis DB", exc_info=True)
            raise e

    async def flushall(self):
        try:
            await self.client.flushall()
            logger.info("✅ Flushed ALL Redis databases")
        except Exception as e:
            logger.error("❌ Error flushing ALL Redis databases", exc_info=True)
            raise e



user_data = RedisManager()
