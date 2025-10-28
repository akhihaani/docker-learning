import os
import time
from flask import Flask, jsonify
import redis

# Config from env, with defaults for local dev
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB   = int(os.getenv("REDIS_DB", "0"))
COUNTER_KEY = os.getenv("COUNTER_KEY", "visits")

# One global Redis client with a connection pool
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def wait_for_redis(max_tries=5, delay=0.3):
    """Ping Redis a few times before giving up."""
    for i in range(max_tries):
        try:
            if r.ping():
                return True
        except redis.exceptions.RedisError:
            time.sleep(delay * (i + 1))
    return False

count = Flask(__name__)

@count.route("/")
def index():
    return "Welcome to the CoderCo Flask + Redis counter"

@count.route("/count")
def count():
    # INCR is atomic in Redis
    value = r.incr(COUNTER_KEY)
    return jsonify(count=value)

if __name__ == "__main__":
    # Optional warmup so you fail early with a clear message
    if not wait_for_redis():
        raise SystemExit(f"Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
    count.run(host="0.0.0.0", port=5004)