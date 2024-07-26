from pony.orm import set_sql_debug
from pony.orm import Database, Required, Optional, Set

db = Database()


class Person(db.Entity):
    name = Required(str)
    contact_info = Required(str)
    cases = Set("CasePerson")


class Case(db.Entity):
    number = Required(str)
    jurisdiction = Required(str)
    documents = Set("Document")
    people = Set("CasePerson")


class Document(db.Entity):
    creation_date = Required(str)
    text = Required(str)
    title = Required(str)
    type = Required(str)
    status = Required(str)
    case = Required(Case)


class CasePerson(db.Entity):
    role = Required(str)
    case = Required(Case)
    person = Required(Person)


def init_db(filename=":sharedmemory:", debug=True):
    set_sql_debug(debug)
    db.bind(provider="sqlite", filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)

