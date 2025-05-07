from .grupa import router as grupa_router
from .ocena import router as ocena_router
from .ja import router as ja_router

student_router =[
    grupa_router,
    ocena_router,
    ja_router
]