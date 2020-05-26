from rest_framework import serializers
from main.models import Usuario

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'sobrenome', 'idade', 'is_admin']