from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.plugin.http import HTTPPluginControl
from HTTPClient import NVPair

from com.xhaus.jyson import JysonCodec as json
 
test1 = Test(1, "Request resource")
request = HTTPRequest()
test1.record(request)

control = HTTPPluginControl.getConnectionDefaults()
control.setDefaultHeaders([
    NVPair("Content-Type", "application/json"),
])

def login_service(request):
    body = {
        "username":"brian",
        "password":"brian"
    }
    json_body = json.dumps(body)

    result = request.POST("http://localhost:8000/service-login",json_body)
    
    data = json.loads(result.getText())
    grinder.logger.info("login -- " + data["status"])
    
def logout_service(request):
    result = request.POST("http://localhost:8000/service-logout")
    data = json.loads(result.getText())
    grinder.logger.info("logout -- " + data["status"])
    
def submit_transaction_service(request):
    body = {
        "student_id":"student1",
        "session_id":"session1",
        "step":"step1",
        "problem":"problem1",
        "transaction_id":"transaction1",
        "skills":[("skill1","model1")],
        "outcome":"correct",
        "input":"s",
        "selection":"s",
        "action":"keypress",
    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/transaction-plugin/store-transaction",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("store-transaction -- " + str(data["success"]))
    
    

class TestRunner:
    # This method is called for every run.
    def __call__(self):
        # Per thread scripting goes here.
        grinder.logger.info("Hello World")
        login_service(request)
        submit_transaction_service(request)
        logout_service(request)
