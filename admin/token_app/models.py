from django.db import models


class AdmissionToken(models.Model):
    token = models.CharField(max_length=255, verbose_name="Token")
    isActive = models.BooleanField(default=False, verbose_name="Token ishlaydimi?")
    createdTime = models.DateTimeField(auto_now_add=True, verbose_name='Token olingan vaqt')
    updatedTime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Token eskirgan vaqt")

    def __str__(self):
        return self.token

    class Meta:
        ordering = ['-createdTime']
        db_table = 'tokens'
        verbose_name = "Token"
        verbose_name_plural = "Tokenlar"
