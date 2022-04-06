from database import Session,engine
from models import Student

local_session=Session(bind=engine)


def get_all_students():
    return local_session.query(Student).all()


def create_a_student(student_data):

    new_student=Student(**student_data)

    try:
        local_session.add(new_student)
        local_session.commit()

    except:
        local_session.rollback()
    finally:
        local_session.close()


def get_a_student_by_id(student_id):
    return local_session.query(Student).filter_by(id=student_id).first()


def update_student_data(student_id,student_data):
    student_to_update=get_a_student_by_id(student_id)

    student_to_update.name = student_data["name"]
    student_to_update.age =student_data["age"]
    student_to_update.registration_no = student_data["registration_no"]

    local_session.commit()


def delete_student_data(student_id):
    student_to_delete=get_a_student_by_id(student_id)

    local_session.delete(student_to_delete)

    local_session.commit()