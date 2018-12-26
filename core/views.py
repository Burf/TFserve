#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from burf.common.util import VariableEncoder, ValueObject
from burf.common.volume import Volume
from burf.tensorflow.multiworkspace import MultiWorkspace

__RESPONSE_HTTP__ = "Please access the post method with the json."
__API_GUIDE__ = {"/":{"context":"API guide",
                      "json":{"requset":None,
                              "response":{"request_result":"Request result",
                                          "result":"API guide"}}},
                 "/json_test/":{"context":"Json reflector",
                                "json":{"requset":"Input json",
                                        "response":{"request_result":"Request result",
                                                    "result":"Input json"}}},
                 "/create/":{"context":"Server on(Default:Created)",
                             "json":{"requset":None,
                                     "response":{"request_result":"Request result",
                                                 "result":"Server on result"}}},
                 "/destroy/":{"context":"Server off",
                              "json":{"requset":None,
                                      "response":{"request_result":"Request result",
                                                  "result":"Server off result"}}},
                 "/create_workspace/":{"context":"Create workspace",
                                       "json":{"requset":{"name":"Workspace name(Default:Random)",
                                                          "type":"0 is multiprocess, 1 is thread(Default:0)",
                                                          "time_interval":"Time interval for checking job(Default:1)"},
                                               "response":{"request_result":"Request result",
                                                           "result":"Created workspace name"}}},
                 "/destroy_workspace/":{"context":"Destroy workspace",
                                        "json":{"request":{"name":"Workspace name(Default:All workspace)"},
                                                "response":{"request_result":"Request result",
                                                            "result":"Workspace destruction result"}}},
                 "/get_workspace/":{"context":"Get workspace name",
                                    "json":{"requset":None,
                                            "response":{"request_result":"Request result",
                                                        "result":"Created workspace name"}}},
                 "/get_status/":{"context":"Get workspace status",
                                 "json":{"requset":{"name":"Workspace name(Necessary field)"},
                                         "response":{"request_result":"Request result",
                                                     "result":"Workspace status"}}},
                 "/push_job/":{"context":"Push job by python file or script",
                               "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                  "job":"File path or script(Necessary field)",
                                                  "type":"0 is file, 1 is script(Default:0)",
                                                  "clear":"Clear memory before running job(Defalut:False)",
                                                  "timeout":"Wait time for job result(Default:1)",
                                                  "time_interval":"Time interval for checking job(Default:1)"},
                                       "response":{"request_result":"Request result",
                                                   "result":{"job":"Job number",
                                                             "finish":"Complete status for job",
                                                             "result":"Executed job result",
                                                             "time":"Response time",
                                                             "variable":{"Variable name":"Variable value"}}}}},
                 "/clear/":{"context":"Push job for clear memory in push_job API",
                            "json":{"requset":{"name":"Workspace name(Necessary field)",
                                               "timeout":"Wait time for job result(Default:1)",
                                               "time_interval":"Time interval for checking job(Default:1)"},
                                    "response":{"request_result":"Request result",
                                                "result":{"job":"Job number",
                                                          "finish":"Complete status for job",
                                                          "result":"Executed job result",
                                                          "time":"Response time"}}}},
                 "/deploy/":{"context":"Push job for model deployment",
                               "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                  "path":"Model path(Necessary field)",
                                                  "device":"Device name(Default:'/cpu:0')",
                                                  "timeout":"Wait time for job result(Default:1)",
                                                  "time_interval":"Time interval for checking job(Default:1)"},
                                       "response":{"request_result":"Request result",
                                                   "result":{"job":"Job number",
                                                             "finish":"Complete status for job",
                                                             "result":"Executed job result",
                                                             "time":"Response time"}}}},
                 "/update/":{"context":"Push job for update of deployed model",
                               "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                  "path":"Model path(Necessary field)",
                                                  "timeout":"Wait time for job result(Default:1)",
                                                  "time_interval":"Time interval for checking job(Default:1)"},
                                       "response":{"request_result":"Request result",
                                                   "result":{"job":"Job number",
                                                             "finish":"Complete status for job",
                                                             "result":"Executed job result",
                                                             "time":"Response time"}}}},
                 "/undeploy/":{"context":"Push job for undeployment of deployed model",
                               "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                  "timeout":"Wait time for job result(Default:1)",
                                                  "time_interval":"Time interval for checking job(Default:1)"},
                                       "response":{"request_result":"Request result",
                                                   "result":{"job":"Job number",
                                                             "finish":"Complete status for job",
                                                             "result":"Executed job result",
                                                             "time":"Response time"}}}},
                 "/predict/":{"context":"Push job for prediction of deployed model",
                               "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                  "fetches":"List or string by collection key or tensor name'(Necessary field)",
                                                  "feed_dict":"Dictionary by collection key or tensor name & feeding data(Default:None)",
                                                  "timeout":"Wait time for job result(Default:1)",
                                                  "time_interval":"Time interval for checking job(Default:1)"},
                                       "response":{"request_result":"Request result",
                                                   "result":{"job":"Job number",
                                                             "finish":"Complete status for job",
                                                             "result":"Executed job result",
                                                             "time":"Response time"}}}},
                 "/get_job/":{"context":"Get residual job count",
                              "json":{"requset":{"name":"Workspace name(Necessary field)"},
                                      "response":{"request_result":"Request result",
                                                  "result":"Residual job count"}}},
                 "/get_finish/":{"context":"Check whether job is executing",
                                 "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                    "job":"Job number(Default:Last job number)"},
                                         "response":{"request_result":"Request result",
                                                     "result":"Complete status for job"}}},
                 "/get_variable/":{"context":"Get variable by executed jobs in push_job API",
                                   "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                      "variable":"Variable name(Default:All variable)"},
                                           "response":{"request_result":"Request result",
                                                       "result":{"Variable name":"Variable value"}}}},
                 "/get_result/":{"context":"Get result for executed job",
                                 "json":{"requset":{"name":"Workspace name(Necessary field)",
                                                    "job":"Job number(Default:All result)"},
                                         "response":{"request_result":"Request result",
                                                     "result":"Executed job result"}}}}
VOL = Volume()
STORE = VOL.create_volume("__TFSERVE__")
MW = MultiWorkspace(STORE)

@csrf_exempt
def main(request):
    if request.method == "POST":
        try:
            json.loads(request.body)
            response_json = {"request_result":True, "result":__API_GUIDE__}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def json_test(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for k, v in data.items():
                print(k, v)
            response_json = {"request_result":True, "result":data}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def create(request):
    if request.method == "POST":
        try:
            json.loads(request.body)
            result = MW.create(STORE)
            response_json = {"request_result":True, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def destroy(request):
    if request.method == "POST":
        try:
            json.loads(request.body)
            result = MW.destroy()
            response_json = {"request_result":True, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def create_workspace(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.type, int):
                vo.type = 0
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            result = MW.create_workspace(vo.name, vo.type, vo.time_interval)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def destroy_workspace(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = MW.destroy_workspace(vo.name)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def get_workspace(request):
    if request.method == "POST":
        try:
            json.loads(request.body)
            result = MW.get_workspace()
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__) 
    
@csrf_exempt
def get_status(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = MW.get_status(vo.name)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

def __check_job__(name, job_num, timeout = 1, time_interval = 1):
    result = None
    start_time = time.time()
    response_time = 0.0
    while response_time < timeout:
        job_finish = MW.get_finish(name, job_num)
        if job_finish:
            job_result = VariableEncoder(MW.get_result(name, job_num), encoder_func)
            result = {"job":job_num, "finish":job_finish, "result":job_result, "time":response_time}
            break
        else:
            time.sleep(time_interval)
            response_time = round(time.time() - start_time, 2)
    return result
    
@csrf_exempt
def push_job(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.type, int):
                vo.type = 0
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            if not isinstance(vo.clear, bool):
                vo.clear = False
            job_num = None
            if vo.name is not None and vo.job is not None:
                job_num = MW.push_job(vo.name, vo.job, vo.type, vo.clear)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
                if isinstance(result, dict):
                  result["variable"] = VariableEncoder(MW.get_variable(vo.name), encoder_func)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout, "variable":None}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
      
@csrf_exempt
def clear(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            job_num = None
            if vo.name is not None:
                job_num = MW.clear(vo.name)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def deploy(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            if not isinstance(vo.device, str):
                vo.device = "/cpu:0"
            job_num = None
            if vo.name is not None and vo.path is not None:
                job_num = MW.deploy(vo.name, vo.path, vo.device)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            job_num = None
            if vo.name is not None and vo.path is not None:
                job_num = MW.update(vo.name, vo.path)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def undeploy(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            job_num = None
            if vo.name is not None:
                job_num = MW.undeploy(vo.name)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
    
@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            if not isinstance(vo.timeout, int):
                vo.timeout = 1
            if not isinstance(vo.time_interval, int):
                vo.time_interval = 1
            job_num = None
            if vo.name is not None and vo.fetches is not None:
                job_num = MW.predict(vo.name, vo.fetches, vo.feed_dict)
            result = None
            request_result = False
            if job_num is not None:
                request_result = True
                result = __check_job__(vo.name, job_num, vo.timeout, vo.time_interval)
            if result is None:
                result = {"job":job_num, "finish":False, "result":None, "time":vo.timeout}
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def get_job(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = MW.get_job(vo.name)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def get_finish(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = MW.get_finish(vo.name, vo.job)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)
      
@csrf_exempt
def get_variable(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = None
            if isinstance(vo.variable, list):
                variable = MW.get_variable(vo.name)
                if variable is not None:
                    result = {}
                    for var in vo.variable:
                        value = None
                        if var in variable:
                            value = variable[var]
                        result[var] = value
            else:
                result = MW.get_variable(vo.name, vo.variable)
            result = VariableEncoder(result, encoder_func)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

@csrf_exempt
def get_result(request):
    if request.method == "POST":
        try:
            vo = ValueObject(json.loads(request.body))
            result = VariableEncoder(MW.get_result(vo.name, vo.job), encoder_func)
            request_result = result is not None
            response_json = {"request_result":request_result, "result":result}
        except Exception as e:
            print(e)
            response_json = {"request_result":False, "result":str(e)}
        return JsonResponse(response_json)
    else:
        return HttpResponse(__RESPONSE_HTTP__)

def encoder_func(value):
    mod = type(value).__module__
    if mod == "numpy":
        value = value.tolist()
    elif mod == "pandas.core.frame":
        value = value.to_csv()
    elif "pandas.core.indexes" in mod:
        value = value.tolist()
    else:
        try:
            json.dumps(value)
        except:
            try:
                value = str(value)
            except:
                value = None
    return value
