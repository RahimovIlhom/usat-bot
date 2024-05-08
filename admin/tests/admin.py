from django.contrib import admin


from .models import Science, Test, Question, ExamResult


class ScienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'nameUz', 'nameRu']
    search_fields = ['nameUz', 'nameRu']


class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'directionOfEducation', 'science', 'questionsCount', 'language', 'isActive']
    list_filter = ['directionOfEducation', 'science', 'language']
    search_fields = ['directionOfEducation__nameUz', 'directionOfEducation__nameRu', 'science__nameUz',
                     'science__nameRu', 'questionsCount', 'language']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'test', 'trueResponse']
    search_fields = ['test__pk', 'image', 'question', 'trueResponse']


class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'applicant', 'result']
    search_fields = ['applicant__tgId', 'applicant__phoneNumber', 'applicant__pinfl', 'applicant__firstName',
                     'applicant__passport', 'applicant__lastName', 'applicant__middleName', 'result']


admin.site.register(Science, ScienceAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
