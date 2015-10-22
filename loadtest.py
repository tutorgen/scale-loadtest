from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
 
 
test1 = Test(1, "Request resource")
request = HTTPRequest()
test1.record(request)

class TestRunner:
    # This method is called for every run.
    def __call__(self):
        # Per thread scripting goes here.
        grinder.logger.info("Hello World")
        result = request.GET("http://localhost:8000/")
