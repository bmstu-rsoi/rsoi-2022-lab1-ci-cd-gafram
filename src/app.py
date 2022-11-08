from fastapi import FastAPI, status, Body
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
import psycopg2
from pydantic.dataclasses import dataclass
from typing import Optional, Union
import json
from pydantic.json import pydantic_encoder


app = FastAPI()

conn = psycopg2.connect(dbname='persons', user='program',
                        password='test', host='localhost')


@dataclass
class PersonRes:
    id: int
    name: str
    age: Optional[int] = None
    work: Optional[str] = None
    address: Optional[str] = None


@dataclass
class PersonReq:
    name: str
    age: Optional[int] = None
    work: Optional[str] = None
    address: Optional[str] = None


def get_person_by_id(person_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT \"Id\", \"Name\", \"Age\", \"Work\", \"Address\" FROM persons WHERE \"Id\" = \'{person_id}\'"
        )
        person_data = cur.fetchone()
        return PersonRes(*person_data) if person_data else None


def get_persons_all():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT \"Id\", \"Name\", \"Age\", \"Work\", \"Address\" FROM persons"
        )
        persons_data = cur.fetchall()

        return [PersonRes(*persons_data[i]) for i in range(len(persons_data))] if persons_data else None


def person_insert(person: PersonReq):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO persons(\"Id\", \"Name\", \"Age\", \"Work\", \"Address\") \
              VALUES (DEFAULT, \'{person.name}\', {person.age}, \'{person.work}\', \'{person.address}\') \
              RETURNING \"Id\";"
        )
        conn.commit()
        row = cur.fetchone()
        return row[0]


def person_delete(person_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM persons WHERE \"Id\" = \'{person_id}\'"
        )
        conn.commit()


def person_patch(person_id, person: PersonReq):
    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE persons SET \"Name\" = \'{person.name}\'" +
            (f", \"Age\" = \'{person.age}\'" if person.age else "") +
            (f", \"Address\" = \'{person.address}\'" if person.address else "") +
            (f", \"Work\" = \'{person.work}\'" if person.work else "") +
            (f"WHERE \"Id\" = \'{person_id}\'")
        )
        conn.commit()
    return get_person_by_id(person_id)


@app.get("/api/v1/persons/{person_id}")
def get_person(person_id: int):
    person = get_person_by_id(person_id)
    if person != None:
        content = json.dumps(person,
                             default=pydantic_encoder)
        headers = {'Content-Type': 'application/json'}
        return Response(content=content,
                        headers=headers,
                        status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content="Not found Person for ID",
                            status_code=status.HTTP_404_NOT_FOUND)


@app.get("/api/v1/persons")
def get_all_persons():
    persons = get_persons_all()
    if persons != None:
        content = json.dumps(persons, default=pydantic_encoder)
        headers = {'Content-Type': 'application/json'}
        return Response(content=content,
                        headers=headers,
                        status_code=status.HTTP_200_OK)


@app.post("/api/v1/persons")
def post_person(person: PersonReq):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(content="Invalid data",
                            status_code=status.HTTP_400_BAD_REQUEST)

    new_person_id = person_insert(person)
    headers = {'Location': f'/api/v1/persons/{new_person_id}'}
    return JSONResponse(content="Created new person",
                        headers=headers,
                        status_code=status.HTTP_201_CREATED)


@ app.patch("/api/v1/persons/{person_id}")
def patch_person(person_id: int, person: PersonReq):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(content="Invalid data",
                            status_code=status.HTTP_400_BAD_REQUEST)

    person_by_id = get_person_by_id(person_id)

    if person_by_id != None:
        person = person_patch(person_id, person)
        content = json.dumps(person, default=pydantic_encoder)
        headers = {'Content-Type': 'application/json'}
        return Response(content=content,
                        headers=headers,
                        status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@ app.delete("/api/v1/persons/{person_id}")
def delete_person(person_id: int):
    person_delete(person_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
