from rest_framework import serializers
from main.models import Usuario

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Usuario
        fields = ['url', 'id', 'nome', 'sobrenome', 'data_nasc', 'idade', 'is_admin']