from django.db import models

class Places(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.name)