from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Users sign in with their university email (auth.html's `email` field), not a username."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('University email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Backs the identity shown in the sidebar footer ({{ userInitial }}, {{ userName }},
    {{ role }}) and the auth screen's role tabs (authTabs → 'student' | 'teacher' | 'admin').
    """

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    # Student-only display field — e.g. "B.S. Computer Science · Sophomore",
    # shown as {{ studentProgram }} on the results screen and {{ s.program }}
    # in the teacher/admin student lists.
    program = models.CharField(max_length=120, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def initials(self):
        parts = [p for p in self.get_full_name().split(' ') if p]
        return ''.join(p[0] for p in parts[:2]).upper() or self.email[0].upper()


class StudentProfile(models.Model):
    """
    One-time onboarding survey answers, collected right after a student's
    first login and before they can start any assessment. `completed_at`
    null means the survey hasn't been submitted yet (see
    accounts.permissions.HasCompletedProfile).
    """

    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    faculty = models.CharField(max_length=150)
    course = models.CharField(max_length=150)
    group = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} profile'
