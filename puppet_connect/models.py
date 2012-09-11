from django.db import models
from systems.models import System
import datetime

class PuppetFact(models.Model):
    fact = models.CharField(max_length = 128, blank=False, null = False)
    value = models.CharField(max_length = 128, blank=True, null = True)
    system = models.ForeignKey(System)
    updated_on = models.DateTimeField(blank=False, null=False)

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

        self.updated_on = datetime.datetime.now()
        try:
            existing = PuppetFact.objects.get(
                    system=self.system, fact=self.fact)
            """
                We don't want to do anything if the incoming and existing
                values are the same.
            """
            if existing.value == self.value:
                return
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

            """
                We only want to keep the most recent 5 entries
                Get the id of the 5th entry and nuke the others
            """

            try:
                """
                    Try to get the 5th version as ordered by negative id.
                    Using negative id here since it will always be sequential
                    If we have a 5th element in the list, then delete any
                    whose id is less than the 5th element since it's
                    an auto_increment primary key it will be older
                """
                oldest = self.puppetfactversion_set.order_by('-id')\
                        .filter(fact=self)[4]
                self.puppetfactversion_set.filter(
                    fact=self, id__lt=oldest.id).delete()
            except IndexError:
                """
                    There are less than 5 versioned facts, nothing to see here
                    move along
                """
                pass

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
