from django.db import models
from datetime import datetime


class Usuario(models.Model):

    nome = models.CharField('Nome', max_length=2000)
    sobrenome = models.CharField('Sobrenome', max_length=2000)
    data_nasc = models.DateField('Data de Nascimento')
    is_admin = models.BooleanField('Admin', default=False)

    @property
    def idade(self):
        delta = datetime.now().date() - self.data_nasc
        return int(delta.days / 365.25)