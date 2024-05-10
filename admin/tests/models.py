from django.db import models

from users.models import DirectionOdEducation, LANGUAGES, Applicant


class Science(models.Model):
    nameUz = models.CharField(max_length=255)
    nameRu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'sciences'


class Test(models.Model):
    directionOfEducation = models.ForeignKey(DirectionOdEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='tests')
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, null=True, blank=True, related_name='tests')
    questionsCount = models.IntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    isActive = models.BooleanField(default=False)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.directionOfEducation}, {self.science} -> {self.language}"

    class Meta:
        db_table = 'tests'


TEST_RESPONSES = (
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    image = models.CharField(max_length=255, null=True, blank=True)
    question = models.TextField()
    trueResponse = models.CharField(max_length=1, choices=TEST_RESPONSES)

    def __str__(self):
        return f"{self.test}: {self.pk}"

    class Meta:
        db_table = 'questions'


class ExamResult(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='exam_result')
    result = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.applicant}: {self.result}"

    class Meta:
        db_table = 'exam_results'
