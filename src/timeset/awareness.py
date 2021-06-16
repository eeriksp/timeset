from datetime import datetime

try:
    from django.utils.timezone import is_aware, make_aware
except ImportError:
    def is_aware(value: datetime) -> bool:
        return True


    def make_aware(value: datetime) -> datetime:
        return value


def ensure_aware(value: datetime) -> datetime:
    return value if is_aware(value) else make_aware(value)
