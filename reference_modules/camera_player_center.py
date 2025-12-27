# tags: camera, scroll, follow, player-center, y-sort
import pygame

class CameraScrollGroup(pygame.sprite.Group):
    """
    跟隨玩家移動的捲動相機，並內建 Y-Sort 深度排序。
    適用於 RPG、冒險遊戲等大地圖遊戲。
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Camera 偏移量
        self.offset = pygame.math.Vector2()
        
        # 取得畫面中心點
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # 嘗試載入地面圖片，若失敗則建立一個綠色背景
        try:
            self.ground_surf = pygame.image.load("Graphic/ground2.png").convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.ground_surf = pygame.Surface((2000, 2000))
            self.ground_surf.fill((30, 100, 30)) # 深綠色草地
            
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        """計算偏移量以確保目標在畫面中心"""
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        """
        :param player: 相機要跟隨的目標物件 (必須有 rect 屬性)
        """
        self.center_target_camera(player)

        # 1. 繪製地面 (需扣除偏移量)
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # 2. Y-Sort 迴圈：只繪製在視野內的物件會更有效能 (這裡先保留全繪製)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)