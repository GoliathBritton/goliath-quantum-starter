"""
GraphQL Integration Scaffold
"""
from fastapi import APIRouter
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, Quantum World!")

schema = graphene.Schema(query=Query)

graphql_router = APIRouter()

graphql_router.add_route("/graphql", GraphQLApp(schema=schema), methods=["GET", "POST"])

graphql_router.add_route("/graphiql", make_graphiql_handler(), methods=["GET"])
