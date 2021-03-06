from django.db import models

class UserInfo(models.Model):
    mobile = models.CharField(max_length=12)
    nick_name = models.CharField(max_length=50, null=True)
    passwd = models.CharField(max_length=20, null=True)
    sex = models.IntegerField(null=True)
    birthday = models.CharField(max_length=20, null=True)
    ctime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nick_name

#class Question(models.Model):
#    question_text = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#
#
#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
#
