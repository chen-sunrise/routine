


import urllib2

def send_request():

    #url = 'http://www.baidu.com'
    url = 'http://httpbin.org/user-agent'
    response = urllib2.urlopen(url)
    #request = urllib2.Request(url)
    #print request.get_header('User-Agent')
    #response = urllib2.urlopen(request)

    html = response.read()
    

    return html


if __name__ == '__main__':

    html = send_request()
    #with open('project.txt', 'w') as f:
       # f.write(html)
    print html
