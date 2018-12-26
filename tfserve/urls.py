"""tfserve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from core.views import main, json_test
from core.views import create, destroy
from core.views import create_workspace, destroy_workspace, get_workspace, get_status, push_job, clear, deploy, update, undeploy, predict, get_job, get_finish, get_variable, get_result

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', main),
    path('json_test/', json_test),
    path('create/', create),
    path('destroy/', destroy),
    path('create_workspace/', create_workspace),
    path('destroy_workspace/', destroy_workspace),
    path('get_workspace/', get_workspace),
    path('get_status/', get_status),
    path('push_job/', push_job),
    path('clear/', clear),
    path('deploy/', deploy),
    path('update/', update),
    path('undeploy/', undeploy),
    path('predict/', predict),
    path('get_job/', get_job),
    path('get_finish/', get_finish),
    path('get_variable/', get_variable),
    path('get_result/', get_result),
]
