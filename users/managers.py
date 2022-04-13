from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where login is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, login, password, **extra_fields):
        if not login:
            raise ValueError('The Login must be set')
        user = self.model(
            login=login,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, password, **extra_fields):
        """
        Create and save a SuperUser with the given login and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(login, password, **extra_fields)

    def update_user(self, user, **extra_fields):
        if not extra_fields.get('login'):
            raise ValueError('The Login must be set')
        user.login = extra_fields.get('login')
        user.name = extra_fields.get('name')
        user.email = extra_fields.get('email')
        user.set_password(extra_fields.get('password'))
        user.save()
        return user
