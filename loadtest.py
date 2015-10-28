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
    
def add_problem_service(request):
    body = {

        "problem_name":"problem1",
        "skills":[("skill1","model1")],
        "tags":["a problem","tag"],

    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/problem-plugin/add-problem",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("add-problem -- " + str(data["success"]))

def set_learned_threshold_service(request):
    body = {
        "threshold":.5,
    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/problem-plugin/set-learned-threshold",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("set-learned-threshold -- " + str(data["success"]))

def get_next_problem_service(request):
    body = {
        "current_problem_name":"problem1",
        "student_id":"student1",
    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/problem-plugin/get-next-problem",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("get-next-problem -- " + str(data["success"]))

def trace_service(request):
    body = {
        "skill":"skill1",
        "student_id":"student1",
        "correct":True
    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/kt-plugin/trace",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("trace -- " + str(data["success"]))
    
def skill_widget_service(request):
    body = {
        "skill":"skill1",
        "student_id":"student1",
        "correct":True
    }
    json_body = json.dumps(body)
    
    result = request.POST("http://localhost:8000/kt-plugin/trace",json_body)
    data = json.loads(result.getText())
    grinder.logger.info("skill-widget -- " + str(data["success"]))

class TestRunner:
    # This method is called for every run.
    def __call__(self):
        # Per thread scripting goes here.
        grinder.logger.info("Starting test")
        login_service(request)
        submit_transaction_service(request)
        add_problem_service(request)
        set_learned_threshold_service(request)
        get_next_problem_service(request)
        trace_service(request)
        skill_widget_service(request)
        logout_service(request)
