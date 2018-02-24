from django.db import models


class Project(models.Model):
    projects = models.Manager()
    name = models.CharField(max_length=50)


class Bug(models.Model):
    bugs = models.Manager()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=0
    )
    number = models.IntegerField()
    url = models.URLField(max_length=200)
    title = models.TextField(max_length=200, default='')


class LogType(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField()
    example = models.TextField()


class LogContentType(models.Model):
    name = models.CharField(max_length=200)


class LogItem(models.Model):
    logs = models.Manager()
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE)
    log_content_type = models.ForeignKey(
        LogContentType, on_delete=models.CASCADE
    )
    description = models.TextField(max_length=1000, default=None)
    raw = models.TextField()
    valid = models.BooleanField(default=False)
    parse_details = models.TextField()
    parsed = models.TextField()
