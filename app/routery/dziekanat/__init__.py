from .uzytkownik import router as uzytkownik_router
from .przedmiot import router as przedmiot_router
from .ocena import router as ocena_router
from .grupa import router as grupa_router

dziekanat_router = [
    uzytkownik_router,
    przedmiot_router,
    ocena_router,
    grupa_router
]