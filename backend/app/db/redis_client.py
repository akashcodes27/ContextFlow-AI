import redis
from app.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    decode_responses=True
)




# This file creates a Redis client for your FastAPI application. It's the equivalent of the database connection file but for Redis (your cache/message broker). 