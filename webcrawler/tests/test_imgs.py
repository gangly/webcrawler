import json
import urllib
import requests

# url = "http://haiheyuanzhu.fang.com/photo/list_907_1110769899.htm"
url = "http://haiheyuanzhu.fang.com/photo/list_903_1110769899.htm"
elems = url.split('/photo/')
host = elems[0]
para1 = elems[1].split('.')[0]
para2 = para1.split('_')
ptype = para2[1]
pnewcode = para2[2]
args = (host, pnewcode, ptype)
new_url = "%s/house/ajaxrequest/photolist_get.php?newcode=%s&type=%s&nextpage=" % args

print new_url


# new_url = "http://haiheyuanzhu.fang.com/house/ajaxrequest/photolist_get.php?newcode=1110769899&type=907&nextpage="
# new_url = "http://haiheyuanzhu.fang.com/house/ajaxrequest/photolist_get.php?newcode=1110769899&type=904&nextpage="

nextpage = 1
simg = []
while True:
    real_url = new_url + str(nextpage)
    # print real_url
    ret = requests.get(real_url)
    if ret.status_code != 200:
        break
    data = json.loads(ret.content)
    if isinstance(data, list):
        for dat in data:
            simg.append(dat['url_s'])
    else:
        break
    nextpage += 1
bimg = [img.replace('124x82', '880x578') for img in simg]

print len(simg)
print bimg
