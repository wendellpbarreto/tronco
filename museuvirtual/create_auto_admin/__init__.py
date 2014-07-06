from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.contrib.auth import models as auth_models
from django.conf import settings

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)

def create_admin(app, created_models, verbosity, **kwargs):
    
    usuario = 'admin'
    email = 'admin@museuvirtual.info'
    senha = '(projetoufrn)'
    
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print ""
        print '#' * 80
        print 'Creating admin user -- login: %s, password: %s' %(usuario, senha)
        print '#' * 80
        print ""
        assert auth_models.User.objects.create_superuser(usuario, email, senha)


signals.post_syncdb.connect(
    create_admin,
    sender=auth_models,
    dispatch_uid='apps.auth.models.create_admin'
)
