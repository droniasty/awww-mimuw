from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    

class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    supercatalog = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # owner should reference a User object
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # accessibility marker should be a boolean field with default value True
    accessibility_marker = models.BooleanField(default=True)
    # date of accessibility marker change
    accessibility_date = models.DateTimeField(auto_now_add=True)
    # add a method to check if catalog is accessible
    last_modified = models.DateTimeField(auto_now=True)
    def is_accessible(self):
        return self.accessibility_marker
    

class File(models.Model):
    id = models.AutoField(primary_key=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # owner should reference a User object
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # accessibility marker should be a boolean field with default value True
    accessibility_marker = models.BooleanField(default=True)
    # date of accessibility marker change
    accessibility_date = models.DateTimeField(auto_now_add=True)
    # add a method to check if file is accessible
    last_modified = models.DateTimeField(auto_now=True)
    def is_accessible(self):
        return self.accessibility_marker
    

class SectionKind(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__in=['procedure', 'comment', 'code', 'compiler directive','variable declaration', 'assembly code']), 
                name='kind_name_in_set'
            )
        ]
    

class SectionStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__in=['Not tried','compiled', 'not compiled', 'compiled with warnings', ]), 
                name='status_name_in_set'
            )
        ]

class StatusData(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
    description = models.TextField()
    

class FileSection(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    start = models.IntegerField()
    end = models.IntegerField()
    kind = models.ForeignKey(SectionKind, on_delete=models.PROTECT)
    status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
    content = models.TextField()

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    if sender.name == "awwwapp":
        # Only add initial data when migrating "myapp"
        initial_data = [
            {'name': 'procedure'},
            {'name': 'comment'},
            {'name': 'code'},
            {'name': 'compiler directive'},
            {'name': 'variable declaration'},
            {'name': 'assembly code'},
        ]
        for data in initial_data:
            SectionKind.objects.create(**data)


# Create your models here.
