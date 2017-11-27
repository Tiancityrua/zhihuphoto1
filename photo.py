import re
import requests
import os
import multiprocessing
URL="https://www.zhihu.com/api/v4/questions/37787176/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20&sort_by=default"
if not os.path.exists('images'):
     os.mkdir("images")
def parse(url):
    photourl=[]
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Referer":"https://www.zhihu.com/question/37787176",
        "Host":"www.zhihu.com",
         #自己加上去auth
        "authorization":""
    }
    #匹配照片的正则表达式
    pattern=re.compile('https://pic[1-4]\.zhimg\.com\/[a-z0-9-/_]*?_hd\.jpe?g')
    response=requests.get(url,headers=header)
    data=response.json()
    #内容在“data”的“content”这个节点里面
    realdata=data['data']
    for datacontent in realdata:
        pa=re.compile(pattern)
        result=pa.findall(datacontent['content'])
        finall=list(set(result))
        if finall:
            for a in finall:
                photourl.append(a)
    return photourl
    #进行下载图片
def download(photourl):
    for photo in photourl:
        photoname=photo[28:38]
        img=requests.get(photo).content
        with open('images/'+photoname+'.jpg','wb') as f:
            f.write(img)

allresult=parse(URL)

if __name__=='__main__':
    for i in range(5):
        p=multiprocessing.Process(target=download(allresult),args=(i,))
        p.start()

    print('cpu number'+str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print('child process name '+p.name+'id '+str(p.pid))

    print('process ended')

