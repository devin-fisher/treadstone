import daemon
import jwt
import os
import requests
from calendar import timegm
from datetime import datetime, timedelta

from websocket import create_connection
import websocket
import time
import uuid


TOKEN_FILE = ".token"
TOKEN_ISSUE_API = "http://api.lolesports.com/api/issueToken"

DATA_DIRECTORY = "data"

STATS_API = "ws://livestats.proxy.lolesports.com/stats"
TOKEN_EXPRIED_MOD = 1000
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2IjoiMS4wIiwiamlkIjoiNzY2ZDA4YWItNGI4Mi00NWMzLTgyZGUtYjNmNGQxYWNhMjRjIiwiaWF0IjoxNDcwMDY2MDgxNzA3LCJleHAiOjE0NzA2NzA4ODE3MDcsIm5iZiI6MTQ3MDA2NjA4MTcwNywiY2lkIjoiYTkyNjQwZjI2ZGMzZTM1NGI0MDIwMjZhMjA3NWNiZjMiLCJzdWIiOnsiaXAiOiI2Ny4xNjEuMjQxLjIxMSIsInVhIjoiTW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNTEuMC4yNzA0LjEwNiBTYWZhcmkvNTM3LjM2In0sInJlZiI6WyJ3YXRjaC4qLmxvbGVzcG9ydHMuY29tIl0sInNydiI6WyJsaXZlc3RhdHMtdjEuMCJdfQ.KQVuSivkPAqR7uV5U7aPH7AgdWVnYlhrXhdPp1pp65I"

WS = None
RUNNING = True

MIN_RETRY_TIME = 10
MAX_RETRY_TIME = 60
CUR_RETRY_TIME = 1

def _get_token_from_disk():
    file_path = os.path.join(os.getcwd(), TOKEN_FILE)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    else:
        return None

def _get_new_token():
    print("!" * 20)
    r = requests.get(TOKEN_ISSUE_API)
    j = r.json()
    rtn = j.get("token", None)

    if rtn:
        with open(os.path.join(os.getcwd(), TOKEN_FILE), 'w') as f:
            f.write(rtn)
        return rtn
    else:
        return None
        #Throw error, we did not get a token

def _token_is_expired(token):
    decode_token = jwt.decode(token, verify=False)
    exp = decode_token['exp']
    exp = exp/1000
    exp = exp - TOKEN_EXPRIED_MOD
    now = timegm(datetime.utcnow().utctimetuple())

    # print "now:" + str(now)
    # print "exp:" + str(exp)
    if exp < (now):
        return True
    else:
        return False


def _get_token():
    token = _get_token_from_disk()
    if token is None:
        token = _get_new_token()

    if _token_is_expired(token):
        token = _get_new_token()

    return token


def _on_message(ws, message):
    name = str(uuid.uuid4())
    # print name
    loc = os.path.join(os.getcwd(), DATA_DIRECTORY, name)
    with open(loc, "w") as f:
        f.write(message)

def _on_error(ws, error):
    print error
    # CUR_RETRY_TIME = min((CUR_RETRY_TIME * 2) + MIN_RETRY_TIME, MAX_RETRY_TIME)
    # print CUR_RETRY_TIME

def _on_close(ws):
    print "### closed ###"

def _on_open(ws):
    print "### open ###"

def main():
    data_dir = os.path.join(os.getcwd(), DATA_DIRECTORY)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print min((CUR_RETRY_TIME * 2) + MIN_RETRY_TIME, MAX_RETRY_TIME)
    while(RUNNING):
        time.sleep(CUR_RETRY_TIME)
        token = _get_token()
        url = STATS_API + "?jwt=" +token
        url = "ws://192.168.1.2:9999/"
        print(url)
        websocket.enableTrace(True)
        WS = websocket.WebSocketApp(url,
                                  on_message = _on_message,
                                  on_error = _on_error,
                                  on_close = _on_close)
        WS.on_open = _on_open
        WS.run_forever(ping_interval=None)


if __name__ == "__main__":
    # context = daemon.DaemonContext(
    # working_directory='/var/opt/live_game_grabber',
    # umask=0o002,
    # pidfile=lockfile.FileLock('/var/run/live_game_grabber.pid'),
    # )

    # context.signal_map = {
    # signal.SIGTERM: program_cleanup,
    # signal.SIGHUP: 'terminate',
    # signal.SIGUSR1: reload_program_config,
    # }

    # with context:
    #     main(args)
    main()
