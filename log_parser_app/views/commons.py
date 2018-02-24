from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from log_parser_app.models import (
    Project, Bug, LogType, LogContentType, LogItem
)
from log_parser_app.lib.validators import (
    validate_int, validate_str_1, validate_str_2,
    validate_project_name, validate_url
)
from log_parser_app.lib.parser import LogParser


class BaseView(object):

    def __init__(self, request):
        self._request = request


def index(request):

    projects = Project.projects.all()
    template = loader.get_template('log_parser_app/index.html')
    context = {
        'projects': projects
    }

    return HttpResponse(template.render(context, request))


def details_create(request):
    projects_names = [p.name for p in Project.projects.all().iterator()]
    context = dict(projects_names=projects_names)

    template = loader.get_template('log_parser_app/details_create.html')
    return HttpResponse(template.render(context, request))


def project_create(request):
    """
    Creates new project in db

    :param request:
    :return:
    """
    name = validate_project_name(request.POST['name'])

    # check if just exist:
    existing_project = Project.projects.all().filter(name__exact=name).first()
    if not existing_project:
        Project.projects.create(
            name=name
        )
    else:
        return details_create(request)
    return HttpResponseRedirect(reverse('log_parser_app:details_create'))


def bug_create(request):

    project_name = validate_project_name(request.POST['project_name'])
    project = Project.projects.get(name=project_name)
    number = validate_int(
        request.POST['number'],
        min_value=0,
        max_value=999999999
    )
    url = validate_url(
        request.POST['url']
    )
    title = validate_str_2(
        request.POST['title'],
        min_len=0,
        max_len=200
    )
    Bug.bugs.create(
        project=project,
        number=number,
        url=url,
        title=title
    )
    return HttpResponseRedirect(reverse('log_parser_app:details_create'))


def log_type_create(request):
    name = validate_str_2(request.POST['name'])
    details = request.POST['details']
    example = request.POST['example']

    LogType.objects.create(
        name=name,
        details=details,
        example=example
    )
    return HttpResponseRedirect(reverse('log_parser_app:index'))


def log_content_type_create(request):
    name = validate_str_2(request.POST['name'])

    LogContentType.objects.create(
        name=name,
    )
    return HttpResponseRedirect(reverse('log_parser_app:index'))


def log_create_init(reqest):
    projects_names = [p.name for p in Project.projects.all().iterator()]
    bugs = [
        dict(
            number=b.number, title=b.title, projects_name=b.project.name
        ) for b in Bug.bugs.all().iterator()
    ]
    log_types = [l_type.name for l_type in LogType.objects.all().iterator()]
    log_content_types = [
        l_c_type.name for l_c_type in LogContentType.objects.all().iterator()
    ]

    template = loader.get_template('log_parser_app/log_create.html')
    content = dict(
        projects_names=projects_names,
        bugs=bugs,
        log_types=log_types,
        log_content_types=log_content_types
    )
    return HttpResponse(template.render(content, reqest))


def log_create(request):
    bug = Bug.bugs.get(number=request.POST['bug_number'])
    log_type = LogType.objects.get(name=request.POST['log_type'])
    log_content_type = LogContentType.objects.get(
        name=request.POST['log_content_type']
    )

    parsed_log = LogParser(request.POST['raw_log'])
    description = validate_str_2(
        request.POST['description'],
        missing_allowed=True, default='',
        min_len=0, max_len=200
    )

    created_log = LogItem.logs.create(
        bug=bug,
        log_type=log_type,
        log_content_type=log_content_type,
        raw=parsed_log.raw,
        description=description,
        valid=parsed_log.valid,
        parse_details=parsed_log.parse_details,
        parsed=parsed_log.parsed,
    )
    return _show_log_details(request, created_log.id)


def _show_log_details(request, log_id):
    log = LogItem.logs.get(id=log_id)

    template = loader.get_template('log_parser_app/show_log.html')
    content = {
        'log': log
    }
    return HttpResponse(template.render(content, request))


def log_details(request):
    log_id = validate_int(request.POST('log_id'))
    return _show_log_details(request, log_id)
