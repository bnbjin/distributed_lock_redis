import time
import uuid

import redis

def acquire_lock(conn, lockname, acquire_timeout=10):
    identifier = str(uuid.uuid4())

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):
            return identifier

        time.sleep(.001)

    return False

def release_lock(conn, lockname, identifier):
    with conn.pipeline(True) as pipe:
        while True:
            try:
                pipe.watch(lockname)

                value = pipe.get(lockname)
                if value is None:
                    break

                if value.decode('utf-8') == identifier:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True

                pipe.unwatch()
                break

            except redis.exceptions.WatchError:
                pass

    return False
