from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse,JSONResponse,RedirectResponse
from starlette.templating import Jinja2Templates
from db import ( get_all_students,
                    create_a_student,
                    get_a_student_by_id,
                    update_student_data,
                    delete_student_data
)


templates=Jinja2Templates(directory="templates")


# async def index(request:Request):
#     student_id = request.path_params.get("student_id")

#     student_name= request.query_params.get("student_name") or "World"
#     return PlainTextResponse(content=f"Hello {student_name}")

async def json_endpoint(request:Request):
    return JSONResponse(content={"message":"Hello World"})

async def html_endpoint(request:Request):
    student_name="JOHN DOE"


    students=get_all_students()

    context={"request":request,"name":student_name,"students":students}
    return templates.TemplateResponse("index.html",context)


async def create_students(request:Request):

    if request.method == "POST":
        student_data=await request.form()

        create_a_student(student_data)

        return RedirectResponse(request.url_for('html_endpoint'),status_code=303)

    context={"request":request}
    return templates.TemplateResponse("create.html",context)


async def update_a_student(request:Request):
    student_id=request.path_params.get('student_id')

    student_to_update=get_a_student_by_id(student_id)

    if request.method == "POST":
        student_update_data = await request.form()

        update_student_data(student_id,student_update_data)

        return RedirectResponse(request.url_for('html_endpoint'),status_code=303)

    context={"request":request,"student":student_to_update}
    return templates.TemplateResponse("update.html",context)


async def delete_student(request:Request):
    student_id=request.path_params.get('student_id')

    delete_student_data(student_id)

    return RedirectResponse(request.url_for('html_endpoint'),status_code=303)



routes=[
    # Route("/{student_id:int}/",endpoint=index),
    Route('/json',endpoint=json_endpoint),
    Route('/',endpoint=html_endpoint),
    Route('/create_student',endpoint=create_students,methods=["GET","POST"]),
    Route('/update_student/{student_id:int}/',endpoint=update_a_student,
        methods=["GET","POST"]
    ),
    Route('/delete/{student_id:int}/',endpoint=delete_student)
]

app=Starlette(
    debug=True,
    routes=routes
)