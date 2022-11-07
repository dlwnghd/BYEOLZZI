from django.db import models

class Answer(models.Model):
    answer_idx = models.AutoField(primary_key=True)
    intent_1 = models.CharField(max_length=10, blank=True, null=True)
    intent_2 = models.CharField(max_length=10, blank=True, null=True)
    ner = models.CharField(max_length=20, blank=True, null=True)
    answer = models.CharField(max_length=100, blank=True, null=True)
    answer_contents = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'answer'


class Location(models.Model):
    location_idx = models.AutoField(primary_key=True)
    metro_code = models.IntegerField(blank=True, null=True)
    metro = models.CharField(max_length=50, blank=True, null=True)
    location_code = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    q = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'location'

class Members(models.Model):
    members_idx = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30, blank=True, null=True)
    pw = models.CharField(max_length=50, blank=True, null=True)
    m_name = models.CharField(max_length=30, blank=True, null=True)
    addr = models.CharField(max_length=200, blank=True, null=True)
    m_location = models.CharField(max_length=10, default="NULL", blank=True, null=True)
    m_state = models.IntegerField(default="NULL", blank=True, null=True)
    m_answer = models.CharField(max_length=10, default="NULL", blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'members'

class MemberLocation(models.Model):
    ml_idx = models.AutoField(primary_key=True)
    m_idx = models.ForeignKey(Members, on_delete=models.CASCADE, db_column='m_idx', blank=True, null=True)
    location_list = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'member_location'