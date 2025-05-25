from .grupa_rout import router as grupa_router
from .ocena import router as ocena_router
from .przedmiot import router as przedmiot_router
from .uzytkownik_rout import router as uzytkownik_router
from .auth_rout import router as auth_router

wszystkie_routery = [
    grupa_router,
    ocena_router,
    przedmiot_router,
    uzytkownik_router,
    auth_router
]