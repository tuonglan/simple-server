from tornado.web import RequestHandler


class FileHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=samples.jpg')
        
        import os
        
        with open('../data/sample.jpg', 'rb') as sin:
            self.write(sin.read())
        self.finish()
       
