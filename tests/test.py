import pytest
from fastapi.testclient import TestClient

import sys
sys.path.append("lawyers")

from pony.orm import db_session, select

from main import app   # noqa


@pytest.fixture(scope="function")
def client():
    from models import db, Person, Case, Document, CasePerson, init_db
    # Setup the database and create tables

    client = TestClient(app)
    response = client.get("/health")
    with db_session:
        # Add some initial data
        person = Person(name="John Doe", contact_info="john@example.com")
        case = Case(number="12345", jurisdiction="NY")
        document = Document(creation_date="2024-07-25", text="Document text", title="Document title", type="Type A", status="Draft", case=case)
        case_person = CasePerson(role="Lawyer", case=case, person=person)
    yield client
    # Teardown the database
    db.drop_all_tables(with_all_data=True)


def test_all_people(client):
    query = """
    query {
        allPeople {
            id
            name
            contactInfo
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert len(data["data"]["allPeople"]) == 1

def test_all_cases(client):
    query = """
    query {
        allCases {
            id
            number
            jurisdiction
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert len(data["data"]["allCases"]) == 1
