# import User_Type
from app.models.tcc_model import User_Type


def get_user_type(email):
    teacher_email = "computacao.ufcg.edu.br"
    student_email = "ccc.ufcg.edu.br"

    # if email.endswith(teacher_email):
    #     return User_Type.Teacher
    # elif email.endswith(student_email):
    #     return User_Type.Student
    # else:
    #     return None

    if email.endswith(teacher_email):
        return User_Type.Student
    elif email.endswith(student_email):
        return User_Type.Teacher
    else:
        return None
