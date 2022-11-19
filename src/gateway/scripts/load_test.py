from pprint import pprint
import requests, time

gateway_url = "http://video-to-mp3.aksaman.com/ping"
auth_svc_url = "http://auth.video-to-mp3.aksaman.com/general/api/v1/results"


def load_test(url, iterations=1000):
    res = {}
    for i in range(iterations):
        print(f"{url}: Iteration: {i}/{iterations}", end="\r")
        start = time.monotonic()
        r = requests.get(url)
        taken = time.monotonic() - start
        if r.status_code == 200:
            host = r.json().get("host", "na")
        else:
            host = "error"
            print(f"{i=}, error:{r.text=}")
        d = res.setdefault(host, {"count": 0, "time": 0})
        d["count"] += 1
        d["time"] += taken
        d["time"] = round(d["time"], 2)
        d["avg"] = round(d["time"] / (d["count"] + 1), 2)
    pprint(res)


if __name__ == "__main__":
    iterations = 1000
    load_test(auth_svc_url, iterations=iterations)
    load_test(gateway_url, iterations=iterations)
