from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
  
class UserAccountManager(BaseUserManager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
          
        user = self.model(
            email = self.normalize_email(email) , 
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def create_superuser(self , email , password):
        user = self.create_user(
            email = self.normalize_email(email) , 
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_student = False
        user.save(using = self._db)
        return user
      
class UserAccount(AbstractBaseUser):
    class Types(models.TextChoices):
        STUDENT = "STUDENT" , "student"
        FACULTY = "FACULTY" , "faculty"
        STAFF_LIB ="STAFF_LIB", 'staff_lib'
        STAFF_MED ="STAFF_MED", "staff_med"

          
    type = models.CharField(max_length = 20 , choices = Types.choices , 
                            # Default is user is student
                            default = Types.FACULTY)
    email = models.EmailField(max_length = 200 , unique = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
      
    # special permission which define that
    # the new user is teacher or student 
    is_student = models.BooleanField(default = False)
    is_faculty = models.BooleanField(default = False)
    is_staff_med = models.BooleanField(default = False)
    is_staff_lib = models.BooleanField(default = False)
      
    USERNAME_FIELD = "email"
      
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
      
    def __str__(self):
        return str(self.email)
      
    def has_perm(self , perm, obj = None):
        return self.is_admin
      
    def has_module_perms(self , app_label):
        return True
      
    def save(self , *args , **kwargs):
        if not self.type or self.type == None : 
            self.type = UserAccount.Types.STUDENT
        return super().save(*args , **kwargs)



class StudentManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.STUDENT)
        return queryset    
        
class Student(UserAccount):
    class Meta : 
        proxy = True
    objects = StudentManager()
      

    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.STUDENT
        self.is_student = True
        return super().save(*args , **kwargs)

class FacultyManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.FACULTY)
        return queryset    
        
class Faculty(UserAccount):
    class Meta : 
        proxy = True
    objects = FacultyManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.FACULTY
        self.is_faculty = True
        return super().save(*args , **kwargs)


class StaffMedManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.STAFF_MED)
        return queryset    
        
class StaffMed(UserAccount):
    class Meta : 
        proxy = True
    objects =StaffMedManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.STAFF_MED
        self.is_staff_med = True
        return super().save(*args , **kwargs)

class StaffLibManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.STAFF_LIB)
        return queryset    
        
class StaffLib(UserAccount):
    class Meta : 
        proxy = True
    objects =StaffLibManager()
      
    def save(self , *args , **kwargs):
        self.type = UserAccount.Types.STAFF_LIB
        self.is_staff_lib = True
        return super().save(*args , **kwargs)