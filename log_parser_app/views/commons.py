from django.http import HttpResponse
from django.template import loader

from log_parser_app.models import (
    Project, Bug, LogType, LogContentType, LogItem
)


def index(request):

    projects = Project.project.all()
    template = loader.get_template('log_parser_app/index.html')
    context = {
        'projects': projects
    }

    return HttpResponse(template.render(context, request))
