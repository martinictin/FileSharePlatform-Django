from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.timezone import now

# Create your models here.


class KorisniciManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        #user_obj.Roles = Uloge.Titula
        user_obj.save(using=self._db)
        return user_obj
    
class Uloge(models.Model):
    
    class TitulaClass(models.TextChoices):
            ADMINISTRATOR = 'Administrator', _('Administrator')
            PROFESOR = 'Profesor', _('Profesor')
            STUDENT = 'Student', _('Student')
            
    Titula = models.CharField(
    max_length=15,
    choices=TitulaClass.choices,
    default=TitulaClass.STUDENT,
)
    def __str__(self):
        return self.Titula
    
class Korisnici(AbstractBaseUser):
    Email = models.EmailField(max_length=255, unique=True, default="test@test.com")
    
    Role = models.ForeignKey(Uloge, on_delete=models.CASCADE)
    
    
    USERNAME_FIELD = 'Email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = KorisniciManager()
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.Email
    
    def get_roles(self):
        return self.Role
    
    
class Dokumenti(models.Model):
    Naslov = models.CharField(max_length=255)
    Dokument = models.FileField(upload_to='documents/')
    Vrijeme = models.DateTimeField(default=datetime.now, blank=True)
    Kreator = models.ForeignKey(Korisnici,on_delete=models.CASCADE,null=True,related_name="Kreator")
    Korisnik = models.ManyToManyField(Korisnici,through='Student_Dokument',related_name="Korisnik")
    Azuriran = models.DateTimeField(default=datetime.now,blank=True)
    
    def __str__(self):
        return self.Naslov
    
    def get_kreator(self):
        return self.Kreator
    
    
    


class Student_Dokument(models.Model):

    class Meta:
        unique_together = (('StudentID', 'DokumentID'),)

    DokumentID = models.ForeignKey(Dokumenti, on_delete=models.CASCADE)
    StudentID = models.ForeignKey(Korisnici, on_delete=models.CASCADE)

    def get_studentID(self):
        return self.StudentID
    
    def get_dokumentID(self):
        return self.DokumentID
    

