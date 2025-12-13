import pygame
import sys
from enum import Enum
import random
import math
from typing import Dict, List, Optional, Tuple, Any, Callable

# --- Constants & Configuration ---

class GameConstants:
    """Centralized class for all game constants and configuration."""
    # Screen
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 700
    FPS: int = 60

    # Colors
    FIELD_COLOR: Tuple[int, int, int] = (34, 139, 34)  # Forest Green
    SKY_COLOR: Tuple[int, int, int] = (135, 206, 235)  # Sky Blue
    LINE_COLOR: Tuple[int, int, int] = (255, 255, 255) # White
    BASE_COLOR: Tuple[int, int, int] = (200, 200, 200) # Grey
    BAT_COLOR: Tuple[int, int, int] = (100, 50, 0)     # Brown
    BALL_COLOR_SEAM: Tuple[int, int, int] = (255, 0, 0) # Red for seam
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)
    UI_BG_COLOR: Tuple[int, int, int, int] = (50, 50, 50, 180) # Semi-transparent dark grey
    BUTTON_NORMAL_COLOR: Tuple[int, int, int] = (100, 100, 100)
    BUTTON_HOVER_COLOR: Tuple[int, int, int] = (150, 150, 150)
    HIGHLIGHT_COLOR: Tuple[int, int, int] = (0, 150, 0) # Green for selection
    PITCH_TARGET_COLOR: Tuple[int, int, int] = (255, 255, 0) # Yellow for target
    STRIKE_ZONE_OUTLINE_COLOR: Tuple[int, int, int] = (255, 0, 0) # Red outline
    GAME_OVER_WINNER_COLOR: Tuple[int, int, int] = (255, 255, 0)
    PLAYER_BATTER_COLOR: Tuple[int, int, int] = (200, 0, 200) # Purple for batter
    PLAYER_PITCHER_COLOR: Tuple[int, int, int] = (0, 200, 0) # Green for pitcher
    PLAYER_SPRITE_SIZE: int = 30 # Size for placeholder player sprites

    # Game Physics Constants
    GRAVITY: float = 9.8 * 60  # Pixels/second^2 (scaled for visual effect and dt)
    AIR_RESISTANCE_COEFFICIENT: float = 0.00001
    BALL_MASS: float = 0.145 # kg
    BALL_RADIUS: int = 10 # pixels
    BOUNCE_FACTOR: float = 0.6 # How much velocity is retained after bouncing
    FRICTION_FACTOR: float = 0.9 # How much horizontal velocity is retained after bouncing
    BALL_STOP_SPEED_THRESHOLD: float = 50.0 # Min velocity for ball to be considered in motion after bouncing

    # Baseball Physics Tuning (Magnus Effect, Hit physics) - extracted magic numbers
    CURVEBALL_SPIN_Y_EFFECT: float = 0.8 # Increased drop
    CURVEBALL_SPIN_X_EFFECT: float = -0.2 # Lateral movement
    SLIDER_SPIN_X_EFFECT: float = 0.5 # Lateral movement
    SLIDER_SPIN_Y_EFFECT: float = 0.1 # Small drop
    CHANGEUP_SLOWDOWN_EFFECT_MULTIPLIER: float = 0.5 # Additional slowdown factor
    CHANGEUP_SPIN_Y_EFFECT: float = 0.3 # Increased drop

    # Game Rules Constants
    MAX_BALLS: int = 4
    MAX_STRIKES: int = 3
    MAX_OUTS: int = 3
    DEFAULT_INNINGS: int = 9
    MIN_INNINGS_CHOICE: int = 5
    MAX_INNINGS_CHOICE: int = 9
    HOME_TEAM_ID: str = "HOME"
    AWAY_TEAM_ID: str = "AWAY"

    # UI Layout Constants
    BUTTON_WIDTH: int = 200
    BUTTON_HEIGHT: int = 50
    SMALL_BUTTON_WIDTH: int = 140
    MENU_BUTTON_Y_SPACING: int = 60
    MENU_CENTER_OFFSET: int = 50
    RULES_TEXT_MARGIN_X: int = 50
    RULES_TEXT_MARGIN_Y: int = 50
    RULES_SCROLL_SPEED_LINES: int = 3 # Lines per scroll
    RULES_SCROLL_ARROW_SIZE: int = 20 # Size of scroll arrow polygons
    SCOREBOARD_WIDTH: int = 240
    SCOREBOARD_HEIGHT: int = 100
    SCOREBOARD_X_MARGIN: int = 10
    SCOREBOARD_Y_MARGIN: int = 10
    SCOREBOARD_TEXT_Y_SPACING: int = 30
    COUNT_AND_RUNNERS_WIDTH: int = 200
    COUNT_AND_RUNNERS_HEIGHT: int = 100
    COUNT_TEXT_Y_SPACING: int = 25
    BASE_ICON_SIZE: int = 15
    THIRD_BASE_UI_OFFSET: Tuple[int, int] = (160, 20)
    SECOND_BASE_UI_OFFSET: Tuple[int, int] = (185, 20)
    FIRST_BASE_UI_OFFSET: Tuple[int, int] = (185, 45)
    PITCH_SELECTION_Y_OFFSET: int = 60 # From bottom of screen
    PITCH_SELECTION_BUTTON_WIDTH: int = 120
    PITCH_SELECTION_BUTTON_HEIGHT: int = 40
    PITCH_SELECTION_PADDING: int = 10
    UI_BORDER_RADIUS: int = 5
    PITCH_TARGET_CROSSHAIR_SIZE: int = 5 # Size of the crosshair lines on pitch target
    GAME_OVER_SCORE_OFFSET_Y: int = 20
    GAME_OVER_MESSAGE_OFFSET_Y: int = 100
    GAME_LOBBY_ROLE_TEXT_OFFSET_X: int = 250
    GAME_LOBBY_BUTTON_SPACING_X: int = 10
    GAME_LOBBY_BUTTON_SPACING_X_SMALL: int = 20

    # Field Layout Constants (relative to SCREEN_WIDTH, SCREEN_HEIGHT)
    GROUND_Y_OFFSET: int = 50 # Distance from bottom of screen to ground level
    HOME_RUN_WALL_Y_OFFSET: int = 450 # Distance from top of screen to home run wall
    PITCHER_POS_Y_OFFSET: int = 200 # Distance from bottom of screen to pitcher's Y position
    BATTER_POS_Y_OFFSET: int = 50 # Distance from bottom of screen to batter's Y position
    FOUL_LINE_X_EXTENT: int = 250 # Horizontal distance from screen center for foul line at ground level
    FOUL_LINE_Y_VISUAL_EXTENSION: int = 50 # How much lines extend up beyond HR wall Y for drawing
    FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR: float = 0.5 # How much foul lines diverge horizontally at HR wall Y
    STRIKE_ZONE_WIDTH: int = 100
    STRIKE_ZONE_HEIGHT: int = 100
    STRIKE_ZONE_Y_FROM_BOTTOM: int = 250 # Distance from bottom of screen to top of strike zone
    BAT_POSITION_OFFSET_X: int = 40
    BAT_POSITION_OFFSET_Y: int = -10
    BAT_HITBOX_WIDTH: int = 80
    BAT_HITBOX_HEIGHT: int = 20
    FIELDER_CATCH_ZONE_WIDTH: int = 200
    FIELDER_CATCH_ZONE_HEIGHT: int = 100
    FIELDER_CATCH_ZONE_Y_FROM_BOTTOM: int = 350 # Distance from bottom of screen to top of fielder catch zone
    BALL_OUT_OF_BOUNDS_MARGIN: int = 200 # How far off-screen before considered out of play
    HOME_PLATE_RADIUS: int = 15
    FIELD_BACKGROUND_HEIGHT: int = 300 # Height of the green field rectangle

    # Pitching/Batting Mechanics Tuning
    PITCHER_ACCURACY_X_ERROR_RANGE: Tuple[float, float] = (-50.0, 50.0) # For random target offset
    PITCHER_ACCURACY_Y_ERROR_RANGE: Tuple[float, float] = (-30.0, 30.0)
    PITCHER_MIN_PITCH_INTERVAL: float = 0.8 # sec
    PITCHER_BASE_FASTBALL_SPEED: float = 600.0 # px/sec
    PITCHER_BASE_CURVEBALL_BREAK: float = 200.0 # Spin magnitude for curve
    PITCHER_BASE_SLIDER_MOVEMENT: float = 150.0 # Spin magnitude for slider
    PITCHER_BASE_CHANGEUP_DECEPTION: float = 100.0 # Spin magnitude for changeup (slowdown/drop)

    BATTER_SWING_DURATION: float = 0.1 # sec
    BATTER_RUNNING_SPEED_BASE: float = 200.0 # px/sec
    BAT_HIT_BASE_SPEED: float = 800.0 # Base speed added to ball after hit
    BAT_HIT_BALL_SPEED_RETENTION: float = 0.3 # % of incoming ball speed retained
    BAT_HIT_SPEED_RANDOM_FACTOR: Tuple[float, float] = (0.9, 1.1)
    BAT_HIT_DIRECTION_RANDOM_X_RANGE: Tuple[float, float] = (-0.5, 0.5)
    BAT_HIT_DIRECTION_RANDOM_Y_RANGE: Tuple[float, float] = (-1.0, -0.2)
    BAT_HIT_DIRECTION_RANDOM_ANGLE: Tuple[float, float] = (-15.0, 15.0)
    HIT_BALL_Y_THRESHOLD_FOR_FOUL_CHECK: int = -10 # Y-offset from home plate to consider ball "past" for detailed foul check
    BALL_PASSED_STRIKE_ZONE_BUFFER: int = 20 # How far below strike zone bottom before judging strike/ball
    PITCH_TARGET_MOVE_AMOUNT: int = 10 # Pixels for pitch target movement
    PITCH_TARGET_Y_MIN: int = SCREEN_HEIGHT // 2 - 200
    PITCH_TARGET_Y_MAX: int = SCREEN_HEIGHT - 150 - STRIKE_ZONE_HEIGHT

    # AI Tuning
    AI_BATTER_SWING_CHANCE_STRIKE_ZONE: float = 0.8
    AI_BATTER_SWING_CHANCE_BALL_ZONE: float = 0.1
    AI_BATTER_CONTACT_ABILITY_MULTIPLIER: float = 0.7 # Multiplies against swing chance
    AI_PITCHER_VARIETY_CHANCE: float = 0.3 # Chance to throw non-fastball
    AI_PITCHER_TARGET_OFFSET_FACTOR: float = 0.4 # % of strike zone width/height for target randomness
    AI_FIELDER_CATCH_CHANCE: float = 0.7 # Chance to catch a hit ball in catch zone

    # At-bat Outcome Distances (simplified)
    HIT_TRIPLE_DISTANCE_THRESHOLD: float = 400.0 
    HIT_DOUBLE_DISTANCE_THRESHOLD: float = 200.0 
    HOME_RUN_MIN_Y_VELOCITY_FOR_HR: float = 0.0 # Ball must be moving upwards (negative Y velocity)

    # Ball arrival prediction for AI/player feedback
    BALL_PREDICT_SIM_DT: float = 0.005
    BALL_PREDICT_MAX_SIM_TIME: float = 2.0

    # Font sizes
    FONT_SIZE_SMALL: int = 24
    FONT_SIZE_MEDIUM: int = 36
    FONT_SIZE_LARGE: int = 48
    FONT_SIZE_XLARGE: int = 72


# Use a shorter alias for convenience
C = GameConstants

# --- Utility Classes ---

class GenericObjectPool:
    """
    A generic object pool for recycling frequently created/destroyed objects.
    Each object managed by the pool must have a `reset(*args, **kwargs)` method.
    """
    def __init__(self, obj_class: type, initial_size: int):
        self.obj_class = obj_class
        self.pool: List[Any] = [obj_class() for _ in range(initial_size)]
        self.active_objects: List[Any] = []

    def get(self, *args: Any, **kwargs: Any) -> Any:
        if self.pool:
            obj = self.pool.pop()
            obj.reset(*args, **kwargs)
        else:
            obj = self.obj_class()
            obj.reset(*args, **kwargs)
        self.active_objects.append(obj)
        return obj

    def recycle(self, obj: Any) -> None:
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            self.pool.append(obj)

    def get_active(self) -> List[Any]:
        return list(self.active_objects) # Return a copy to prevent modification during iteration

    def clear_active(self) -> None:
        """Recycles all currently active objects."""
        for obj in list(self.active_objects):
            self.recycle(obj)

class EventManager:
    """
    Implements a simple observer pattern for cross-object communication.
    """
    def __init__(self) -> None:
        self.listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, listener: Callable[[Any], None]) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener: Callable[[Any], None]) -> None:
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)

    def post(self, event_type: str, data: Optional[Any] = None) -> None:
        if event_type in self.listeners:
            # Iterate over a copy to prevent issues if listeners modify the list during iteration
            for listener in list(self.listeners[event_type]): 
                listener(data)

# --- Game Enums ---

class GameStateEnum(Enum):
    MAIN_MENU = 1
    RULES = 2
    GAME_LOBBY = 3
    PLAYING = 4
    GAME_OVER = 5

class PlayerRole(Enum):
    BATTER = 1
    PITCHER = 2

class PitchType(Enum):
    FASTBALL = "快速球"
    CURVEBALL = "變化球"
    SLIDER = "滑球"
    CHANGEUP = "變速球"

class BaseballState(Enum):
    IN_FLIGHT = 1
    GROUNDED = 2
    CAUGHT = 3
    FOUL = 4
    STRIKE_ZONE = 5 # Ball passed through strike zone
    BALL_ZONE = 6   # Ball passed outside strike zone
    HOME_RUN = 7
    OUT_OF_PLAY = 8 # Ball is off-screen, caught, or otherwise done with its current play
    AWAITING_PITCH = 9 # Before pitch is thrown

class BaseEnum(Enum):
    HOME_PLATE = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3

class GameMode(Enum):
    PLAYER_PITCHING = 1 # Player controls pitcher, AI controls batter
    PLAYER_BATTING = 2  # Player controls batter, AI controls pitcher

# --- Game Entities ---

class Baseball:
    """
    Represents the baseball in the game. Managed by an Object Pool.
    """
    def __init__(self) -> None:
        # Pre-render ball image for performance
        self.image = pygame.Surface((C.BALL_RADIUS * 2, C.BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, C.LINE_COLOR, (C.BALL_RADIUS, C.BALL_RADIUS), C.BALL_RADIUS)
        pygame.draw.line(self.image, C.BALL_COLOR_SEAM, (0, C.BALL_RADIUS), (C.BALL_RADIUS * 2, C.BALL_RADIUS), 2)
        pygame.draw.line(self.image, C.BALL_COLOR_SEAM, (C.BALL_RADIUS, 0), (C.BALL_RADIUS, C.BALL_RADIUS * 2), 2)
        self.image = self.image.convert_alpha()

        self.position: pygame.math.Vector2 = pygame.math.Vector2()
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2()
        self.acceleration: pygame.math.Vector2 = pygame.math.Vector2()
        self.radius: int = C.BALL_RADIUS
        self.mass: float = C.BALL_MASS
        self.spin_magnitude: float = 0.0
        self.pitch_type: PitchType = PitchType.FASTBALL
        self.state: BaseballState = BaseballState.AWAITING_PITCH
        self.is_hit: bool = False # True if the ball was hit by a bat
        self.has_bounced: bool = False
        self.owner_id: Optional[int] = None # Who pitched it or hit it last

    def reset(self, position: pygame.math.Vector2, velocity: pygame.math.Vector2, 
              pitch_type: PitchType, spin_magnitude: float = 0.0, owner_id: Optional[int] = None) -> None:
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.acceleration = pygame.math.Vector2(0, C.GRAVITY) # Gravity always applies
        self.radius = C.BALL_RADIUS
        self.mass = C.BALL_MASS
        self.spin_magnitude = spin_magnitude
        self.pitch_type = pitch_type
        self.state = BaseballState.IN_FLIGHT
        self.is_hit = False
        self.has_bounced = False
        self.owner_id = owner_id
        
    def update(self, dt: float, ground_y: int) -> None:
        if self.state not in [BaseballState.IN_FLIGHT, BaseballState.GROUNDED]:
            return

        # Apply air resistance (drag)
        if self.velocity.length_squared() > 0:
            drag_force_magnitude = C.AIR_RESISTANCE_COEFFICIENT * self.velocity.length_squared()
            drag_force = -self.velocity.normalize() * drag_force_magnitude
            self.acceleration += drag_force / self.mass

        # Apply Magnus Effect for breaking balls (simplified simulation)
        if self.spin_magnitude > 0 and not self.is_hit:
            if self.pitch_type == PitchType.CURVEBALL:
                self.acceleration.y += self.spin_magnitude * C.CURVEBALL_SPIN_Y_EFFECT
                self.acceleration.x += self.spin_magnitude * C.CURVEBALL_SPIN_X_EFFECT
            elif self.pitch_type == PitchType.SLIDER:
                self.acceleration.x += self.spin_magnitude * C.SLIDER_SPIN_X_EFFECT
                self.acceleration.y += self.spin_magnitude * C.SLIDER_SPIN_Y_EFFECT
            elif self.pitch_type == PitchType.CHANGEUP:
                self.velocity *= (1 - C.CHANGEUP_SLOWDOWN_EFFECT_MULTIPLIER * dt * self.spin_magnitude)
                self.acceleration.y += self.spin_magnitude * C.CHANGEUP_SPIN_Y_EFFECT
        
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.acceleration = pygame.math.Vector2(0, C.GRAVITY) # Reset non-gravitational acceleration each frame

        # Simplified ground collision
        if self.position.y + self.radius > ground_y:
            self.position.y = ground_y - self.radius # Prevent sinking
            if self.state == BaseballState.IN_FLIGHT:
                self.state = BaseballState.GROUNDED
                if not self.has_bounced:
                    self.velocity.y *= -C.BOUNCE_FACTOR # Bounce up
                    self.velocity.x *= C.FRICTION_FACTOR # Reduce horizontal speed
                    self.has_bounced = True
                else:
                    # After first bounce, if speed is very low, stop the ball
                    if self.velocity.length() < C.BALL_STOP_SPEED_THRESHOLD:
                        self.velocity = pygame.math.Vector2(0,0)
                        self.acceleration = pygame.math.Vector2(0,0)
                        self.state = BaseballState.OUT_OF_PLAY

    def draw(self, screen: pygame.Surface) -> None:
        if self.state in [BaseballState.IN_FLIGHT, BaseballState.GROUNDED]:
            screen.blit(self.image, self.image.get_rect(center=self.position))

class Player(pygame.sprite.Sprite):
    """
    Abstract base class for Player entities (Pitcher, Batter).
    """
    def __init__(self, role: PlayerRole, team_id: str, position: pygame.math.Vector2) -> None:
        super().__init__()
        self.role: PlayerRole = role
        self.team_id: str = team_id
        self.position: pygame.math.Vector2 = position.copy()
        self.stamina: float = 100.0
        self.fatigue_effect: float = 0.0
        self.current_animation_state: str = "IDLE"
        self.running_speed_base: float = C.BATTER_RUNNING_SPEED_BASE
        self.id: int = random.randint(1, 100000) # Simple unique ID

        self.image = pygame.Surface((C.PLAYER_SPRITE_SIZE, C.PLAYER_SPRITE_SIZE))
        self.image.fill(C.HIGHLIGHT_COLOR if team_id == C.HOME_TEAM_ID else C.SKY_COLOR) # Visual placeholder for team
        self.rect = self.image.get_rect(center=self.position)
        self.image = self.image.convert()

    def update(self, dt: float) -> None:
        # Update stamina, fatigue, etc. (simplified for this version)
        pass

    def draw(self, screen: pygame.Surface) -> None:
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

class Pitcher(Player):
    def __init__(self, team_id: str, position: pygame.math.Vector2) -> None:
        super().__init__(PlayerRole.PITCHER, team_id, position)
        self.image.fill(C.PLAYER_PITCHER_COLOR) # Green for pitcher
        self.pitching_power: float = 0.9 # Affects initial speed
        self.pitching_accuracy: float = 0.8 # Affects target offset
        self.fastball_speed_base: float = C.PITCHER_BASE_FASTBALL_SPEED
        self.curveball_break: float = C.PITCHER_BASE_CURVEBALL_BREAK
        self.slider_movement: float = C.PITCHER_BASE_SLIDER_MOVEMENT
        self.changeup_deception: float = C.PITCHER_BASE_CHANGEUP_DECEPTION
        self.pitch_rate_limit: float = C.PITCHER_MIN_PITCH_INTERVAL
        self.last_pitch_time: float = -self.pitch_rate_limit # Allow immediate first pitch
        self.available_pitches: List[PitchType] = [PitchType.FASTBALL, PitchType.CURVEBALL, PitchType.SLIDER, PitchType.CHANGEUP]

    def throw_ball(self, current_time: float, target_pos: pygame.math.Vector2, 
                   pitch_type: PitchType, ball_pool: GenericObjectPool) -> Optional[Baseball]:
        if current_time - self.last_pitch_time < self.pitch_rate_limit:
            return None

        pitcher_pos = self.position
        initial_speed = self.fastball_speed_base * self.pitching_power

        # Introduce accuracy error based on pitching_accuracy
        accuracy_offset_x = (1 - self.pitching_accuracy) * random.uniform(C.PITCHER_ACCURACY_X_ERROR_RANGE[0], C.PITCHER_ACCURACY_X_ERROR_RANGE[1])
        accuracy_offset_y = (1 - self.pitching_accuracy) * random.uniform(C.PITCHER_ACCURACY_Y_ERROR_RANGE[0], C.PITCHER_ACCURACY_Y_ERROR_RANGE[1])
        actual_target_pos = target_pos + pygame.math.Vector2(accuracy_offset_x, accuracy_offset_y)

        direction = (actual_target_pos - pitcher_pos).normalize()
        initial_velocity = direction * initial_speed

        # Set spin magnitude based on pitch type
        spin_magnitude = 0.0
        if pitch_type == PitchType.CURVEBALL:
            spin_magnitude = self.curveball_break
        elif pitch_type == PitchType.SLIDER:
            spin_magnitude = self.slider_movement
        elif pitch_type == PitchType.CHANGEUP:
            spin_magnitude = self.changeup_deception

        baseball = ball_pool.get(position=pitcher_pos, velocity=initial_velocity, 
                                 pitch_type=pitch_type, spin_magnitude=spin_magnitude, owner_id=self.id)
        self.last_pitch_time = current_time
        return baseball

class Batter(Player):
    def __init__(self, team_id: str, position: pygame.math.Vector2) -> None:
        super().__init__(PlayerRole.BATTER, team_id, position)
        self.image.fill(C.PLAYER_BATTER_COLOR) # Purple for batter
        self.batting_power: float = 0.8 # Affects hit ball speed
        self.batting_timing_window: float = 0.15 # seconds for "perfect" hit
        self.contact_ability: float = 0.7 # For AI, chance to hit in general
        self.eyesight: float = 0.7 # For AI, accuracy of strike/ball judgment
        self.bat_rect: pygame.Rect = pygame.Rect(0, 0, C.BAT_HITBOX_WIDTH, C.BAT_HITBOX_HEIGHT) # Simplified bat hitbox
        self.bat_position_offset: pygame.math.Vector2 = pygame.math.Vector2(C.BAT_POSITION_OFFSET_X, C.BAT_POSITION_OFFSET_Y) # Relative to batter's center
        self.is_swinging: bool = False
        self.swing_timer: float = 0.0
        self.swing_duration: float = C.BATTER_SWING_DURATION

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.is_swinging:
            self.swing_timer += dt
            if self.swing_timer >= self.swing_duration:
                self.is_swinging = False
                self.swing_timer = 0.0
        self.bat_rect.center = self.position + self.bat_position_offset

    def swing_bat(self) -> None:
        if not self.is_swinging:
            self.is_swinging = True
            self.swing_timer = 0.0

    def get_bat_hitbox(self) -> Optional[pygame.Rect]:
        if self.is_swinging:
            return self.bat_rect
        return None

# --- Game Systems ---

class UISystem:
    """
    Manages and renders all User Interface elements.
    """
    def __init__(self, event_manager: EventManager, fonts: Dict[str, pygame.font.Font]) -> None:
        self.event_manager = event_manager
        self.fonts = fonts
        self.rules_text = [
            "經典棒球對決 - 規則說明",
            "",
            "1. 遊戲模式:",
            "   - 投球模式: 玩家扮演投手，選擇球路和瞄準區域，三振電腦AI打者。",
            "   - 打擊模式: 玩家扮演打者，判斷來球時機，揮棒擊球，打出安打或全壘打。",
            "",
            "2. 投球操作 (玩家為投手):",
            "   - 方向鍵 (A/D/W/S): 調整投球瞄準區的位置。",
            "   - Z/X/C/V: 選擇球路 (快速球/變化球/滑球/變速球)。",
            "   - 空白鍵: 確認投球。",
            "",
            "3. 打擊操作 (玩家為打者):",
            "   - 空白鍵: 揮棒。需精準判斷來球時機。",
            "",
            "4. 棒球規則簡述 (簡化版):",
            "   - 投打對決: 投手將球投向本壘，打者嘗試擊球。",
            "   - 好球/壞球: 球進入好球帶且打者未揮棒為好球；未進入好球帶為壞球。",
            "   - 三振: 3個好球，打者出局。",
            "   - 四壞球: 4個壞球，打者保送上一壘。",
            "   - 出局: 3個出局數結束半局。",
            "   - 得分: 跑者安全回到本壘得分。",
            "   - 局數: 遊戲進行預設9局，分數高者勝。",
            "",
            "按任意鍵或滑鼠點擊返回主選單"
        ]
        self.scroll_offset: int = 0
        self.line_height: int = self.fonts['sm'].get_linesize() + 2

        # Subscribe to game events for UI updates
        self.event_manager.subscribe("UPDATE_SCOREBOARD", self.update_scoreboard)
        self.event_manager.subscribe("UPDATE_COUNT", self.update_count)
        self.event_manager.subscribe("UPDATE_RUNNERS", self.update_runners)
        self.event_manager.subscribe("SET_PITCH_TARGET", self.set_pitch_target)
        self.event_manager.subscribe("GAME_OVER_INFO", self.set_game_over_info)
        self.event_manager.subscribe("SET_PITCH_SELECTION", self.set_pitch_selection_options)

        # UI data storage
        self.scoreboard_data: Dict[str, Any] = {'HomeScore': 0, 'AwayScore': 0, 'Inning': 1, 'IsTopHalf': True}
        self.count_data: Dict[str, int] = {'Balls': 0, 'Strikes': 0, 'Outs': 0}
        self.runners_data: Dict[BaseEnum, bool] = {BaseEnum.FIRST: False, BaseEnum.SECOND: False, BaseEnum.THIRD: False}
        self.pitch_target_rect: Optional[pygame.Rect] = None
        self.pitch_selection_options: List[PitchType] = []
        self.selected_pitch_type: Optional[PitchType] = None
        self.game_over_info: Optional[Dict[str, str]] = None

        # Pre-render button surfaces for performance
        self.button_normal_surf = pygame.Surface((C.BUTTON_WIDTH, C.BUTTON_HEIGHT))
        self.button_normal_surf.fill(C.BUTTON_NORMAL_COLOR)
        self.button_normal_surf = self.button_normal_surf.convert()

        self.button_hover_surf = pygame.Surface((C.BUTTON_WIDTH, C.BUTTON_HEIGHT))
        self.button_hover_surf.fill(C.BUTTON_HOVER_COLOR)
        self.button_hover_surf = self.button_hover_surf.convert()

        self.small_button_normal_surf = pygame.Surface((C.SMALL_BUTTON_WIDTH, C.BUTTON_HEIGHT))
        self.small_button_normal_surf.fill(C.BUTTON_NORMAL_COLOR)
        self.small_button_normal_surf = self.small_button_normal_surf.convert()

        self.small_button_hover_surf = pygame.Surface((C.SMALL_BUTTON_WIDTH, C.BUTTON_HEIGHT))
        self.small_button_hover_surf.fill(C.BUTTON_HOVER_COLOR)
        self.small_button_hover_surf = self.small_button_hover_surf.convert()

        self.small_button_selected_surf = pygame.Surface((C.SMALL_BUTTON_WIDTH, C.BUTTON_HEIGHT))
        self.small_button_selected_surf.fill(C.HIGHLIGHT_COLOR)
        self.small_button_selected_surf = self.small_button_selected_surf.convert()


    def update_scoreboard(self, data: Dict[str, Any]) -> None:
        self.scoreboard_data.update(data)

    def update_count(self, data: Dict[str, int]) -> None:
        self.count_data.update(data)

    def update_runners(self, data: Dict[str, bool]) -> None:
        self.runners_data[BaseEnum.FIRST] = data['FirstBaseOccupied']
        self.runners_data[BaseEnum.SECOND] = data['SecondBaseOccupied']
        self.runners_data[BaseEnum.THIRD] = data['ThirdBaseOccupied']

    def set_pitch_target(self, rect: Optional[pygame.Rect]) -> None:
        self.pitch_target_rect = rect

    def set_pitch_selection_options(self, data: Dict[str, Any]) -> None:
        self.pitch_selection_options = data['options']
        self.selected_pitch_type = data['selected_type']

    def set_game_over_info(self, info: Dict[str, str]) -> None:
        self.game_over_info = info

    def draw_scoreboard(self, screen: pygame.Surface) -> None:
        bg_rect = pygame.Rect(C.SCREEN_WIDTH - C.SCOREBOARD_WIDTH - C.SCOREBOARD_X_MARGIN, C.SCOREBOARD_Y_MARGIN, C.SCOREBOARD_WIDTH, C.SCOREBOARD_HEIGHT)
        pygame.draw.rect(screen, C.UI_BG_COLOR, bg_rect, border_radius=C.UI_BORDER_RADIUS)
        pygame.draw.rect(screen, C.LINE_COLOR, bg_rect, 1, border_radius=C.UI_BORDER_RADIUS)

        text_inning = self.fonts['sm'].render(f"局數: {self.scoreboard_data['Inning']}{'上' if self.scoreboard_data['IsTopHalf'] else '下'}", True, C.TEXT_COLOR)
        text_score = self.fonts['sm'].render(f"主隊: {self.scoreboard_data['HomeScore']} 客隊: {self.scoreboard_data['AwayScore']}", True, C.TEXT_COLOR)

        screen.blit(text_inning, (bg_rect.x + C.SCOREBOARD_X_MARGIN, bg_rect.y + C.SCOREBOARD_Y_MARGIN))
        screen.blit(text_score, (bg_rect.x + C.SCOREBOARD_X_MARGIN, bg_rect.y + C.SCOREBOARD_Y_MARGIN + C.SCOREBOARD_TEXT_Y_SPACING))

    def draw_count_and_runners(self, screen: pygame.Surface) -> None:
        bg_rect = pygame.Rect(C.SCOREBOARD_X_MARGIN, C.SCOREBOARD_Y_MARGIN, C.COUNT_AND_RUNNERS_WIDTH, C.COUNT_AND_RUNNERS_HEIGHT)
        pygame.draw.rect(screen, C.UI_BG_COLOR, bg_rect, border_radius=C.UI_BORDER_RADIUS)
        pygame.draw.rect(screen, C.LINE_COLOR, bg_rect, 1, border_radius=C.UI_BORDER_RADIUS)

        text_balls = self.fonts['sm'].render(f"壞球: {self.count_data['Balls']}", True, C.TEXT_COLOR)
        text_strikes = self.fonts['sm'].render(f"好球: {self.count_data['Strikes']}", True, C.TEXT_COLOR)
        text_outs = self.fonts['sm'].render(f"出局: {self.count_data['Outs']}", True, C.TEXT_COLOR)

        screen.blit(text_balls, (bg_rect.x + C.SCOREBOARD_X_MARGIN, bg_rect.y + C.SCOREBOARD_Y_MARGIN))
        screen.blit(text_strikes, (bg_rect.x + C.SCOREBOARD_X_MARGIN, bg_rect.y + C.SCOREBOARD_Y_MARGIN + C.COUNT_TEXT_Y_SPACING))
        screen.blit(text_outs, (bg_rect.x + C.SCOREBOARD_X_MARGIN, bg_rect.y + C.SCOREBOARD_Y_MARGIN + C.COUNT_TEXT_Y_SPACING * 2))

        # Draw bases for runners (simplified diamond shape)
        base_size = C.BASE_ICON_SIZE
        
        # Third base
        third_base_center = (bg_rect.x + C.THIRD_BASE_UI_OFFSET[0], bg_rect.y + C.THIRD_BASE_UI_OFFSET[1])
        pygame.draw.polygon(screen, C.HIGHLIGHT_COLOR if self.runners_data[BaseEnum.THIRD] else C.BASE_COLOR,
                            [(third_base_center[0], third_base_center[1] - base_size/2),
                             (third_base_center[0] + base_size/2, third_base_center[1]),
                             (third_base_center[0], third_base_center[1] + base_size/2),
                             (third_base_center[0] - base_size/2, third_base_center[1])])
        pygame.draw.polygon(screen, C.LINE_COLOR,
                            [(third_base_center[0], third_base_center[1] - base_size/2),
                             (third_base_center[0] + base_size/2, third_base_center[1]),
                             (third_base_center[0], third_base_center[1] + base_size/2),
                             (third_base_center[0] - base_size/2, third_base_center[1])], 1)

        # Second base
        second_base_center = (bg_rect.x + C.SECOND_BASE_UI_OFFSET[0], bg_rect.y + C.SECOND_BASE_UI_OFFSET[1])
        pygame.draw.polygon(screen, C.HIGHLIGHT_COLOR if self.runners_data[BaseEnum.SECOND] else C.BASE_COLOR,
                            [(second_base_center[0], second_base_center[1] - base_size/2),
                             (second_base_center[0] + base_size/2, second_base_center[1]),
                             (second_base_center[0], second_base_center[1] + base_size/2),
                             (second_base_center[0] - base_size/2, second_base_center[1])])
        pygame.draw.polygon(screen, C.LINE_COLOR,
                            [(second_base_center[0], second_base_center[1] - base_size/2),
                             (second_base_center[0] + base_size/2, second_base_center[1]),
                             (second_base_center[0], second_base_center[1] + base_size/2),
                             (second_base_center[0] - base_size/2, second_base_center[1])], 1)
        
        # First base
        first_base_center = (bg_rect.x + C.FIRST_BASE_UI_OFFSET[0], bg_rect.y + C.FIRST_BASE_UI_OFFSET[1])
        pygame.draw.polygon(screen, C.HIGHLIGHT_COLOR if self.runners_data[BaseEnum.FIRST] else C.BASE_COLOR,
                            [(first_base_center[0], first_base_center[1] - base_size/2),
                             (first_base_center[0] + base_size/2, first_base_center[1]),
                             (first_base_center[0], first_base_center[1] + base_size/2),
                             (first_base_center[0] - base_size/2, first_base_center[1])])
        pygame.draw.polygon(screen, C.LINE_COLOR,
                            [(first_base_center[0], first_base_center[1] - base_size/2),
                             (first_base_center[0] + base_size/2, first_base_center[1]),
                             (first_base_center[0], first_base_center[1] + base_size/2),
                             (first_base_center[0] - base_size/2, first_base_center[1])], 1)


    def draw_pitch_selection_ui(self, screen: pygame.Surface) -> None:
        if not self.pitch_selection_options:
            return

        start_y = C.SCREEN_HEIGHT - C.PITCH_SELECTION_Y_OFFSET
        button_width = C.PITCH_SELECTION_BUTTON_WIDTH
        button_height = C.PITCH_SELECTION_BUTTON_HEIGHT
        padding = C.PITCH_SELECTION_PADDING
        total_width = len(self.pitch_selection_options) * (button_width + padding) - padding
        start_x = (C.SCREEN_WIDTH - total_width) // 2

        for i, pitch_type in enumerate(self.pitch_selection_options):
            btn_rect = pygame.Rect(start_x + i * (button_width + padding), start_y, button_width, button_height)
            
            if pitch_type == self.selected_pitch_type:
                pygame.draw.rect(screen, C.HIGHLIGHT_COLOR, btn_rect, border_radius=C.UI_BORDER_RADIUS)
            else:
                pygame.draw.rect(screen, C.BUTTON_NORMAL_COLOR, btn_rect, border_radius=C.UI_BORDER_RADIUS)
            
            pygame.draw.rect(screen, C.LINE_COLOR, btn_rect, 1, border_radius=C.UI_BORDER_RADIUS)

            text_surf = self.fonts['sm'].render(pitch_type.value, True, C.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=btn_rect.center)
            screen.blit(text_surf, text_rect)

    def draw_pitch_target_ui(self, screen: pygame.Surface) -> None:
        if self.pitch_target_rect:
            pygame.draw.rect(screen, C.PITCH_TARGET_COLOR, self.pitch_target_rect, 2)
            center_x, center_y = self.pitch_target_rect.center
            pygame.draw.line(screen, C.PITCH_TARGET_COLOR, (center_x - C.PITCH_TARGET_CROSSHAIR_SIZE, center_y), (center_x + C.PITCH_TARGET_CROSSHAIR_SIZE, center_y), 2)
            pygame.draw.line(screen, C.PITCH_TARGET_COLOR, (center_x, center_y - C.PITCH_TARGET_CROSSHAIR_SIZE), (center_x, center_y + C.PITCH_TARGET_CROSSHAIR_SIZE), 2)

    def draw_rules_page(self, screen: pygame.Surface) -> None:
        screen.fill(C.UI_BG_COLOR)
        
        y_offset = C.RULES_TEXT_MARGIN_Y + self.scroll_offset
        for line in self.rules_text:
            text_surf = self.fonts['sm'].render(line, True, C.TEXT_COLOR)
            screen.blit(text_surf, (C.RULES_TEXT_MARGIN_X, y_offset))
            y_offset += self.line_height

        # Scroll indicator arrows
        if self.scroll_offset < 0:
            pygame.draw.polygon(screen, C.TEXT_COLOR, [(C.SCREEN_WIDTH - C.RULES_SCROLL_ARROW_SIZE - 10, 20), (C.SCREEN_WIDTH - 10, 20), (C.SCREEN_WIDTH - C.RULES_SCROLL_ARROW_SIZE / 2 - 10, 40)]) # Up arrow
        if y_offset > C.SCREEN_HEIGHT - C.RULES_TEXT_MARGIN_Y:
            pygame.draw.polygon(screen, C.TEXT_COLOR, [(C.SCREEN_WIDTH - C.RULES_SCROLL_ARROW_SIZE - 10, C.SCREEN_HEIGHT - 40), (C.SCREEN_WIDTH - 10, C.SCREEN_HEIGHT - 40), (C.SCREEN_WIDTH - C.RULES_SCROLL_ARROW_SIZE / 2 - 10, C.SCREEN_HEIGHT - 20)]) # Down arrow


    def draw_menu_button(self, screen: pygame.Surface, text: str, rect: pygame.Rect, is_hovered: bool) -> None:
        current_image = self.button_hover_surf if is_hovered else self.button_normal_surf
        screen.blit(current_image, rect)
        text_surf = self.fonts['md'].render(text, True, C.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def draw_selection_button(self, screen: pygame.Surface, text: str, rect: pygame.Rect, 
                               is_selected: bool, is_hovered: bool) -> None:
        if is_selected:
            current_image = self.small_button_selected_surf
        elif is_hovered:
            current_image = self.small_button_hover_surf
        else:
            current_image = self.small_button_normal_surf
        
        screen.blit(current_image, rect)
        text_surf = self.fonts['md'].render(text, True, C.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def draw_game_over_screen(self, screen: pygame.Surface) -> None:
        screen.fill(C.UI_BG_COLOR)
        if self.game_over_info:
            winner_text = self.fonts['xl'].render(self.game_over_info['winner'], True, C.GAME_OVER_WINNER_COLOR)
            score_text = self.fonts['lg'].render(self.game_over_info['score_text'], True, C.TEXT_COLOR)
            message_text = self.fonts['md'].render("按任意鍵或滑鼠點擊返回主選單", True, C.TEXT_COLOR)

            winner_rect = winner_text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - C.MENU_CENTER_OFFSET))
            score_rect = score_text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + C.GAME_OVER_SCORE_OFFSET_Y))
            message_rect = message_text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + C.GAME_OVER_MESSAGE_OFFSET_Y))

            screen.blit(winner_text, winner_rect)
            screen.blit(score_text, score_rect)
            screen.blit(message_text, message_rect)

class AIManager:
    """
    Manages AI logic for pitcher and batter.
    """
    def __init__(self, event_manager: EventManager, collision_manager: 'CollisionManager') -> None:
        self.event_manager = event_manager
        self.collision_manager = collision_manager
    
    def ai_pitcher_decide_pitch(self, pitcher: Pitcher) -> Tuple[PitchType, pygame.math.Vector2]:
        """
        AI Pitcher decides pitch type and target.
        """
        available_pitches = pitcher.available_pitches
        pitch_type = PitchType.FASTBALL

        if random.random() < C.AI_PITCHER_VARIETY_CHANCE and len(available_pitches) > 1:
            non_fastballs = [p for p in available_pitches if p != PitchType.FASTBALL]
            if non_fastballs:
                pitch_type = random.choice(non_fastballs)

        strike_zone_x_center = self.collision_manager.strike_zone_rect.centerx
        strike_zone_y_center = self.collision_manager.strike_zone_rect.centery

        target_offset_x = random.uniform(-self.collision_manager.strike_zone_rect.width * C.AI_PITCHER_TARGET_OFFSET_FACTOR,
                                         self.collision_manager.strike_zone_rect.width * C.AI_PITCHER_TARGET_OFFSET_FACTOR)
        target_offset_y = random.uniform(-self.collision_manager.strike_zone_rect.height * C.AI_PITCHER_TARGET_OFFSET_FACTOR,
                                         self.collision_manager.strike_zone_rect.height * C.AI_PITCHER_TARGET_OFFSET_FACTOR)
        
        target_pos = pygame.math.Vector2(strike_zone_x_center + target_offset_x, strike_zone_y_center + target_offset_y)
        
        return pitch_type, target_pos
    
    def ai_batter_decide_swing(self, batter: Batter, baseball_obj: Optional[Baseball]) -> bool:
        """
        AI Batter decides whether to swing at an incoming pitch.
        """
        if baseball_obj is None or baseball_obj.state != BaseballState.IN_FLIGHT:
            return False

        temp_ball = Baseball()
        temp_ball.reset(baseball_obj.position, baseball_obj.velocity, baseball_obj.pitch_type, 
                        baseball_obj.spin_magnitude, baseball_obj.owner_id)
        
        sim_dt = C.BALL_PREDICT_SIM_DT
        sim_time = 0.0
        is_strike = False

        while temp_ball.position.y < self.collision_manager.strike_zone_rect.bottom + C.BALL_PASSED_STRIKE_ZONE_BUFFER and sim_time < C.BALL_PREDICT_MAX_SIM_TIME:
            temp_ball.update(sim_dt, C.SCREEN_HEIGHT - C.GROUND_Y_OFFSET) # Pass ground_y
            sim_time += sim_dt
            if self.collision_manager.strike_zone_rect.collidepoint(temp_ball.position.x, temp_ball.position.y):
                is_strike = True
                break

        if is_strike:
            return random.random() < batter.contact_ability * C.AI_BATTER_SWING_CHANCE_STRIKE_ZONE
        else:
            return random.random() < batter.contact_ability * C.AI_BATTER_SWING_CHANCE_BALL_ZONE

class CollisionManager:
    """
    Handles collision detection and resolution for game objects, and defines field boundaries.
    """
    def __init__(self) -> None:
        self.ground_y: int = C.SCREEN_HEIGHT - C.GROUND_Y_OFFSET
        self.home_plate_pos_center: pygame.math.Vector2 = pygame.math.Vector2(C.SCREEN_WIDTH // 2, self.ground_y)

        # Foul lines start from home plate area, extending out
        self.foul_line_left_x_at_ground: int = C.SCREEN_WIDTH // 2 - C.FOUL_LINE_X_EXTENT
        self.foul_line_right_x_at_ground: int = C.SCREEN_WIDTH // 2 + C.FOUL_LINE_X_EXTENT

        # Outfield wall for home runs
        self.home_run_wall_y: int = C.SCREEN_HEIGHT - C.HOME_RUN_WALL_Y_OFFSET

        # Strike zone definition (relative to screen, fixed position)
        self.strike_zone_rect: pygame.Rect = pygame.Rect(
            C.SCREEN_WIDTH // 2 - C.STRIKE_ZONE_WIDTH // 2,
            C.SCREEN_HEIGHT - C.STRIKE_ZONE_Y_FROM_BOTTOM,
            C.STRIKE_ZONE_WIDTH,
            C.STRIKE_ZONE_HEIGHT
        )

        # Fielder catch zone (simplified)
        self.fielder_catch_zone_rect: pygame.Rect = pygame.Rect(
            C.SCREEN_WIDTH // 2 - C.FIELDER_CATCH_ZONE_WIDTH // 2,
            C.SCREEN_HEIGHT - C.FIELDER_CATCH_ZONE_Y_FROM_BOTTOM,
            C.FIELDER_CATCH_ZONE_WIDTH,
            C.FIELDER_CATCH_ZONE_HEIGHT
        )

    def check_bat_ball_collision(self, baseball_obj: Baseball, batter_bat_rect: pygame.Rect, batter: Batter) -> bool:
        """
        Checks for collision between the baseball and the batter's bat.
        If collision occurs, updates baseball's velocity for a hit.
        """
        if baseball_obj.state != BaseballState.IN_FLIGHT or baseball_obj.is_hit:
            return False

        ball_rect = pygame.Rect(baseball_obj.position.x - baseball_obj.radius,
                                baseball_obj.position.y - baseball_obj.radius,
                                baseball_obj.radius * 2, baseball_obj.radius * 2)

        if batter_bat_rect.colliderect(ball_rect):
            baseball_obj.is_hit = True
            baseball_obj.state = BaseballState.IN_FLIGHT
            
            hit_direction = pygame.math.Vector2(random.uniform(C.BAT_HIT_DIRECTION_RANDOM_X_RANGE[0], C.BAT_HIT_DIRECTION_RANDOM_X_RANGE[1]), 
                                                random.uniform(C.BAT_HIT_DIRECTION_RANDOM_Y_RANGE[0], C.BAT_HIT_DIRECTION_RANDOM_Y_RANGE[1])).normalize()
            hit_speed = batter.batting_power * C.BAT_HIT_BASE_SPEED + baseball_obj.velocity.length() * C.BAT_HIT_BALL_SPEED_RETENTION

            hit_speed *= random.uniform(C.BAT_HIT_SPEED_RANDOM_FACTOR[0], C.BAT_HIT_SPEED_RANDOM_FACTOR[1])
            hit_direction.rotate_ip(random.uniform(C.BAT_HIT_DIRECTION_RANDOM_ANGLE[0], C.BAT_HIT_DIRECTION_RANDOM_ANGLE[1]))

            baseball_obj.velocity = hit_direction * hit_speed
            baseball_obj.acceleration = pygame.math.Vector2(0, C.GRAVITY)
            baseball_obj.spin_magnitude = 0.0
            return True
        return False

    def check_ball_field_boundaries(self, baseball_obj: Baseball) -> Optional[BaseballState]:
        """
        Checks if the baseball has gone foul, hit a home run, or is out of play.
        """
        if baseball_obj.state not in [BaseballState.IN_FLIGHT, BaseballState.GROUNDED]:
            return None

        # Check for home run
        if baseball_obj.position.y < self.home_run_wall_y and baseball_obj.velocity.y < C.HOME_RUN_MIN_Y_VELOCITY_FOR_HR and baseball_obj.is_hit:
           y_norm_factor = max(0.0, min(1.0, (self.ground_y - baseball_obj.position.y) / (self.ground_y - self.home_run_wall_y)))
           
           # Max X deviation for foul lines at the HR wall Y
           max_x_deviation_at_hr_wall = (C.SCREEN_WIDTH / 2) - C.FOUL_LINE_X_EXTENT

           current_left_foul_x = self.foul_line_left_x_at_ground - (max_x_deviation_at_hr_wall * y_norm_factor * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR)
           current_right_foul_x = self.foul_line_right_x_at_ground + (max_x_deviation_at_hr_wall * y_norm_factor * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR)

           if current_left_foul_x < baseball_obj.position.x < current_right_foul_x:
                return BaseballState.HOME_RUN
        
        # Check for foul lines
        if (baseball_obj.position - self.home_plate_pos_center).y < C.HIT_BALL_Y_THRESHOLD_FOR_FOUL_CHECK:
            foul_left_x_at_ball_y = C.SCREEN_WIDTH // 2 - C.FOUL_LINE_X_EXTENT - (self.ground_y - baseball_obj.position.y) * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR 
            foul_right_x_at_ball_y = C.SCREEN_WIDTH // 2 + C.FOUL_LINE_X_EXTENT + (self.ground_y - baseball_obj.position.y) * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR
            
            if not (foul_left_x_at_ball_y < baseball_obj.position.x < foul_right_x_at_ball_y):
                return BaseballState.FOUL

        # Check for ball leaving the game area completely (past general screen bounds)
        if (baseball_obj.position.x < -C.BALL_OUT_OF_BOUNDS_MARGIN or baseball_obj.position.x > C.SCREEN_WIDTH + C.BALL_OUT_OF_BOUNDS_MARGIN or
            baseball_obj.position.y < -C.BALL_OUT_OF_BOUNDS_MARGIN or baseball_obj.position.y > C.SCREEN_HEIGHT + C.BALL_OUT_OF_BOUNDS_MARGIN):
            return BaseballState.OUT_OF_PLAY
        
        return None

    def check_ball_strike_zone(self, baseball_obj: Baseball) -> Optional[BaseballState]:
        """
        Checks if the baseball has passed through or outside the strike zone.
        This is for pitches not hit by the batter.
        """
        if baseball_obj.state != BaseballState.IN_FLIGHT or baseball_obj.is_hit:
            return None

        if self.strike_zone_rect.collidepoint(baseball_obj.position):
            return BaseballState.STRIKE_ZONE
        
        if baseball_obj.position.y > self.strike_zone_rect.bottom + C.BALL_PASSED_STRIKE_ZONE_BUFFER:
             return BaseballState.BALL_ZONE
             
        return None

    def draw_field_boundaries(self, screen: pygame.Surface) -> None:
        # Foul lines
        left_foul_end_x = C.SCREEN_WIDTH // 2 - C.FOUL_LINE_X_EXTENT - (self.ground_y - C.HOME_RUN_WALL_Y_OFFSET + C.FOUL_LINE_Y_VISUAL_EXTENSION) * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR
        right_foul_end_x = C.SCREEN_WIDTH // 2 + C.FOUL_LINE_X_EXTENT + (self.ground_y - C.HOME_RUN_WALL_Y_OFFSET + C.FOUL_LINE_Y_VISUAL_EXTENSION) * C.FOUL_LINE_HR_WALL_X_DEVIATION_FACTOR
        
        pygame.draw.line(screen, C.LINE_COLOR, self.home_plate_pos_center,
                         (left_foul_end_x, C.HOME_RUN_WALL_Y_OFFSET - C.FOUL_LINE_Y_VISUAL_EXTENSION), 2)
        pygame.draw.line(screen, C.LINE_COLOR, self.home_plate_pos_center,
                         (right_foul_end_x, C.HOME_RUN_WALL_Y_OFFSET - C.FOUL_LINE_Y_VISUAL_EXTENSION), 2)
        
        # Home run wall
        pygame.draw.line(screen, C.LINE_COLOR, (left_foul_end_x, C.HOME_RUN_WALL_Y_OFFSET),
                         (right_foul_end_x, C.HOME_RUN_WALL_Y_OFFSET), 2)

        # Home plate
        pygame.draw.circle(screen, C.BASE_COLOR, (int(self.home_plate_pos_center.x), int(self.home_plate_pos_center.y)), C.HOME_PLATE_RADIUS)
        
        # Strike zone rect outline (for visual debugging/player reference)
        pygame.draw.rect(screen, C.STRIKE_ZONE_OUTLINE_COLOR, self.strike_zone_rect, 1)

class AtBatManager:
    """
    Manages the current at-bat, including balls, strikes, outs, runners on base,
    and handles scoring and inning progression.
    It does NOT manage the baseball physics or collision directly,
    but processes outcomes reported by the AtBatController.
    """
    def __init__(self, event_manager: EventManager, total_innings: int) -> None:
        self.event_manager = event_manager
        self.total_innings: int = total_innings
        self.current_inning: int = 1
        self.is_top_half: bool = True # True for top of inning (away team batting), False for bottom (home team batting)
        self.home_score: int = 0
        self.away_score: int = 0
        self.balls: int = 0
        self.strikes: int = 0
        self.outs: int = 0
        self.runners_on_base: Dict[BaseEnum, Optional[int]] = {BaseEnum.FIRST: None, BaseEnum.SECOND: None, BaseEnum.THIRD: None}
        self.active_batter_id: Optional[int] = None # ID of the current batter

    def reset_game_state(self, total_innings: int) -> None:
        """Resets all game state for a new game."""
        self.total_innings = total_innings
        self.current_inning = 1
        self.is_top_half = True
        self.home_score = 0
        self.away_score = 0
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.runners_on_base = {BaseEnum.FIRST: None, BaseEnum.SECOND: None, BaseEnum.THIRD: None}
        self.active_batter_id = None 
        self._update_ui_data() # Initial UI update

    def set_active_batter_id(self, batter_id: int) -> None:
        self.active_batter_id = batter_id

    def _update_ui_data(self) -> None:
        """Sends current game state data to the UISystem via EventManager."""
        self.event_manager.post("UPDATE_SCOREBOARD", {'HomeScore': self.home_score, 'AwayScore': self.away_score, 
                                                      'Inning': self.current_inning, 'IsTopHalf': self.is_top_half})
        self.event_manager.post("UPDATE_COUNT", {'Balls': self.balls, 'Strikes': self.strikes, 'Outs': self.outs})
        self.event_manager.post("UPDATE_RUNNERS", {'FirstBaseOccupied': self.runners_on_base[BaseEnum.FIRST] is not None,
                                                  'SecondBaseOccupied': self.runners_on_base[BaseEnum.SECOND] is not None,
                                                  'ThirdBaseOccupied': self.runners_on_base[BaseEnum.THIRD] is not None})

    def increment_ball(self) -> None:
        """Increments ball count and checks for walk outcome."""
        self.balls += 1
        self.event_manager.post("BALL", {'balls': self.balls})
        self._check_at_bat_outcome_pitch()
        self._update_ui_data()

    def increment_strike(self) -> None:
        """Increments strike count and checks for strikeout outcome."""
        self.strikes += 1
        self.event_manager.post("STRIKE", {'strikes': self.strikes})
        self._check_at_bat_outcome_pitch()
        self._update_ui_data()

    def handle_foul_ball(self) -> None:
        """Handles a foul ball, adding a strike if appropriate."""
        if self.strikes < C.MAX_STRIKES - 1: # Foul counts as a strike, unless already 2 strikes
            self.strikes += 1
            self.event_manager.post("STRIKE", {'strikes': self.strikes})
        self._update_ui_data()

    def _check_at_bat_outcome_pitch(self) -> None:
        """Checks for walk or strikeout immediately after a pitch (ball/strike count updated)."""
        if self.strikes >= C.MAX_STRIKES:
            self._end_at_bat('strikeout')
        elif self.balls >= C.MAX_BALLS:
            self._end_at_bat('walk')

    def _end_at_bat(self, outcome: str) -> None:
        """Resolves the current at-bat based on outcome and updates game state."""
        if outcome == 'strikeout':
            self.outs += 1
        elif outcome == 'walk':
            self._advance_runners(1)
        elif outcome == 'hit_single':
            self._advance_runners(1)
        elif outcome == 'hit_double':
            self._advance_runners(2)
        elif outcome == 'hit_triple':
            self._advance_runners(3)
        elif outcome == 'home_run':
            self._advance_runners(4)
        elif outcome == 'out': # Any other form of out (flyout, groundout, caught fly)
            self.outs += 1
        
        # After any at-bat resolution, reset counts
        self.balls = 0
        self.strikes = 0
        
        self._check_half_inning_end()
        self._update_ui_data()

    def _advance_runners(self, batter_bases_achieved: int) -> None:
        """
        Advances runners on base and scores.
        batter_bases_achieved: Number of bases the batter achieved (1 for single, 2 for double, 3 for triple, 4 for HR/walk).
        """
        score_this_play = 0
        
        active_runners_info = [] # List of (runner_id, current_base_number)
        # Fix: Removed extra single quote from BaseEnum keys
        if self.runners_on_base[BaseEnum.THIRD] is not None: active_runners_info.append((self.runners_on_base[BaseEnum.THIRD], 3))
        if self.runners_on_base[BaseEnum.SECOND] is not None: active_runners_info.append((self.runners_on_base[BaseEnum.SECOND], 2))
        if self.runners_on_base[BaseEnum.FIRST] is not None: active_runners_info.append((self.runners_on_base[BaseEnum.FIRST], 1))
        
        if self.active_batter_id is not None:
            active_runners_info.append((self.active_batter_id, 0)) # Add the current batter as starting at home plate

        active_runners_info.sort(key=lambda x: x[1], reverse=True) # Sort to handle advancement from further bases first
        
        # Track which bases are newly occupied
        temp_occupied_bases: Dict[int, Optional[int]] = {1: None, 2: None, 3: None}
        
        for runner_id, current_base_num in active_runners_info:
            target_base_num = current_base_num + batter_bases_achieved
            
            if target_base_num >= 4: # Runner scores if target is home plate or beyond
                score_this_play += 1
            else: # Runner lands on a base (1, 2, or 3)
                if temp_occupied_bases[target_base_num] is None:
                    temp_occupied_bases[target_base_num] = runner_id
                else:
                    score_this_play += 1 # If the target base is blocked, for simplicity, current runner scores. 

        self.runners_on_base[BaseEnum.FIRST] = temp_occupied_bases[1]
        self.runners_on_base[BaseEnum.SECOND] = temp_occupied_bases[2]
        self.runners_on_base[BaseEnum.THIRD] = temp_occupied_bases[3]

        if self.is_top_half:
            self.away_score += score_this_play
        else:
            self.home_score += score_this_play
        
        self.event_manager.post("SCORE_UPDATE", {'team': 'Away' if self.is_top_half else 'Home', 'runs': score_this_play})
        self._update_ui_data()

    def _check_half_inning_end(self) -> None:
        """Checks if 3 outs have been made, ending the current half-inning."""
        if self.outs >= C.MAX_OUTS:
            self.outs = 0
            self.balls = 0
            self.strikes = 0
            self.runners_on_base = {BaseEnum.FIRST: None, BaseEnum.SECOND: None, BaseEnum.THIRD: None}

            self.is_top_half = not self.is_top_half
            if self.is_top_half:
                self.current_inning += 1
            
            self.event_manager.post("HALF_INNING_END", {'current_inning': self.current_inning, 'is_top_half': self.is_top_half})
            
            self._check_game_end()
            self._update_ui_data()

    def _check_game_end(self) -> None:
        """Determines if the game has ended based on innings and score."""
        game_over = False
        winner_text = ""
        score_text = f"主隊: {self.home_score} 客隊: {self.away_score}"

        if self.current_inning > self.total_innings and self.home_score != self.away_score:
            game_over = True
        elif self.current_inning > self.total_innings and self.home_score == self.away_score and not self.is_top_half: 
             game_over = True
        
        if not self.is_top_half and self.current_inning >= self.total_innings and self.home_score > self.away_score:
            game_over = True 

        if game_over:
            if self.home_score > self.away_score:
                winner_text = "主隊獲勝!"
            elif self.away_score > self.home_score:
                winner_text = "客隊獲勝!"
            else:
                winner_text = "平手!"
            self.event_manager.post("GAME_OVER_INFO", {'winner': winner_text, 'score_text': score_text})

class AtBatController:
    """
    Manages the lifecycle of a single at-bat, from pitch generation to play resolution.
    It encapsulates the logic for ball physics, collisions, AI decisions, and reporting outcomes
    to the AtBatManager.
    """
    def __init__(self, event_manager: EventManager, collision_manager: CollisionManager, 
                 ai_manager: AIManager, at_bat_manager: AtBatManager, 
                 baseball_pool: GenericObjectPool) -> None:
        self.event_manager = event_manager
        self.collision_manager = collision_manager
        self.ai_manager = ai_manager
        self.at_bat_manager = at_bat_manager
        self.baseball_pool = baseball_pool

        self.player_char: Optional[Player] = None
        self.ai_char: Optional[Player] = None
        self.game_mode: GameMode = GameMode.PLAYER_BATTING # Placeholder, will be set by PlayGameState

        self.current_baseball: Optional[Baseball] = None
        self.ball_in_play: bool = False
        self.batter_has_swung: bool = False # Tracks if the current batter (player or AI) has swung
        self.ball_at_plate_predicted_time: float = 0.0

        # Player Pitcher specific UI state
        self.player_pitcher_target_rect: pygame.Rect = pygame.Rect(
            C.SCREEN_WIDTH // 2 - C.STRIKE_ZONE_WIDTH // 2,
            C.SCREEN_HEIGHT - C.STRIKE_ZONE_Y_FROM_BOTTOM,
            C.STRIKE_ZONE_WIDTH,
            C.STRIKE_ZONE_HEIGHT
        )
        self.player_pitcher_selected_pitch_type: PitchType = PitchType.FASTBALL

    def reset_at_bat(self, game_mode: GameMode, player_char: Player, ai_char: Player) -> None:
        """Resets state for a new at-bat."""
        self.player_char = player_char
        self.ai_char = ai_char
        self.game_mode = game_mode

        self.baseball_pool.clear_active()
        self.current_baseball = None
        self.ball_in_play = False
        self.batter_has_swung = False
        self.ball_at_plate_predicted_time = 0.0

        if isinstance(player_char, Pitcher): # If player is pitching, set initial pitch type
             self.player_pitcher_selected_pitch_type = player_char.available_pitches[0]

        self._update_ui_for_mode()
        self.at_bat_manager.set_active_batter_id(player_char.id if game_mode == GameMode.PLAYER_BATTING else ai_char.id)


    def _update_ui_for_mode(self) -> None:
        """Updates UI elements based on current game mode (pitcher/batter)."""
        if self.player_char and isinstance(self.player_char, Pitcher):
            self.event_manager.post("SET_PITCH_SELECTION", {'options': self.player_char.available_pitches, 'selected_type': self.player_pitcher_selected_pitch_type})
            self.event_manager.post("SET_PITCH_TARGET", self.player_pitcher_target_rect)
        else:
            self.event_manager.post("SET_PITCH_SELECTION", {'options': [], 'selected_type': None})
            self.event_manager.post("SET_PITCH_TARGET", None)
        self.at_bat_manager._update_ui_data()

    def handle_player_pitch_input(self, event: pygame.event.Event, current_time: float) -> None:
        """Handles player input when in pitching mode."""
        if not self.ball_in_play and self.player_char and isinstance(self.player_char, Pitcher):
            if event.key == pygame.K_a:
                self.player_pitcher_target_rect.x = max(0, self.player_pitcher_target_rect.x - C.PITCH_TARGET_MOVE_AMOUNT)
            elif event.key == pygame.K_d:
                self.player_pitcher_target_rect.x = min(C.SCREEN_WIDTH - self.player_pitcher_target_rect.width, self.player_pitcher_target_rect.x + C.PITCH_TARGET_MOVE_AMOUNT)
            elif event.key == pygame.K_w:
                self.player_pitcher_target_rect.y = max(C.PITCH_TARGET_Y_MIN, self.player_pitcher_target_rect.y - C.PITCH_TARGET_MOVE_AMOUNT)
            elif event.key == pygame.K_s:
                self.player_pitcher_target_rect.y = min(C.PITCH_TARGET_Y_MAX, self.player_pitcher_target_rect.y + C.PITCH_TARGET_MOVE_AMOUNT)
            elif event.key == pygame.K_z:
                self.player_pitcher_selected_pitch_type = PitchType.FASTBALL
            elif event.key == pygame.K_x:
                self.player_pitcher_selected_pitch_type = PitchType.CURVEBALL
            elif event.key == pygame.K_c:
                self.player_pitcher_selected_pitch_type = PitchType.SLIDER
            elif event.key == pygame.K_v:
                self.player_pitcher_selected_pitch_type = PitchType.CHANGEUP
            elif event.key == pygame.K_SPACE:
                self.current_baseball = self.player_char.throw_ball(current_time, 
                                                                     pygame.math.Vector2(self.player_pitcher_target_rect.center), 
                                                                     self.player_pitcher_selected_pitch_type, self.baseball_pool)
                if self.current_baseball:
                    self.ball_in_play = True
                    self.ball_at_plate_predicted_time = self._predict_ball_arrival_time(self.current_baseball, current_time)

            self._update_ui_for_mode()

    def handle_player_batter_swing(self) -> None:
        """Processes player's swing input."""
        if not self.batter_has_swung and self.ball_in_play and self.player_char and isinstance(self.player_char, Batter):
            self.player_char.swing_bat()
            self.batter_has_swung = True # Mark that player has swung

    def update(self, dt: float, current_time: float) -> None:
        """Updates the current at-bat logic."""
        if self.player_char: self.player_char.update(dt)
        if self.ai_char: self.ai_char.update(dt)

        # Handle AI pitcher throwing if player is batting and no ball is in play
        if not self.ball_in_play and self.game_mode == GameMode.PLAYER_BATTING and self.ai_char and isinstance(self.ai_char, Pitcher):
            if current_time - self.ai_char.last_pitch_time > self.ai_char.pitch_rate_limit:
                pitch_type, target_pos = self.ai_manager.ai_pitcher_decide_pitch(self.ai_char)
                self.current_baseball = self.ai_char.throw_ball(current_time, target_pos, pitch_type, self.baseball_pool)
                if self.current_baseball:
                    self.ball_in_play = True
                    self.batter_has_swung = False # Reset swing state for this pitch
                    self.ball_at_plate_predicted_time = self._predict_ball_arrival_time(self.current_baseball, current_time)
        
        # Process active baseballs
        for baseball_obj in list(self.baseball_pool.get_active()):
            if baseball_obj.state == BaseballState.OUT_OF_PLAY:
                if baseball_obj == self.current_baseball and baseball_obj.has_bounced: # This implies it came to a rest after being hit
                    self._resolve_hit_ball_outcome(baseball_obj)
                self.baseball_pool.recycle(baseball_obj)
                if baseball_obj == self.current_baseball:
                    self.current_baseball = None
                    self.ball_in_play = False
                    self._reset_for_next_pitch()
                continue

            baseball_obj.update(dt, self.collision_manager.ground_y)

            # AI batter swing logic for player pitching mode
            if self.current_baseball == baseball_obj and self.game_mode == GameMode.PLAYER_PITCHING \
               and self.ai_char and isinstance(self.ai_char, Batter) and not baseball_obj.is_hit and not self.batter_has_swung:
                if self.ai_manager.ai_batter_decide_swing(self.ai_char, baseball_obj):
                    self.ai_char.swing_bat()
                    self.batter_has_swung = True

            # Collision with bat (for both player and AI batter)
            active_batter = self.player_char if self.game_mode == GameMode.PLAYER_BATTING else self.ai_char
            if self.current_baseball == baseball_obj and active_batter and isinstance(active_batter, Batter) and active_batter.is_swinging and not baseball_obj.is_hit:
                bat_hitbox = active_batter.get_bat_hitbox()
                if bat_hitbox and self.collision_manager.check_bat_ball_collision(baseball_obj, bat_hitbox, active_batter):
                    baseball_obj.owner_id = active_batter.id # Set owner to the batter who hit it
                    self.ball_at_plate_predicted_time = 0.0 # Hit, so prediction is no longer relevant
                    self.ball_in_play = True # Still in play, but now a hit ball
                    self.event_manager.post("BALL_HIT", {'batter_id': active_batter.id}) # Notify others of a hit
            
            # If ball hasn't been hit yet, check for strike/ball decision once it passes home plate
            if self.current_baseball == baseball_obj and baseball_obj.state == BaseballState.IN_FLIGHT \
               and not baseball_obj.is_hit and baseball_obj.position.y > self.collision_manager.strike_zone_rect.bottom + C.BALL_PASSED_STRIKE_ZONE_BUFFER:
                
                strike_zone_outcome = self.collision_manager.check_ball_strike_zone(baseball_obj)
                
                did_batter_swing = active_batter.is_swinging if active_batter else False

                if did_batter_swing: # Batter swung and missed
                    self.at_bat_manager.increment_strike()
                else: # Batter did not swing
                    if strike_zone_outcome == BaseballState.STRIKE_ZONE: # Didn't swing at a strike
                        self.at_bat_manager.increment_strike()
                    else: # Didn't swing at a ball
                        self.at_bat_manager.increment_ball()
                
                baseball_obj.state = BaseballState.OUT_OF_PLAY # End the pitch
                self._reset_for_next_pitch()
                continue

            # Check field boundaries for hit balls
            if self.current_baseball == baseball_obj and baseball_obj.is_hit:
                boundary_result = self.collision_manager.check_ball_field_boundaries(baseball_obj)
                if boundary_result == BaseballState.HOME_RUN:
                    baseball_obj.state = BaseballState.OUT_OF_PLAY
                    self.at_bat_manager._end_at_bat('home_run')
                    self._reset_for_next_pitch()
                    continue
                elif boundary_result == BaseballState.FOUL:
                    baseball_obj.state = BaseballState.OUT_OF_PLAY
                    self.at_bat_manager.handle_foul_ball()
                    self._reset_for_next_pitch()
                    continue
                elif boundary_result == BaseballState.OUT_OF_PLAY: # Generic out of play for a hit ball
                    baseball_obj.state = BaseballState.OUT_OF_PLAY
                    self.at_bat_manager._end_at_bat('out') # Could be a flyout, groundout etc. if off-screen
                    self._reset_for_next_pitch()
                    continue

            # Simplified fielding/catch logic: if a hit ball enters a "fielder's zone" and is in flight
            if self.current_baseball == baseball_obj and baseball_obj.is_hit and baseball_obj.state == BaseballState.IN_FLIGHT:
                ball_hitbox = pygame.Rect(baseball_obj.position.x - baseball_obj.radius, baseball_obj.position.y - baseball_obj.radius, baseball_obj.radius*2, baseball_obj.radius*2)
                if self.collision_manager.fielder_catch_zone_rect.colliderect(ball_hitbox) and random.random() < C.AI_FIELDER_CATCH_CHANCE:
                    baseball_obj.state = BaseballState.OUT_OF_PLAY
                    self.at_bat_manager._end_at_bat('out') # Caught is an out
                    self._reset_for_next_pitch()
                    continue

    def _predict_ball_arrival_time(self, ball_obj: Baseball, current_game_time: float) -> float:
        """
        Simulates the ball's trajectory to predict when it will reach the center of the strike zone.
        Used for AI/player batting timing.
        """
        if ball_obj is None:
            return 0.0

        temp_ball = Baseball()
        temp_ball.reset(ball_obj.position, ball_obj.velocity, ball_obj.pitch_type, ball_obj.spin_magnitude, ball_obj.owner_id)
        
        sim_dt = C.BALL_PREDICT_SIM_DT
        sim_time = 0.0
        
        strike_zone_center_y = self.collision_manager.strike_zone_rect.centery
        while temp_ball.position.y < strike_zone_center_y and sim_time < C.BALL_PREDICT_MAX_SIM_TIME:
            temp_ball.update(sim_dt, self.collision_manager.ground_y)
            sim_time += sim_dt
            
        if sim_time >= C.BALL_PREDICT_MAX_SIM_TIME:
            return 0.0
        
        return current_game_time + sim_time

    def _resolve_hit_ball_outcome(self, baseball_obj: Baseball) -> None:
        """Resolves the outcome for a ball that was hit and has now come to rest."""
        home_plate_pos = self.collision_manager.home_plate_pos_center
        distance_hit = (baseball_obj.position - home_plate_pos).length()
        
        if distance_hit > C.HIT_TRIPLE_DISTANCE_THRESHOLD: 
            self.at_bat_manager._end_at_bat('hit_triple') 
        elif distance_hit > C.HIT_DOUBLE_DISTANCE_THRESHOLD:
            self.at_bat_manager._end_at_bat('hit_double')
        else:
            self.at_bat_manager._end_at_bat('hit_single')

    def _reset_for_next_pitch(self) -> None:
        """Cleans up after a pitch/play, preparing for the next one."""
        if self.current_baseball:
            self.baseball_pool.recycle(self.current_baseball)
            self.current_baseball = None
        self.ball_in_play = False
        self.batter_has_swung = False
        self.ball_at_plate_predicted_time = 0.0
        self._update_ui_for_mode()

class GameState:
    """Abstract base class for all game states."""
    def __init__(self, game: Any) -> None:
        self.game = game
    def enter(self, data: Optional[Any] = None) -> None: pass
    def exit(self) -> None: pass
    def handle_input(self, event: pygame.event.Event) -> None: pass
    def update(self, dt: float) -> None: pass
    def draw(self, screen: pygame.Surface) -> None: pass

class MainMenuState(GameState):
    def __init__(self, game: Any) -> None:
        super().__init__(game)
        self.play_button_rect: pygame.Rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2, C.SCREEN_HEIGHT // 2 - C.MENU_CENTER_OFFSET, C.BUTTON_WIDTH, C.BUTTON_HEIGHT)
        self.rules_button_rect: pygame.Rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2, self.play_button_rect.y + C.MENU_BUTTON_Y_SPACING, C.BUTTON_WIDTH, C.BUTTON_HEIGHT)
        self.exit_button_rect: pygame.Rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2, self.rules_button_rect.y + C.MENU_BUTTON_Y_SPACING, C.BUTTON_WIDTH, C.BUTTON_HEIGHT)

    def enter(self, data: Optional[Any] = None) -> None:
        pygame.mixer.music.stop()

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.play_button_rect.collidepoint(event.pos):
                    self.game.state_machine.change_state(GameStateEnum.GAME_LOBBY)
                elif self.rules_button_rect.collidepoint(event.pos):
                    self.game.state_machine.change_state(GameStateEnum.RULES)
                elif self.exit_button_rect.collidepoint(event.pos):
                    self.game.running = False

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(C.SKY_COLOR)
        
        title_text = self.game.fonts['xl'].render("經典棒球對決", True, C.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        self.game.ui_system.draw_menu_button(screen, "開始遊戲", self.play_button_rect, self.play_button_rect.collidepoint(mouse_pos))
        self.game.ui_system.draw_menu_button(screen, "規則說明", self.rules_button_rect, self.rules_button_rect.collidepoint(mouse_pos))
        self.game.ui_system.draw_menu_button(screen, "離開遊戲", self.exit_button_rect, self.exit_button_rect.collidepoint(mouse_pos))

class RulesDisplayState(GameState):
    def enter(self, data: Optional[Any] = None) -> None:
        self.game.ui_system.scroll_offset = 0

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game.ui_system.scroll_offset = min(0, self.game.ui_system.scroll_offset + self.game.ui_system.line_height * C.RULES_SCROLL_SPEED_LINES)
            elif event.key == pygame.K_DOWN:
                max_scroll_height = len(self.game.ui_system.rules_text) * self.game.ui_system.line_height
                visible_height = C.SCREEN_HEIGHT - C.RULES_TEXT_MARGIN_Y * 2
                if max_scroll_height > visible_height:
                    max_scroll_offset = max_scroll_height - visible_height
                    self.game.ui_system.scroll_offset = max(-max_scroll_offset, self.game.ui_system.scroll_offset - self.game.ui_system.line_height * C.RULES_SCROLL_SPEED_LINES)
                else:
                    self.game.ui_system.scroll_offset = 0
            else:
                self.game.state_machine.change_state(GameStateEnum.MAIN_MENU)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.state_machine.change_state(GameStateEnum.MAIN_MENU)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        self.game.ui_system.draw_rules_page(screen)

class GameLobbyState(GameState):
    def __init__(self, game: Any) -> None:
        super().__init__(game)
        self.player_role_choice: PlayerRole = PlayerRole.BATTER
        self.innings_choice: int = C.DEFAULT_INNINGS

        self.batter_btn_rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.SMALL_BUTTON_WIDTH - C.GAME_LOBBY_BUTTON_SPACING_X, C.SCREEN_HEIGHT // 2 - C.MENU_CENTER_OFFSET * 2, C.SMALL_BUTTON_WIDTH, C.BUTTON_HEIGHT)
        self.pitcher_btn_rect = pygame.Rect(C.SCREEN_WIDTH // 2 + C.GAME_LOBBY_BUTTON_SPACING_X, C.SCREEN_HEIGHT // 2 - C.MENU_CENTER_OFFSET * 2, C.SMALL_BUTTON_WIDTH, C.BUTTON_HEIGHT)
        
        self.innings_5_btn_rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.SMALL_BUTTON_WIDTH - C.GAME_LOBBY_BUTTON_SPACING_X, self.batter_btn_rect.y + C.MENU_BUTTON_Y_SPACING, C.SMALL_BUTTON_WIDTH // 2, C.BUTTON_HEIGHT)
        self.innings_9_btn_rect = pygame.Rect(self.innings_5_btn_rect.x + C.SMALL_BUTTON_WIDTH // 2 + C.GAME_LOBBY_BUTTON_SPACING_X_SMALL, self.batter_btn_rect.y + C.MENU_BUTTON_Y_SPACING, C.SMALL_BUTTON_WIDTH // 2, C.BUTTON_HEIGHT)
        
        self.start_game_btn_rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2, self.innings_5_btn_rect.y + C.MENU_BUTTON_Y_SPACING * 2, C.BUTTON_WIDTH, C.BUTTON_HEIGHT)
        self.back_btn_rect = pygame.Rect(C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2, self.start_game_btn_rect.y + C.MENU_BUTTON_Y_SPACING, C.BUTTON_WIDTH, C.BUTTON_HEIGHT)

    def enter(self, data: Optional[Any] = None) -> None:
        self.player_role_choice = PlayerRole.BATTER
        self.innings_choice = C.DEFAULT_INNINGS

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.batter_btn_rect.collidepoint(mouse_pos):
                self.player_role_choice = PlayerRole.BATTER
            elif self.pitcher_btn_rect.collidepoint(mouse_pos):
                self.player_role_choice = PlayerRole.PITCHER
            elif self.innings_5_btn_rect.collidepoint(mouse_pos):
                self.innings_choice = C.MIN_INNINGS_CHOICE
            elif self.innings_9_btn_rect.collidepoint(mouse_pos):
                self.innings_choice = C.MAX_INNINGS_CHOICE
            elif self.start_game_btn_rect.collidepoint(mouse_pos):
                self.game.state_machine.change_state(GameStateEnum.PLAYING, 
                                                     {'player_role': self.player_role_choice,
                                                      'total_innings': self.innings_choice})
            elif self.back_btn_rect.collidepoint(mouse_pos):
                self.game.state_machine.change_state(GameStateEnum.MAIN_MENU)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(C.UI_BG_COLOR)

        title_text = self.game.fonts['lg'].render("遊戲設定", True, C.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        role_text = self.game.fonts['md'].render("選擇角色:", True, C.TEXT_COLOR)
        screen.blit(role_text, (C.SCREEN_WIDTH // 2 - C.GAME_LOBBY_ROLE_TEXT_OFFSET_X, self.batter_btn_rect.centery - self.game.fonts['md'].get_height() // 2))

        mouse_pos = pygame.mouse.get_pos()
        self.game.ui_system.draw_selection_button(screen, "打者", self.batter_btn_rect, 
                                                  self.player_role_choice == PlayerRole.BATTER, 
                                                  self.batter_btn_rect.collidepoint(mouse_pos))
        self.game.ui_system.draw_selection_button(screen, "投手", self.pitcher_btn_rect, 
                                                  self.player_role_choice == PlayerRole.PITCHER, 
                                                  self.pitcher_btn_rect.collidepoint(mouse_pos))

        innings_text = self.game.fonts['md'].render("總局數:", True, C.TEXT_COLOR)
        screen.blit(innings_text, (C.SCREEN_WIDTH // 2 - C.GAME_LOBBY_ROLE_TEXT_OFFSET_X, self.innings_5_btn_rect.centery - self.game.fonts['md'].get_height() // 2))

        self.game.ui_system.draw_selection_button(screen, f"{C.MIN_INNINGS_CHOICE} 局", self.innings_5_btn_rect, 
                                                  self.innings_choice == C.MIN_INNINGS_CHOICE, 
                                                  self.innings_5_btn_rect.collidepoint(mouse_pos))
        self.game.ui_system.draw_selection_button(screen, f"{C.MAX_INNINGS_CHOICE} 局", self.innings_9_btn_rect, 
                                                  self.innings_choice == C.MAX_INNINGS_CHOICE, 
                                                  self.innings_9_btn_rect.collidepoint(mouse_pos))
        
        self.game.ui_system.draw_menu_button(screen, "開始比賽", self.start_game_btn_rect, self.start_game_btn_rect.collidepoint(mouse_pos))
        self.game.ui_system.draw_menu_button(screen, "返回主選單", self.back_btn_rect, self.back_btn_rect.collidepoint(mouse_pos))

class PlayGameState(GameState):
    def __init__(self, game: Any) -> None:
        super().__init__(game)
        
        self.player_char: Optional[Player] = None
        self.ai_char: Optional[Player] = None
        self.game_mode: GameMode = GameMode.PLAYER_BATTING # Placeholder

        self.player_pitcher_pos: pygame.math.Vector2 = pygame.math.Vector2(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT - C.PITCHER_POS_Y_OFFSET)
        self.player_batter_pos: pygame.math.Vector2 = pygame.math.Vector2(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT - C.BATTER_POS_Y_OFFSET)

        self.at_bat_controller: AtBatController = AtBatController(
            self.game.event_manager, self.game.collision_manager, 
            self.game.ai_manager, self.game.at_bat_manager, 
            GenericObjectPool(Baseball, initial_size=C.MAX_BALLS) 
        )
        
        self.game.event_manager.subscribe("HALF_INNING_END", self.handle_half_inning_end)
        self.game.event_manager.subscribe("GAME_OVER_INFO", self.handle_game_over_event)

    def enter(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Initializes game state when entering the playing screen."""
        player_role_choice = data.get('player_role', PlayerRole.BATTER)
        total_innings = data.get('total_innings', C.DEFAULT_INNINGS)

        self.game.at_bat_manager.reset_game_state(total_innings)
        
        self._setup_players_for_half_inning(player_role_choice, C.HOME_TEAM_ID, self.game.at_bat_manager.is_top_half)

        # Pass the initialized player/AI characters to the AtBatController
        if self.player_char and self.ai_char:
            self.at_bat_controller.reset_at_bat(self.game_mode, self.player_char, self.ai_char)
        else:
            # Handle error or provide a default fallback if player/ai chars are not initialized.
            # For now, this should not happen with current logic.
            pass


    def exit(self) -> None:
        """Cleans up resources when leaving the playing screen."""
        self.at_bat_controller.baseball_pool.clear_active()
        self.game.ui_system.set_pitch_target(None)
        self.game.ui_system.set_pitch_selection_options({'options': [], 'selected_type': None})
        self.game.ui_system.set_game_over_info(None)

    def _setup_players_for_half_inning(self, player_initial_role_choice: PlayerRole, player_team_id: str, is_top_half: bool) -> None:
        """Sets up player and AI characters based on the current half-inning and player's chosen role."""
        if player_initial_role_choice == PlayerRole.BATTER: 
            if is_top_half: # AI (Away) bats, Player's team (Home) pitches. Player controls pitcher.
                self.player_char = Pitcher(player_team_id, self.player_pitcher_pos)
                self.ai_char = Batter(C.AWAY_TEAM_ID, self.player_batter_pos)
                self.game_mode = GameMode.PLAYER_PITCHING
            else: # Player's team (Home) bats, AI (Away) pitches. Player controls batter.
                self.player_char = Batter(player_team_id, self.player_batter_pos)
                self.ai_char = Pitcher(C.AWAY_TEAM_ID, self.player_pitcher_pos)
                self.game_mode = GameMode.PLAYER_BATTING
        else: # Player initial role choice is Pitcher
            if is_top_half: # Player's team (Home) pitches, AI (Away) bats. Player controls pitcher.
                self.player_char = Pitcher(player_team_id, self.player_pitcher_pos)
                self.ai_char = Batter(C.AWAY_TEAM_ID, self.player_batter_pos)
                self.game_mode = GameMode.PLAYER_PITCHING
            else: # AI (Away) pitches, Player's team (Home) bats. Player controls batter (even if chose pitcher initially).
                  # This is a key design decision. Player's *role* switches with the half-inning to keep them active.
                self.player_char = Batter(player_team_id, self.player_batter_pos)
                self.ai_char = Pitcher(C.AWAY_TEAM_ID, self.player_pitcher_pos)
                self.game_mode = GameMode.PLAYER_BATTING
        
    # --- Event Handlers from AtBatManager ---
    def handle_half_inning_end(self, data: Dict[str, Any]) -> None:
        """Switches player/AI roles and resets for the next half-inning."""
        # The player's *chosen* role remains, but their *active* role switches with the half-inning.
        # This logic determines who the player controls in the next half.
        
        # We need the original player_role_choice from GameLobbyState, but it's not directly accessible here.
        # A better way would be to store the player's initial preference in the `Game` object.
        # For now, let's infer based on the current `player_char` and `game_mode`.
        player_initial_role_choice = PlayerRole.BATTER # Default if inference fails
        if self.game_mode == GameMode.PLAYER_PITCHING and isinstance(self.player_char, Pitcher):
            player_initial_role_choice = PlayerRole.PITCHER
        elif self.game_mode == GameMode.PLAYER_BATTING and isinstance(self.player_char, Batter):
            player_initial_role_choice = PlayerRole.BATTER
        
        player_team_id = self.player_char.team_id if self.player_char else C.HOME_TEAM_ID 
        is_top_half = data['is_top_half']
        
        self._setup_players_for_half_inning(player_initial_role_choice, player_team_id, is_top_half)
        
        # After setting up new player/AI characters, reset the AtBatController
        if self.player_char and self.ai_char:
            self.at_bat_controller.reset_at_bat(self.game_mode, self.player_char, self.ai_char)
        

    def handle_game_over_event(self, data: Dict[str, str]) -> None:
        """Transitions to the game over state."""
        self.game.state_machine.change_state(GameStateEnum.GAME_OVER, data)

    # --- Input Handling ---
    def handle_input(self, event: pygame.event.Event) -> None:
        current_time = pygame.time.get_ticks() / 1000.0
        if self.game_mode == GameMode.PLAYER_PITCHING:
            self.at_bat_controller.handle_player_pitch_input(event, current_time)
        elif self.game_mode == GameMode.PLAYER_BATTING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.at_bat_controller.handle_player_batter_swing()

    # --- Game Logic Update ---
    def update(self, dt: float) -> None:
        current_time = pygame.time.get_ticks() / 1000.0
        self.at_bat_controller.update(dt, current_time)
        # Player and AI char are updated within at_bat_controller.update already.

    def draw(self, screen: pygame.Surface) -> None:
        """Draws game elements to the screen."""
        screen.fill(C.SKY_COLOR)
        pygame.draw.rect(screen, C.FIELD_COLOR, (0, C.SCREEN_HEIGHT - C.FIELD_BACKGROUND_HEIGHT, C.SCREEN_WIDTH, C.FIELD_BACKGROUND_HEIGHT))
        
        self.game.collision_manager.draw_field_boundaries(screen)

        if self.player_char: self.player_char.draw(screen)
        if self.ai_char: self.ai_char.draw(screen)
        
        for baseball_obj in self.at_bat_controller.baseball_pool.get_active():
            baseball_obj.draw(screen)

        self.game.ui_system.draw_scoreboard(screen)
        self.game.ui_system.draw_count_and_runners(screen)
        self.game.ui_system.draw_pitch_selection_ui(screen)
        self.game.ui_system.draw_pitch_target_ui(screen)

class GameOverState(GameState):
    def enter(self, data: Optional[Dict[str, str]] = None) -> None:
        if data:
            self.game.ui_system.set_game_over_info(data)
    
    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.game.state_machine.change_state(GameStateEnum.MAIN_MENU)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        self.game.ui_system.draw_game_over_screen(screen)

class GameStateMachine:
    """
    Manages the overall game state transitions using a dictionary mapping of GameStateEnum to GameState objects.
    """
    def __init__(self, game: Any) -> None:
        self.game = game
        self.states: Dict[GameStateEnum, GameState] = {
            GameStateEnum.MAIN_MENU: MainMenuState(game),
            GameStateEnum.RULES: RulesDisplayState(game),
            GameStateEnum.GAME_LOBBY: GameLobbyState(game),
            GameStateEnum.PLAYING: PlayGameState(game),
            GameStateEnum.GAME_OVER: GameOverState(game),
        }
        self.current_state: Optional[GameState] = None
        self.change_state(GameStateEnum.MAIN_MENU) # Set initial game state

    def change_state(self, new_state_enum: GameStateEnum, data: Optional[Any] = None) -> None:
        """Transitions to a new game state."""
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[new_state_enum]
        self.current_state.enter(data)

    def handle_input(self, event: pygame.event.Event) -> None:
        if self.current_state:
            self.current_state.handle_input(event)

    def update(self, dt: float) -> None:
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        if self.current_state:
            self.current_state.draw(screen)

# --- Main Game Class ---

class Game:
    """
    The main game class, orchestrating all game systems and the game loop.
    """
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.running: bool = True
        self.screen: pygame.Surface = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption("經典棒球對決")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.fonts: Dict[str, pygame.font.Font] = {
            'sm': pygame.font.Font(None, C.FONT_SIZE_SMALL),
            'md': pygame.font.Font(None, C.FONT_SIZE_MEDIUM),
            'lg': pygame.font.Font(None, C.FONT_SIZE_LARGE),
            'xl': pygame.font.Font(None, C.FONT_SIZE_XLARGE),
        }
        
        self.event_manager: EventManager = EventManager() 
        self.ui_system: UISystem = UISystem(self.event_manager, self.fonts)
        self.collision_manager: CollisionManager = CollisionManager()
        self.ai_manager: AIManager = AIManager(self.event_manager, self.collision_manager)
        self.at_bat_manager: AtBatManager = AtBatManager(self.event_manager, C.DEFAULT_INNINGS) 
        
        self.state_machine: GameStateMachine = GameStateMachine(self)

    def run(self) -> None:
        """The main game loop."""
        while self.running:
            dt = self.clock.tick(C.FPS) / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state_machine.handle_input(event)

            self.state_machine.update(dt)
            self.state_machine.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()