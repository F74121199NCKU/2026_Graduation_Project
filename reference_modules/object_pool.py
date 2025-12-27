# tags: optimization, memory, pool
class ObjectPool:
    """簡易的物件池，用於重複使用子彈或敵人，避免頻繁的記憶體配置"""
    def __init__(self, cls, size=100):
        # 預先建立一批物件
        self.pool = [cls() for _ in range(size)]
        self.active = []

    def get(self, *args, **kwargs):
        """從池中取出一個物件並初始化"""
        if self.pool:
            obj = self.pool.pop()
            # 假設物件都有一個 init 方法來重置狀態
            if hasattr(obj, 'init'):
                obj.init(*args, **kwargs)
            self.active.append(obj)
            return obj
        return None # 池子空了

    def release(self, obj):
        """將物件放回池中"""
        if obj in self.active:
            self.active.remove(obj)
            self.pool.append(obj)