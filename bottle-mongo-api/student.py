import json

from bottle import post, get, delete, put, request, HTTPResponse
from bson.objectid import ObjectId

from models import Student


@post('/student')
def create():
    jstudent = request.json
    name = jstudent.get("name")
    last_name = jstudent.get("last_name")
    if not (name and last_name):
        return HTTPResponse({"error": "One or some required Parameters missing"},
						content_type="application/json", status=422)
    student = Student()
    student.name = name
    student.last_name = last_name
    student.level = jstudent.get('level')
    if(jstudent.get('specialty')):
        student.specialty = jstudent.get('specialty')
    student.save()
    result = {"student": str(student.id)}
    return HTTPResponse(result,
						content_type="application/json", status=201)

@get('/student')
def list_students():
    students = Student.objects.all()
    jstudents = []
    for student in students:
        jstudent = {"id": str(student.id),
                    "name": student.name,
                    "last_name": student.last_name,
                    "level": student.level,
                    "specialty": student.specialty}
        jstudents.append(jstudent)
    result = json.dumps(jstudents)
    return HTTPResponse(result,
						content_type="application/json", status=200)

@get('/student/:id')
def get_student(id):
    student = Student.objects.with_id(ObjectId(id))
    if(student):
        jstudent = {"id": str(student.id),
                    "name": student.name,
                    "last_name": student.last_name,
                    "level": student.level,
                    "specialty": student.specialty}
        result = json.dumps(jstudent)
    else:
        return HTTPResponse("Student does not exist",
                            content_type="application/json", status=404)
    return HTTPResponse(result, content_type="application/json", status=200)
    
@delete('/student/:id')
def delete_student(id):
    student = Student.objects.with_id(ObjectId(id))
    if(student):
        student.delete()
    else:
        return HTTPResponse("Student does not exist",
                            content_type="application/json", status=404)
    return HTTPResponse(content_type="application/json", status=204)   

@put('/student/:id')
def delete_student(id):
    student = Student.objects.with_id(ObjectId(id))
    if(student):
        jstudent = request.json
        name = jstudent.get("name")
        last_name = jstudent.get("last_name")
        if(name):
            student.name = name
        if(last_name):
            student.last_name = last_name
        student.save()
        jstudent = {"id": str(student.id),
                    "name": student.name,
                    "last_name": student.last_name,
                    "level": student.level,
                    "specialty": student.specialty}
    else:
        return HTTPResponse("Student does not exist",
                            content_type="application/json", status=404)
    return HTTPResponse(json.dumps(jstudent), content_type="application/json", status=200)
