# tags: sprite, rendering, group
import pygame

class GameSprite(pygame.sprite.Sprite):
    """所有遊戲物件的基礎類別，繼承自 Pygame 的 Sprite"""
    def __init__(self, x, y, image_path=None):
        super().__init__()
        if image_path:
            # 如果有圖片路徑，載入圖片
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            # 如果沒有圖片，建立一個紅色方塊代表
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0))
        
        # 建立矩形區域，用於碰撞偵測
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        """每幀更新位置，dt 是時間差 (Delta Time)"""
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt