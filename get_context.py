import requests, time, os, json
from lxml import etree
from main import header, Lock, db
from filter import is_target

def get(url):
    try:
        r = requests.get(url, headers=header)
        selector = etree.HTML(r.text)
    except Exception as e:
        time.sleep(15)
        with open(os.path.dirname(os.path.abspath(__file__))+"/context_error.log", 'a') as f:
            f.write(url+"\n"+e+"\n"+"=====================================================================\n")
        return get(url)
    with open(os.path.dirname(os.path.abspath(__file__))+"/output.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    return selector.xpath('//div[@class="RichContent-inner"]')

def context(url, author, question):
    print(url)
    content = get(url)
    print(content)
    try:
        text = ''.join(content[0].xpath('*/text()'))
        images = content[0].xpath('//img/@data-original')
    except:
        with open(os.path.dirname(os.path.abspath(__file__))+"/bad_request.log", 'a') as f:
            f.write(url+"\n")
        return False
    if (is_target(text)):
        if Lock.acquire():
            sql = ""
            try:
                cursor = db.cursor()
                for image in images:
                    sql = "INSERT INTO zhihu(author, question, image) VALUES('%s', '%s', '%s');"%(author, question, image)
                    cursor.execute(sql)
                db.commit()
            except:
                with open(os.path.dirname(os.path.abspath(__file__))+"/dirtydata.log", 'a') as f:
                    f.write(json.dumps(images)+"\n"+sql+"\n")
                db.rollback()
                Lock.release()
                return False
            Lock.release()
        return True
    else:
        return False

