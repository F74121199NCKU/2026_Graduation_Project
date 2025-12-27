# tags: camera, box-camera, scroll, y-sort
import pygame

class BoxCameraGroup(pygame.sprite.Group):
    """
    Box Camera (箱型相機) 邏輯封裝版。
    功能：
    1. 建立一個虛擬的 Camera Box。
    2. 只有當目標 (target) 移出 Box 邊界時，相機才會移動。
    3. 內建 Y-Sort (深度排序) 渲染。
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # 1. 動態獲取螢幕大小 (取代原本寫死的 SCREEN_SIZE)
        # 這樣無論遊戲視窗開多大，這個相機都能自動適應
        screen_w, screen_h = self.display_surface.get_size()
        
        self.offset = pygame.math.Vector2()

        # 2. 設定箱子邊界 (Camera Box Setup)
        # 這裡設定為視窗大小的 20% 作為邊界緩衝
        self.camera_borders = {
            'left': screen_w * 0.2,
            'right': screen_w * 0.2,
            'top': screen_h * 0.2,
            'bottom': screen_h * 0.2
        }
        
        # 計算箱子的具體矩形 (Rect)
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = screen_w - (self.camera_borders['left'] + self.camera_borders['right'])
        h = screen_h - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # 3. 背景設定 (Background)
        # 為了讓 AI 生成的遊戲不報錯，這裡使用通用防呆寫法
        try:
            self.ground_surf = pygame.image.load("Graphic/ground2.png").convert_alpha()
            # 這裡可以視需求調整地圖大小，或由外部傳入
            self.ground_surf = pygame.transform.scale(self.ground_surf, (2000, 2000))
        except Exception:
            # 如果找不到圖，就畫一個藍綠色的大地板
            self.ground_surf = pygame.Surface((2000, 2000))
            self.ground_surf.fill((70, 130, 180)) 
            
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def box_target_camera(self, target):
        """核心運算：更新相機偏移量"""
        
        # 左邊界檢查
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        # 右邊界檢查
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        # 上邊界檢查
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        # 下邊界檢查
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        # 計算最終偏移量 (相機框位置 - 邊界設定)
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, target):
        """渲染循環：包含背景與所有精靈的 Y-Sort"""
        
        self.box_target_camera(target)

        # 1. 畫地圖 (減去偏移量)
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)
        
        # 2. 畫精靈 (Y-Sort: 根據 centery 排序)
        # 這是 2D 遊戲最關鍵的渲染邏輯，確保樹木會擋住後面的人
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
        # (除錯用) 如果想看那個隱形的箱子在哪，可以取消下面這行的註解
        # pygame.draw.rect(self.display_surface, (255, 0, 0), self.camera_rect, 2)