from django.http import HttpResponse
from django.template import loader

from log_parser_app.models import (
    Project, Bug, LogType, LogContentType, LogItem
)


class BaseView(object):

    def __init__(self, request):
        self._request = request


def index(request):

    projects = Project.project.all()
    template = loader.get_template('log_parser_app/index.html')
    context = {
        'projects': projects
    }

    return HttpResponse(template.render(context, request))


def new_log(reqest):

    template = loader.get_template('log_parser_app/new_log.html')
    content = {}
    return HttpResponse(template.render(content, reqest))


def new_log_append(request):
    log = request.POST['log']

    template = loader.get_template('log_parser_app/index.html')
    content = {}
    return HttpResponse(template.render(content, request))


def show_log(request):

    template = loader.get_template('log_parser_app/show_log.html')
    content = {
        'log': 'Generally, when writing a Django app, you’ll evaluate whether '
               'generic views are a good fit for your problem, and you’ll use '
               'them from the beginning, rather than refactoring your code '
               'halfway through. But this tutorial intentionally has focused '
               'on writing the views “the hard way” until now, to focus on '
               'core concepts.\nYou should know basic math before you start '
               'using a calculator.'
    }
    return HttpResponse(template.render(content, request))
