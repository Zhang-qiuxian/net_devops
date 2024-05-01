import redis
from redis import ConnectionPool, Redis
from redis.client import Redis

pool = ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
print(pool, type(pool))

conn:Redis = Redis(connection_pool=pool)

print(conn, type(conn))

print(conn.ping())
