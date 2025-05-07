from .dziekanat import dziekanat_router
from .wykladowca import wykladowca_router
from .student import student_router

wszystkie_routery = [
    dziekanat_router,
    wykladowca_router,
    student_router
]