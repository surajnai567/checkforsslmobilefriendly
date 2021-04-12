from threading import Lock
import concurrent.futures
from util import get_all_from_email
from sslq import wrapper_has_ssl
from requests import post
from util import write_to_file

lock = Lock()
MAX_THREAD = 3
FILE_LOCATION_FOR_SAVING = 'z.txt'
FILE_LOCATION_TO_READ_FOR = 'xyz.csv'

api_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key="
key = "AIzaSyBUT6q6A99cN1kW6jNNx40o7a2UMf2a56w"  # just put the google api with google search service enable


def request_to_check_for_mobile_friendly_ssl(email:str, port=443):
    domain = email.split("@")[1]
    has_ssl = wrapper_has_ssl(domain, port)
    print("has_ssl", has_ssl, end="\n")
    if has_ssl[1]:
        url = "https://"+domain
    if not has_ssl[1]:
        url = "http://" + domain
    params = {"url": url}
    has_mobile_friendly = post(api_url+key, params)
    m_friend = 'error'


    try:
        if has_mobile_friendly.json()['testStatus']['status'] == "COMPLETE":
            m_friend = has_mobile_friendly.json()["mobileFriendliness"] == "MOBILE_FRIENDLY"
        else:
            m_friend = has_mobile_friendly.json()['testStatus']['status']
    except:
        pass
    print("mobile_friendly: " , domain, m_friend, end="\n")
    return email, m_friend, has_ssl


def main():
   with concurrent.futures.ThreadPoolExecutor(max_workers = MAX_THREAD) as executor:
      results = executor.map(request_to_check_for_mobile_friendly_ssl, get_all_from_email(FILE_LOCATION_TO_READ_FOR))
   for result in results:
      email,has_m, has_ssl = result
      lock.acquire()
      write_to_file(FILE_LOCATION_FOR_SAVING, email, has_m, has_ssl[1])
      lock.release()


if __name__ == '__main__':
    main()