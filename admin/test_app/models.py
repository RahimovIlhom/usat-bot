from django.db import models

from users.models import LANGUAGES, Applicant, Science


class Test(models.Model):
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, null=True, blank=True, related_name='tests',
                                verbose_name="Test fani")
    questionsCount = models.IntegerField(verbose_name="Arizachiga fan bo'yicha ko'rinuvchi savollar soni")
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name="Test tili")
    isActive = models.BooleanField(default=False, verbose_name="Test aktivmi?")
    deleted = models.BooleanField(default=False, verbose_name="Test o'chirilganmi?")
    createdTime = models.DateTimeField(auto_now_add=True, verbose_name="Test ochilgan sana")

    def __str__(self):
        return f"{self.science} -> {self.language}: {self.id}"

    class Meta:
        db_table = 'tests'
        verbose_name = "Test"
        verbose_name_plural = "Testlar"


TEST_RESPONSES = (
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions',
                             verbose_name="Savol testi")
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name="Savol rasmi")
    question = models.TextField(verbose_name="Savol matni")
    trueResponse = models.CharField(max_length=1, choices=TEST_RESPONSES, default='a', verbose_name="To'g'ri javob")
    active = models.BooleanField(default=True, verbose_name="Savolning aktivligi")
    response1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Javob 1")
    response2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Javob 2")
    response3 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Javob 3")
    response4 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Javob 4")

    def __str__(self):
        return f"{self.test}: {self.pk}"

    class Meta:
        db_table = 'questions'
        verbose_name = "Savol"
        verbose_name_plural = "Test savollari"


class ExamResult(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='exam_result',
                                  verbose_name="Arizachi")
    userResponses = models.JSONField(null=True, blank=True, verbose_name="Foydalanuvchi javoblari")
    trueResponseCount = models.PositiveIntegerField(verbose_name="To'g'ri yechgan savollar soni")
    result = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Natijasi (%)")
    totalScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Umumiy ball")
    intervalTime = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       verbose_name="Interval (daqiqa)")
    createdTime = models.DateTimeField(auto_now_add=True, verbose_name="Natijaga ochilgan sana")

    def __str__(self):
        return f"{self.applicant}: {self.result}"

    class Meta:
        db_table = 'exam_results'
        verbose_name = "Imtihon natijasi"
        verbose_name_plural = "Imtihon natijalari"
