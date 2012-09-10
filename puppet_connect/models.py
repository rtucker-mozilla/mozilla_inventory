from django.db import models
from systems.models import System
import datetime

class PuppetFact(models.Model):
    fact = models.CharField(max_length = 128, blank=False, null = False)
    value = models.CharField(max_length = 128, blank=True, null = True)
    system = models.ForeignKey(System)

    def __repr__(self):
        return "<PuppetFact %s %s:%s> " % (self.system, self.fact, self.value)

    def __unicode__(self):
        return self.__repr__()

    def save(self, *args, **kwargs):
        """
            Try to see if a fact already exists.
            If it does, we want to take the old value and save it as a 
            PuppetFactVersion with the new value and the old
            If it does not exist, we just save and move on with our lives
        """

        try:
            existing = PuppetFact.objects.get(system=self.system, fact=self.fact)
        except PuppetFact.DoesNotExist:
            existing = False

        if existing:
            """
                We want to backup the old and new values, then overwrite
            """
            versioned_fact = PuppetFactVersion(
                    fact=existing,
                    value=self.value,
                    old_value=existing.value,
                    updated_on = datetime.datetime.now())
            versioned_fact.save()
            self.id = existing.id
        super(PuppetFact, self).save(*args, **kwargs)

class PuppetFactVersion(models.Model):
    fact = models.ForeignKey(PuppetFact)
    value = models.CharField(max_length = 128, blank=True, null = True)
    old_value = models.CharField(max_length = 128, blank=True, null = True)
    updated_on = models.DateTimeField(blank=False, null=False)

    def __repr__(self):
        return "<PuppetFactVersion %s:%s %s> " % (self.fact.fact, self.value, self.updated_on)

    def __unicode__(self):
        return self.__repr__()
    
# Create your models here.
