from itertools import groupby

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views.decorators.http import require_http_methods

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


def _get_logs(bug):
    logs = [log for log in LogItem.logs.filter(bug=bug).all()]
    return sorted(logs, key=lambda l: (l.log_type.name, l.log_content_type.name))


@require_http_methods(['GET'])
def index(request):

    projects = Project.projects.all()

    bugs = [bug for bug in Bug.bugs.all()]
    bugs_projects_sorted = sorted(bugs, key=lambda b: b.project.name)
    bugs_projects_grouped = {
        project: list(group)
        for project, group in groupby(bugs_projects_sorted, key=lambda b: b.project.name)
    }
    logs = dict()
    for i, group in bugs_projects_grouped.items():
        group_number_sorted = sorted(group, key=lambda b: b.number)
        logs[i] = {bug.number: _get_logs(bug) for bug in group_number_sorted}

    template = loader.get_template('log_parser_app/index.html')
    context = {
        'logs': logs
    }

    return HttpResponse(template.render(context, request))


@require_http_methods(['GET'])
def details_create(request):
    projects_names = [p.name for p in Project.projects.all().iterator()]
    context = dict(projects_names=projects_names)

    template = loader.get_template('log_parser_app/details_create.html')
    return HttpResponse(template.render(context, request))


@require_http_methods(['POST'])
def project_create(request):
    """
    Creates new project in db

    :param request:
    :return:
    """

    import ipdb
    ipdb.set_trace()
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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def log_content_type_create(request):
    name = validate_str_2(request.POST['name'])

    LogContentType.objects.create(
        name=name,
    )
    return HttpResponseRedirect(reverse('log_parser_app:index'))


@require_http_methods(['GET'])
def log_create_init(reqest):
    bugs = [dict(number=b.number, title=b.title, project_name=b.project.name)
            for b in Bug.bugs.all().iterator()]
    bugs_sorted = sorted(bugs, key=lambda b: (b['project_name'], b['number']))

    log_types = [l_type.name for l_type in LogType.objects.all().iterator()]
    log_content_types = [
        l_c_type.name for l_c_type in LogContentType.objects.all().iterator()
    ]

    template = loader.get_template('log_parser_app/log_create.html')
    content = dict(
        bugs=bugs_sorted,
        log_types=log_types,
        log_content_types=log_content_types
    )
    return HttpResponse(template.render(content, reqest))


def _show_log_details(request, log_id):
    log = LogItem.logs.get(id=log_id)

    template = loader.get_template('log_parser_app/show_log.html')
    content = {
        'log': log
    }
    return HttpResponse(template.render(content, request))


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
def log_details(request):
    log_id = validate_int(request.POST['log_id'])
    return _show_log_details(request, log_id)
