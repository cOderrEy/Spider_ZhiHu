import requests, json, time, os, threading, pymysql, get_context
from headers import get_headers

Lock = threading.Lock()
db = pymysql.connect("127.0.0.1", "spider", "spider", "spider_result")
header = {
    "Host"                  : "www.zhihu.com",
    "Referer"               : "https://www.zhihu.com/",
    "user-agent"            : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def get_data(url):
    try:
        r = requests.get(url, headers=header)
        data = r.json()
    except Exception as e:
        time.sleep(15)
        with open(os.path.dirname(os.path.abspath(__file__))+"/error.log", 'a') as f:
            f.write(url+"\n"+e+"\n"+"=====================================================================\n")
        return get_data(url)
    return data

def from_timeline(userid):
    url = "https://www.zhihu.com/api/v4/members/%s/activities"%userid
    data = get_data(url)
    while (not data['paging']['is_end']):
        for answer in data['data']:
            if (answer['action_text'] == "赞同了回答"):
                answer_id   = answer['target']['id']
                question_id = answer['target']['question']['id']
                answer_url = "https://www.zhihu.com/question/%s/answer/%s"%(question_id, answer_id)
                print(get_context.context(answer_url, json.dumps(answer['target']['author']), json.dumps(answer['target']['question'])))
        data = get_data(data['paging']['next'])

if __name__ == "__main__":
    from_timeline("excited-vczh")