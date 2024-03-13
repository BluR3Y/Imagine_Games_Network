from django.urls import path
from graphene_django.views import GraphQLView
from . import views
from videos.schema import schema

# URLConf
urlpatterns = [
    path('tester/', views.tester),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema))
]