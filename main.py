from ariadne import QueryType, ObjectType, gql
from ariadne import make_executable_schema
from ariadne.resolvers import GraphQLResolveInfo
from fastapi import FastAPI
from ariadne.asgi import GraphQL


type_defs = gql("""
    type Query {
        ping: String!
        article: Article!
    }

    type Article {
        title: String!
        content: String!
    }
""")

query = QueryType()
article = ObjectType("Article")


@query.field("ping")
def resolve_ping(_, info: GraphQLResolveInfo):
    """Used for health checks."""
    return "pong"


@query.field("article")
def resolve_article(_, info: GraphQLResolveInfo):
    return "article"


@article.field("title")
def resolve_title(_, info: GraphQLResolveInfo):
    return "First Post"


@article.field("content")
def resolve_title(_, info: GraphQLResolveInfo):
    return "Some article content"


schema = make_executable_schema(type_defs, query, article)

app = FastAPI()
app.add_route("/", GraphQL(schema=schema, debug=True))
