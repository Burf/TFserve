# TFserve
TFserve was developed by Hyungjin Kim(flslzk@gmail.com) & Minwoo Kim(fiu900@gmail.com), but anyone interested is welcome to check out the repository and contribute to the project. The sources are licensed under MIT.

<br/>

## What is TFserve?
TFserve is a back-end server based on Django which allows other programs to use facilities of Tensorflow without the need to link Python. TFserve supports separate workspace and job queue.

<br/>

## Dependencies
* Python 3.x
* Django 2.x
* Tensorflow 1.x

<br/>

## Usage

### 1. Cloning the repository
```bash
$ git clone https://github.com/Burf/TFserve.git
$ cd TFserve
```

### 2. Running the server
```bash
$ python manage.py runserver
```

### 3. Enjoy!
http://[Your ip address]:8000/ - Access the post method with the json.

<br/>

## API GUIDE
```bash
{"/":{"context":"API guide",
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
```
