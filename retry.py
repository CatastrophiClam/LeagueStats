import json
import time
import traceback


def retry_on_decode_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except json.decoder.JSONDecodeError:
                print("Caught Decode error, retrying")
                traceback.print_exc()
                time.sleep(1)
    return wrapper
