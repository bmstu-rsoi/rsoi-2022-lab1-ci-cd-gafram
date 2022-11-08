from fastapi import FastAPI, status, Body
from fastapi.responses import JSONResponse
import psycopg2
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

conn = psycopg2.connect(dbname='persons', user='program',
                        password='test', host='localhost')


class PersonRes(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None


class PersonReq(BaseModel):
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None


def get_person_by_id(person_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT Id, Name, Age, Work, Address FROM persons WHERE Id = {person_id}"
        )
        person_data = cur.fetchone()

        return PersonRes(*person_data) if person_data else None


def get_persons_all():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Id, Name, Age, Work, Address FROM persons"
        )
        person_data = cur.fetchall()

        return [PersonRes(*persons_list[i]) for i in len(person_data)] if person_data else None


def person_insert(person: PersonReq):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO persons(Name, Age, Work, Address) \
              VALUES ({person.name}, {person.age}, {person.work}, {person.address}) \
              SELECT currval(pg_get_serial_sequence('persons','Id'))"
        )
        conn.commit()
        row = cur.fetchone()
        return row


def person_delete(person_id):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM persons WHERE Id = {person_id}"
        )
        conn.commit()


def person_patch(person_id, person: PersonReq):
    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE person SET Name = {person.name}" +
            f", Age = {person.age}" if person.age else "" +
            f", Address = {person.address}" if person.address else "" +
            f", Work = {person.work}" if person.work else "" +
            f"WHERE Id = {person_id}"
        )
        conn.commit()
    return get_person_by_id(person_id)


@app.get("/persons/{person_id}")
def get_person(person_id: int):
    person = get_person_by_id(person_id)
    if person != None:
        JSONResponse(content=person, status_code=status.HTTP_200_OK)
    else:
        JSONResponse(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/persons")
def get_all_persons():
    persons = get_persons_all()
    if persons != None:
        JSONResponse(content=persons, status_code=status.HTTP_200_OK)


@app.post("/persons")
def post_person(person: PersonReq):
    person_insert(person)


@app.patch("/persons/{person_id}")
def patch_person(person_id, person: PersonReq):
    pass


@app.delete("/persons/{person_id}")
def delete_person(person_id: int):
    person_delete(person_id)
    return JSONResponse(content="", status_code=status.HTTP_204_NO_CONTENT)
