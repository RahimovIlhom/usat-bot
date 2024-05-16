from django.db import models


LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)


class SimpleUser(models.Model):
    tgId = models.BigIntegerField(primary_key=True)
    fullname = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)

    def __str__(self):
        return f"{self.tgId} {self.fullname}"

    class Meta:
        db_table = 'simple_users'


class DirectionOdEducation(models.Model):
    nameUz = models.CharField(max_length=255)
    nameRu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'educational_areas'


class TypeOfEducation(models.Model):
    nameUz = models.CharField(max_length=255)
    nameRu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'types_of_education'


class ContractPrice(models.Model):
    directionOfEducation = models.ForeignKey(DirectionOdEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='contract_price')
    typeOfEducation = models.ForeignKey(TypeOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="contract_price")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.directionOfEducation}, {self.typeOfEducation} - {self.amount}"

    class Meta:
        db_table = 'contract_prices'


APPLICATION_STATUS = (
    ('DRAFT', 'DRAFT'),
    ('SUBMITTED', 'SUBMITTED'),
    ('REJECTED', 'REJECTED'),
    ('ACCEPTED', 'ACCEPTED'),
    ('PASSED', 'PASSED'),
    ('FAILED', 'FAILED'),
    ('EXAMINED', 'EXAMINED'),
)


class Applicant(models.Model):
    tgId = models.BigIntegerField(primary_key=True)
    phoneNumber = models.CharField(max_length=20, unique=True)
    pinfl = models.CharField(max_length=14, unique=True)
    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    middleName = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(max_length=20, null=True, blank=True, unique=True)
    directionOfEducation = models.ForeignKey(DirectionOdEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='applicants')
    typeOfEducation = models.ForeignKey(TypeOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='applicants')
    languageOfEducation = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    contractFile = models.CharField(max_length=255, null=True, blank=True)
    olympian = models.BooleanField(default=False)
    applicationStatus = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='DRAFT')
    createdTime = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.pinfl}"

    class Meta:
        db_table = 'applicants'


class Olympian(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='olympian_user')
    result = models.DecimalField(max_digits=5, decimal_places=2)
    vaucher = models.BigIntegerField(default=0)
    certificateImage = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.applicant} -> {self.vaucher}"

    class Meta:
        db_table = 'olympians'
