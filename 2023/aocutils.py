import os
import requests

def getDataInput(day, session_id=None):
    if session_id is None:
        session_id = os.getenv("AOC_SESSION_ID")
    if session_id is None:
        RuntimeError("Advent of Code session ID not provided")
    url = f"https://adventofcode.com/2023/day/{day}/input"
    cookies_map = {"session": session_id}
    req_ret = requests.get(url, cookies=cookies_map)
    return_val = [s for s in req_ret.text.split('\n')]
    if return_val[-1] == "":
        return_val.pop(-1)
    return return_val

def printResult(part, value):
    print(f"Result {part}: {value}")