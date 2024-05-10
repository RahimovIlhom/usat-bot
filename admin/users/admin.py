from django.contrib import admin

from .models import SimpleUser, DirectionOdEducation, TypeOfEducation, ContractPrice, Applicant, Olympian


class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ['tgId', 'fullname', 'language']
    list_filter = ['language']
    search_fields = ['tgId', 'fullname']


class EducationalAreasAdmin(admin.ModelAdmin):
    list_display = ['id', 'nameUz', 'nameRu']
    search_fields = ['nameUz', 'nameRu']


class TypeOfEducationAdmin(admin.ModelAdmin):
    list_display = ['id', 'nameUz', 'nameRu']
    search_fields = ['nameUz', 'nameRu']


class ContractPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'directionOfEducation', 'typeOfEducation', 'amount']
    list_filter = ['directionOfEducation', 'typeOfEducation']
    search_fields = ['directionOfEducation__nameUz', 'directionOfEducation__nameRu', 'typeOfEducation__nameUz',
                     'typeOfEducation__nameRu', 'amount']


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['tgId', 'phoneNumber', 'pinfl', 'firstName', 'passport', 'directionOfEducation', 'typeOfEducation',
                    'contractFile', 'olympian']
    list_filter = ['directionOfEducation', 'typeOfEducation']
    search_fields = ['tgId', 'phoneNumber', 'pinfl', 'firstName', 'passport', 'lastName', 'middleName', 'contractFile']


class OlympianAdmin(admin.ModelAdmin):
    list_display = ['id', 'applicant', 'result', 'vaucher', 'certificateImage']
    search_fields = ['applicant__tgId', 'applicant__phoneNumber', 'applicant__pinfl', 'applicant__firstName',
                     'applicant__passport', 'applicant__lastName', 'applicant__middleName']


admin.site.register(SimpleUser, SimpleUserAdmin)
admin.site.register(DirectionOdEducation, EducationalAreasAdmin)
admin.site.register(TypeOfEducation, TypeOfEducationAdmin)
admin.site.register(ContractPrice, ContractPriceAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Olympian, OlympianAdmin)
