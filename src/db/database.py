from src.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "contact": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
