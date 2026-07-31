class SingletonMeta(type):
    """单例元类：同一个类重复构造时始终返回第一次创建的实例。

main.py 的 Database 使用此元类来演示单例；它不等于真实数据库连接池。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """首次创建实例，之后直接复用缓存实例。"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
