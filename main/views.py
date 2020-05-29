from django.shortcuts import render
from rest_framework import viewsets
from main.serializer import UsuarioSerializer
from main.models import Usuario
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.generics import ListAPIView 


class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class MinhaPermissao(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.method)

        if request.method == 'POST':
            return request.user.is_authenticated

        elif request.method == 'GET':
            return True

        else:
            return False

        if request.user.is_authenticated:
            return True


class UsuarioListView(ListAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        usuarios = Usuario.objects.all()
        page = self.paginate_queryset(usuarios)
        if page is not None:
            serializer = UsuarioSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = UsuarioSerializer(usuarios, many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request, format=None):
        print(type(request.data['data_nasc']))
        print(request.data)
        new_dict = {
            'nome': request.data['nome_completo'].split(' ')[0],
            'sobrenome': request.data['nome_completo'].split(' ')[1],
            'data_nasc': request.data['data_nasc'] if 'data_nasc' in request.data else '1900-01-01',
            'is_admin': request.data['is_admin'],
        }
        print(new_dict)
        serializer = UsuarioSerializer(data=new_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def _get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        usuario = self._get_object(pk)
        serializer = UsuarioSerializer(usuario, context={'request': request})

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print(request.data)
        usuario = self._get_object(pk)
        deserializer = UsuarioSerializer(usuario, data=request.data, context={'request': request})

        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_202_ACCEPTED)
        else:   
            return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        usuario = self._get_object(pk)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



