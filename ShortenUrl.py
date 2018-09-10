#!/usr/bin/env python
from Controller import Controller
import web


urls = (
    '/retrieve/(.*)', 'retrieve',
    '/create', 'create'
)

app = web.application(urls, globals())

class retrieve:        
    def GET(self, url):
        controll = Controller()
        full_url = controll.retrieveUrl(url)
        web.seeother(full_url)
        
class create:
    def GET(self):
        controll = Controller()
        data_input = web.input()
        if hasattr(data_input, 'CUSTOM_ALIAS'):
            data = controll.createWithAlias(data_input.url, data_input.CUSTOM_ALIAS)
        else:
            data = controll.createWithoutAlias(data_input.url) 
        return str(data)

if __name__ == "__main__":
    app.run()