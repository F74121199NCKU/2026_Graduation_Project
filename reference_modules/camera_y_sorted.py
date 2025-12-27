# tags: camera, y-sort, depth, rendering, view
import pygame

class YSortStaticCamera(pygame.sprite.Group):
    """
    支援 Y-Sort (深度排序) 的靜態相機群組。
    Y 軸座標較大的物件會繪製在較前方，產生正確的遮擋效果。
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self, background_surface=None):
        """
        繪製所有精靈，並根據 Y 軸進行排序。
        :param background_surface: 可選的背景 Surface，若無則不繪製背景
        """
        # 1. 先畫背景 (如果有)
        if background_surface:
            self.display_surface.blit(background_surface, (0, 0))
        
        # 2. 核心邏輯：Y-Sort 排序繪製
        # sorted 回傳一個新的列表，不會影響原始 Group 的順序
        # lambda sprite: sprite.rect.centery 確保以底部或中心判定深度
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)