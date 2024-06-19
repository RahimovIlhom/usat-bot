from django.contrib import admin

from .models import SimpleUser, DirectionOfEducation, TypeOfEducation, ContractPrice, Applicant, Olympian


class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ['tgId', 'fullname', 'language']
    list_filter = ['language']
    search_fields = ['tgId', 'fullname']


class EducationalAreasAdmin(admin.ModelAdmin):
    list_display = ['nameUz', 'nameRu', 'active']
    search_fields = ['nameUz', 'nameRu']


class TypeOfEducationAdmin(admin.ModelAdmin):
    list_display = ['nameUz', 'nameRu', 'active']
    search_fields = ['nameUz', 'nameRu']


class ContractPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'directionOfEducation', 'typeOfEducation', 'amount']
    list_filter = ['directionOfEducation', 'typeOfEducation']
    search_fields = ['directionOfEducation__nameUz', 'directionOfEducation__nameRu', 'typeOfEducation__nameUz',
                     'typeOfEducation__nameRu', 'amount']


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['passport', 'birthDate', 'firstName', 'directionOfEducation', 'typeOfEducation',
                    'olympian', 'applicationStatus']
    list_filter = ['directionOfEducation', 'typeOfEducation', 'applicationStatus']
    search_fields = ['tgId', 'phoneNumber', 'pinfl', 'firstName', 'passport', 'lastName', 'middleName', 'contractFile']


class OlympianAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'result', 'vaucher', 'certificateImage']
    search_fields = ['applicant__tgId', 'applicant__phoneNumber', 'applicant__pinfl', 'applicant__firstName',
                     'applicant__passport', 'applicant__lastName', 'applicant__middleName']


admin.site.register(SimpleUser, SimpleUserAdmin)
admin.site.register(DirectionOfEducation, EducationalAreasAdmin)
admin.site.register(TypeOfEducation, TypeOfEducationAdmin)
admin.site.register(ContractPrice, ContractPriceAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Olympian, OlympianAdmin)
