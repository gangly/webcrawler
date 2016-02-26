# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication

import random
from webcrawler.conf import middlewareconf
from webcrawler.lib.model.redisdb import get_redis_server

# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def __init__(self):
        self.rdb = get_redis_server()
        self.proxy = ''

    def process_request(self, request, spider):
        # Set the location of the proxy
        # print request.meta['proxy']
        if 'retrytimes' not in request.meta:
            request.meta['retrytimes'] = 0

        if request.meta['retrytimes'] < middlewareconf.MAX_RETYR_TIMES:
            self.proxy = self.rdb.srandmember('ipport')
            if self.proxy:
                request.meta['proxy'] = "http://%s" % self.proxy
                print self.proxy
            elif 'proxy' in request.meta:
                del request.meta['proxy']
        elif 'proxy' in request.meta:
            del request.meta['proxy']

    def process_exception(self, request, exception, spider):

        if 'proxy' in request.meta:
            self.rdb.srem('ipport', self.proxy)
            print 'delete: ' + self.proxy
        request.meta['retrytimes'] += 1
        print request.meta['retrytimes']
        return request
