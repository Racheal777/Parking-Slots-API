import json

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

async def write_to_redis(key, value):
    await r.set(key, json.dumps(value))


async def read_from_redis(key):
    redis_value = await r.get(key)
    if redis_value is not None:
        return json.loads(redis_value)
    return None




def clear_redis_data(key):
    r.delete(key)

