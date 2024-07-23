from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)


class SimpleUser(models.Model):
    tgId = models.BigIntegerField(primary_key=True, verbose_name="Telegram id")
    fullname = models.CharField(max_length=255, null=True, verbose_name="Ism-familiya")
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name="Til")

    def __str__(self):
        return f"{self.tgId} {self.fullname}"

    class Meta:
        db_table = 'simple_users'
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class DirectionOfEducation(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name="Qabul jadvalidagi ID")
    nameUz = models.CharField(max_length=255, verbose_name="Ta'lim yo'nalishi nomi uz")
    nameRu = models.CharField(max_length=255, verbose_name="Ta'lim yo'nalishi ru")
    sciences = models.ManyToManyField('Science', blank=True, verbose_name="Imtihon fanlari")
    active = models.BooleanField(default=True, verbose_name="Ta'lim yo'nalishi aktivligi")
    deleted = models.BooleanField(default=False, verbose_name="O'chirilganmi?")

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'educational_areas'
        verbose_name = "Ta'lim yo'nalishi"
        verbose_name_plural = "Ta'lim yo'nalishlari"


class TypeOfEducation(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name="Qabul jadvalidagi ID")
    nameUz = models.CharField(max_length=255, verbose_name="Ta'lim turi nomi uz")
    nameRu = models.CharField(max_length=255, verbose_name="Ta'lim turi nomi ru")
    active = models.BooleanField(default=True, verbose_name="Ta'lim turi aktivligi")
    deleted = models.BooleanField(default=False, verbose_name="O'chirilganmi?")

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'types_of_education'
        verbose_name = "Ta'lim turi"
        verbose_name_plural = "Ta'lim turlari"


class ContractPrice(models.Model):
    directionOfEducation = models.ForeignKey(DirectionOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='contract_price', verbose_name="Fakultet")
    typeOfEducation = models.ForeignKey(TypeOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="contract_price", verbose_name="Ta'lim turi")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kontrakt miqdori")

    def __str__(self):
        return f"{self.directionOfEducation}, {self.typeOfEducation} - {self.amount}"

    class Meta:
        db_table = 'contract_prices'
        verbose_name = "Kontrakt miqdori"
        verbose_name_plural = "Kontrakt miqdorlari"


APPLICATION_STATUS = (
    ('DRAFT', 'QORALAMA'),
    ('SUBMITTED', 'ARIZA YUBORILDI'),
    ('REJECTED', 'ARIZA RAD ETILDI'),
    ('ACCEPTED', 'ARIZA QABUL QILINDI'),
    ('EXAMINED', 'IMTIHON TOPSHIRDI'),
    ('FAILED', 'IMTIHON MUVAFFAQIYATSIZ'),
    ('PASSED', 'IMTHONDAN MUVAFFAQIYATLI O\'TDI'),
)

GENDER_STATUS = (
    ('MALE', 'Erkak'),
    ('FEMALE', 'Ayol'),
)


class Applicant(models.Model):
    applicantId = models.IntegerField(null=True, blank=True, verbose_name="Arizachi ID")
    applicantNumber = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ariza raqami")
    tgId = models.BigIntegerField(primary_key=True, verbose_name="Telegram id")
    phoneNumber = models.CharField(max_length=255, unique=True, verbose_name="Telefon raqami")
    additionalPhoneNumber = models.CharField(max_length=255, unique=True, null=True, blank=True,
                                             verbose_name="Qo'shimcha telefon raqami")
    passport = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Pasport seriya va raqami")
    birthDate = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tug'ilgan sanasi")
    pinfl = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Pinfl")
    firstName = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ismi")
    lastName = models.CharField(max_length=255, null=True, blank=True, verbose_name="Familiyasi")
    middleName = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sha'rifi")
    passportImageFront = models.ImageField(max_length=255, upload_to='passport/images/front/', null=True, blank=True,
                                           verbose_name="Pasport old rasmi")
    passportImageBack = models.ImageField(max_length=255, upload_to='passport/images/back/', null=True, blank=True,
                                          verbose_name="Pasport orqa rasmi")
    dtmScore = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2, verbose_name="DTM natijasi")
    dtmAbiturientNumber = models.CharField(max_length=255, null=True, blank=True, verbose_name="DTM abituriyent raqami")
    birthPlace = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tug'ilgan joyi")
    birthCountry = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tug'ilgan davlati")
    nationality = models.CharField(max_length=255, null=True, blank=True, verbose_name="Millati")
    citizenship = models.CharField(max_length=255, null=True, blank=True, verbose_name="Fuqaroligi")
    regionId = models.IntegerField(null=True, blank=True, verbose_name="Viloyat ID")
    regionName = models.CharField(max_length=100, null=True, blank=True, verbose_name="Viloyat nomi")
    cityId = models.IntegerField(null=True, blank=True, verbose_name="Tuman ID")
    cityName = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tuman nomi")
    gender = models.CharField(max_length=6, choices=GENDER_STATUS, null=True, blank=True, verbose_name="Jinsi")
    photo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Rasmi")
    directionOfEducation = models.ForeignKey(DirectionOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                             related_name='applicants', verbose_name="Ta'lim yo'nalishi")
    typeOfEducation = models.ForeignKey(TypeOfEducation, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='applicants', verbose_name="Ta'lim turi")
    languageOfEducation = models.CharField(max_length=2, choices=LANGUAGES, default='uz', null=True, blank=True,
                                           verbose_name="Ta'lim tili")
    contractFile = models.CharField(max_length=255, null=True, blank=True, verbose_name="Kontrakt shartnomasi")
    olympian = models.BooleanField(default=False, verbose_name="Olimpiadachimi?")
    applicationStatus = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='DRAFT',
                                         verbose_name="Arizachi holati")
    createdTime = models.DateTimeField(auto_now_add=True, verbose_name="Ariza yuborilgan sana")
    updatedTime = models.DateTimeField(auto_now=True, verbose_name="Oxirgi o'zgarish sanasi")

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.pinfl}"

    class Meta:
        db_table = 'applicants'
        ordering = ['-createdTime']
        verbose_name = "Arizachi"
        verbose_name_plural = "Arizachilar"


class Olympian(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='olympian_user',
                                  verbose_name="Arizachi")
    result = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2, verbose_name="Imtihon natijasi")
    vaucher = models.BigIntegerField(default=0, verbose_name="Vaucheri")
    certificateImage = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sertifikati")

    def __str__(self):
        return f"{self.applicant} -> {self.vaucher}"

    class Meta:
        db_table = 'olympians'
        verbose_name = "Olimpiadachi"
        verbose_name_plural = "Olimpiadachilar"


class Science(models.Model):
    nameUz = models.CharField(max_length=255, verbose_name="Fan nomi uz")
    nameRu = models.CharField(max_length=255, verbose_name="Fan nomi ru")
    deleted = models.BooleanField(default=False, verbose_name="Fan o'chirilganmi?")

    def __str__(self):
        return f"{self.nameUz}"

    class Meta:
        db_table = 'sciences'
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
