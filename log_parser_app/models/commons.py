from django.db import models


class Project(models.Model):
    project = models.Manager()
    name = models.CharField(max_length=50)


class Bug(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=0
    )
    number = models.IntegerField()
    url = models.URLField(max_length=200)


class LogType(models.Model):
    type_name = models.CharField(max_length=50)
    details = models.TextField()
    example = models.TextField()


class LogContentType(models.Model):
    type_name = models.CharField(max_length=200)


class LogItem(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    log_type = models.ForeignKey(LogType, on_delete=models.CASCADE)
    log_content_type = models.ForeignKey(
        LogContentType, on_delete=models.CASCADE
    )
    raw = models.TextField()
    valid = models.BooleanField(default=False)
    parse_details = models.TextField()
    parsed = models.TextField()
