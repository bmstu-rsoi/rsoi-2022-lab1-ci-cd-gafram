from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, FileResponse
import psycopg2


app = FastAPI()

conn = psycopg2.connect(dbname='persons', user='program',
                        password='test', host='localhost')


class Person:
    def __init__(self, id, name, age=None, address=None, work=None):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.work = work


def get_person_by_id(id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT Id, Name, Age, Work, Address FROM persons WHERE id = {id}"
        )
        person_data = cur.fetchone()

        return Person(*person_data) if person_data else None


def get_persons_all():
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Id, Name, Age, Work, Address FROM persons"
        )
        person_data = cur.fetchall()

        return [Person(*persons_list[i]) for i in len(person_data)] if person_data else None


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
def post_person():
    pass


@app.patch("/persons/{person_id}")
def patch_person(person_id):
    pass


@app.delete("/persons/{person_id}")
def delete_person():
    pass
