import requests
from threading import Lock
import concurrent.futures
from util import get_all_from_email

lock = Lock()

api_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key="
key = "AIzaSyBUT6q6A99cN1kW6jNNx40o7a2UMf2a56w"

test = "https://bassfishingtx.com"


def request_to_check_for_mobile_friendly(email:str):
    #url = "http://"+email.split("@")[1]
    params = {"url": email}
    header = {'Content-type': 'application/json'}
    return email, requests.post(api_url+key, params = params, headers=header)


def main():
   with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor:
      results = executor.map(request_to_check_for_mobile_friendly, get_all_from_email('ani.txt'))
   for result in results:
      url, resu = result
      lock.acquire()
      print("url", resu.json())
      # write to file
      lock.release()


email , res = request_to_check_for_mobile_friendly("http://targetmysite.com")

print(res.text)