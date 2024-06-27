from typing import Type

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import BaseSerializer

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


# Create your views here.
class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """

    queryset: QuerySet[Snippet] = Snippet.objects.all()
    serializer_class: Type[BaseSerializer] = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: SnippetSerializer) -> None:
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    queryset: QuerySet[Snippet] = Snippet.objects.all()
    serializer_class: Type[BaseSerializer] = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset: QuerySet[User] = User.objects.all()
    serializer_class: Type[BaseSerializer] = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset: QuerySet[User] = User.objects.all()
    serializer_class: Type[BaseSerializer] = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request: Request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
