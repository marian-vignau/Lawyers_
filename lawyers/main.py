import os
import logging
from pony.orm.core import ERDiagramError, BindingError
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import Query, Mutation
import strawberry
from dotenv import load_dotenv

from models import init_db, db

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Application"),
    version=os.getenv("APP_VERSION", "0.1.0")
)
init_db(filename=os.getenv("DATABASE_URL",":sharedmemory:"))

@app.get("/health")
async def health_check():
    for i in range(2):
        error = ""
        try:
            db.check_tables()
            return {"status": "ok"}
        except Exception as e:
            db.create_tables()
            error = str(e)
        finally:
            if error:
                logger.warning(f"Error init_db {error}")
    return {"status": str(e)}

# Create the Strawberry schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema, graphql_ide="apollo-sandbox")

# Mount the GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")
