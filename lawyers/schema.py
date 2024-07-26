from typing import List, Optional
from datetime import datetime

import strawberry
from pony.orm import db_session
from pony.orm.core import ObjectNotFound

from models import Person, Case, Document, CasePerson

@strawberry.type
class PersonType:
    id: strawberry.ID
    name: str
    contact_info: str

    @classmethod
    def marshall(cls, person: Person):
        return cls(
            id=str(person.id), name=person.name, contact_info=person.contact_info
        )


@strawberry.type
class BaseCaseType:
    id: strawberry.ID
    number: str
    jurisdiction: str

    @classmethod
    def marshall(cls, case: Case):
        return cls(id=str(case.id), number=case.number, jurisdiction=case.jurisdiction)


@strawberry.type
class DocumentType:
    id: strawberry.ID
    case: BaseCaseType
    creation_date: str
    text: str
    title: str
    type: str
    status: str

    @classmethod
    def marshall(cls, document: Document):
        return cls(
            id=str(document.id),
            case=document.case,
            creation_date=document.creation_date,
            text=document.text,
            title=document.title,
            type=document.type,
            status=document.status,
        )


@strawberry.type
class CasePersonType:
    id: strawberry.ID
    role: str
    case: BaseCaseType
    person: PersonType

    @classmethod
    def marshall(cls, case_person: CasePerson):
        return cls(
            id=str(case_person.id),
            role=case_person.role,
            case=case_person.case,
            person=case_person.person,
        )


@strawberry.type
class CaseType(BaseCaseType):
    @strawberry.field
    def documents(self) -> list[DocumentType]:
        with db_session:
            return [
                DocumentType.marshall(document) for document in Case[self.id].documents
            ]


@strawberry.type
class Query:
    @strawberry.field
    def all_people(self) -> list[PersonType]:
        with db_session:
            return [PersonType.marshall(person) for person in Person.select()]

    @strawberry.field
    def all_cases(self) -> list[CaseType]:
        with db_session:
            return [CaseType.marshall(case) for case in Case.select()]

    @strawberry.field
    def all_documents(self) -> list[DocumentType]:
        with db_session:
            return [DocumentType.marshall(document) for document in Document.select()]

    @strawberry.field
    def get_case(
        self, case_id: Optional[str] = strawberry.UNSET
    ) -> Optional["CaseType"]:
        with db_session:
            try:
                case = Case[case_id]
                return CaseType.marshall(case)
            except ObjectNotFound:
                raise Exception("Not Found")

    @strawberry.field
    def get_person(
        self, person_id: Optional[str] = strawberry.UNSET
    ) -> Optional["PersonType"]:
        with db_session:
            try:
                p = Person[person_id]
                return PersonType.marshall(p)
            except ObjectNotFound:
                raise Exception("Not Found")


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_person(self, name: str, contact_info: str) -> PersonType:
        with db_session:
            p = Person(name=name, contact_info=contact_info)
        return PersonType.marshall(p)

    @strawberry.mutation
    def add_case(self, number: str, jurisdiction: str) -> CaseType:
        with db_session:
            case = Case(number=number, jurisdiction=jurisdiction)
        return CaseType.marshall(case)

    @strawberry.mutation
    def add_document(
        self, case_id: str, text: str, title: str, type: str, status: str
    ) -> DocumentType:
        with db_session:
            try:
                case = Case[str(case_id)]
            except ObjectNotFound:
                raise Exception("Not Found")

            document = Document(
                case=case,
                creation_date=datetime.now().isoformat(),
                text=text,
                title=title,
                type=type,
                status=status,
            )

        return DocumentType.marshall(document)
