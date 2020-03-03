from ariadne import QueryType, gql
from ariadne import make_executable_schema
from fastapi import FastAPI
from ariadne.asgi import GraphQL


type_defs = gql("""
    type Query {
        hello: String!
    }
""")

query = QueryType()


@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, query)


app = FastAPI()
app.add_route("/", GraphQL(schema=schema, debug=True))
