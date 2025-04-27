from .auth import router as auth_router
from .ai import router as ai_router
from .help import router as help_router
from .personalization import router as personalization_router
from .points import router as points_router

routers = [
    auth_router,
    ai_router,
    help_router,
    personalization_router,
    points_router
]