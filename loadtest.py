from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.plugin.http import HTTPPluginControl
from HTTPClient import NVPair

from com.xhaus.jyson import JysonCodec as json

import random
from datetime import datetime

test1 = Test(1, "Request resource")
request = HTTPRequest()
test1.record(request)

control = HTTPPluginControl.getConnectionDefaults()
control.setDefaultHeaders([
    NVPair("Content-Type", "application/json"),
])

student_ids = set()
problems={}

start_time = datetime.now().isoformat()

USERNAME = grinder.getProperties()["grinder.username"]
PASSWORD = grinder.getProperties()["grinder.password"]
WEBROOT = grinder.getProperties()["grinder.webroot"]


def login_service(request):
    body = {
        "username":USERNAME,
        "password":PASSWORD
    }
    json_body = json.dumps(body)

    result = request.POST(WEBROOT+"/service-login",json_body)
    
    data = json.loads(result.getText())
    grinder.logger.info("login -- " + data["status"])
    
def logout_service(request):
    result = request.POST(WEBROOT+"/service-logout")
    data = json.loads(result.getText())
    grinder.logger.info("logout -- " + data["status"])
    
def submit_transaction_service(request):
    r = random.randint(0,2)
    if r == 0 or len(student_ids) == 0:
        student_id = "student"+ str(random.randint(0,10000))
        student_ids.update(student_id)
    else:
        student_id = random.sample(student_ids,1)[0]
    
    r = random.randint(0,2)
    if r == 0:
        outcome = "incorrect"
    else:
        outcome = "correct"
        
    problem = random.choice(list(problems.keys()))
    
    body = {
        "student_id":student_id,
        "session_id":"session"+str(start_time),
        "step":problem,
        "problem":problem,
        "transaction_id":"transaction"+str(datetime.now().isoformat()),
        "skills":problems[problem]["skills"],
        "outcome":outcome,
        "input":"s",
        "selection":"s",
        "action":"keypress",
    }
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/transaction-plugin/store-transaction",json_body)
    data = json.loads(result.getText())
    if data["success"] == False:
        grinder.logger.error("store-transaction -- " + str(data["error"]))
    else:
        grinder.logger.info("store-transaction -- " + str(data["success"]))
    
def add_problem_service(request):
    problem_name="problem"+str(random.randint(0,100))
    body = {
        "problem_name":problem_name,
        "skills":[("skill"+str(random.randint(0,100)),"model"+str(random.randint(0,100)))],
        "tags":["a problem","tag"],
    }
    problems[problem_name]=body
    
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/problem-plugin/add-problem",json_body)
    data = json.loads(result.getText())
    
    if data["success"] == False:
        grinder.logger.error("add-problem -- " +str(data["error"]))
    else:
        grinder.logger.info("add-problem -- " + str(data["success"]))

def set_learned_threshold_service(request):
    body = {
        "threshold":.5,
    }
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/problem-plugin/set-learned-threshold",json_body)
    data = json.loads(result.getText())

    if data["success"] == False:
        grinder.logger.error("set-learned-threshold -- " +str(data["error"]))
    else:
        grinder.logger.info("set-learned-threshold -- " + str(data["success"]))

def get_next_problem_service(request):
    problem = random.choice(list(problems.keys()))
    student_id = random.sample(student_ids,1)[0]
    
    body = {
        "current_problem_name":problem,
        "student_id":student_id,
    }
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/problem-plugin/get-next-problem",json_body)
    data = json.loads(result.getText())
    
    if data["success"] == False:
        grinder.logger.error("get-next-problem -- " + str(data["error"]))
    else:
        grinder.logger.info("get-next-problem -- " + str(data["success"]))
        
def trace_service(request):
    problem = random.choice(list(problems.keys()))
    skill = problems[problem]["skills"][0][0]
    student_id = random.sample(student_ids,1)[0]
    body = {
        "skill":skill,
        "student_id":student_id,
        "correct":True
    }
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/kt-plugin/trace",json_body)
    data = json.loads(result.getText())
    if data["success"] == False:
        grinder.logger.error("trace -- " + str(data["error"]))
    else:
        grinder.logger.info("trace -- " + str(data["success"]))
    
def skill_widget_service(request):
    problem = random.choice(list(problems.keys()))
    skill = problems[problem]["skills"][0][0]
    student_id = random.sample(student_ids,1)[0]
    body = {
        "skill":skill,
        "student_id":student_id,
        "correct":True
    }
    json_body = json.dumps(body)
    
    result = request.POST(WEBROOT+"/kt-plugin/skill-widget",json_body)
    data = json.loads(result.getText())
    
    if data["success"] == False:
        grinder.logger.error("skill-widget -- " + str(data["error"]))
    else:
        grinder.logger.info("skill-widget -- " + str(data["success"]))

class TestRunner:
    # This method is called for every run.
    def __call__(self):
        # Per thread scripting goes here.
        grinder.logger.info("Starting test")
        login_service(request)
        add_problem_service(request)
        submit_transaction_service(request)
        trace_service(request)
        set_learned_threshold_service(request)
        get_next_problem_service(request)
        skill_widget_service(request)
        logout_service(request)
