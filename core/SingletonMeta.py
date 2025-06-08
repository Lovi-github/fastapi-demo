class SingletonMeta(type):
    """
    این متا کلاس تضمین می‌کند که تنها یک نمونه از کلاس وجود داشته باشد.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
