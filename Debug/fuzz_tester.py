# fuzz_tester.py
import os
import sys
import re
import subprocess
import random

# 定義要注入的 Chaos Payload 
CHAOS_PAYLOAD = """
# --- [INJECTED FUZZER CODE] START ---
import sys as _sys
import random as _random
import pygame as _pygame

class _ChaosAgent:
    def __init__(self, duration_sec=5.0):
        self.start_t = _pygame.time.get_ticks()
        self.end_t = self.start_t + (duration_sec * 1000)

    def update(self):
        # 1. 時間檢查 (Timeout Check)
        if _pygame.time.get_ticks() > self.end_t:
            print("[FUZZ] SUCCESS: Test Passed cleanly.")
            _pygame.quit()
            _sys.exit(0) # 正常退出 (Exit Code 0)
            
        # 2. 隨機輸入干擾 (Fuzzing)
        if _random.random() < 0.1: # 10% 機率亂按 (提高頻率測試穩定性)
            try:
                # 模擬隨機按鍵事件
                keys = [_pygame.K_LEFT, _pygame.K_RIGHT, _pygame.K_UP, _pygame.K_DOWN, _pygame.K_SPACE, _pygame.K_z, _pygame.K_x]
                _pygame.event.post(_pygame.event.Event(_pygame.KEYDOWN, key=_random.choice(keys)))
            except:
                pass
# 初始化測試員
_tester = _ChaosAgent(duration_sec=5.0)
# --- [INJECTED FUZZER CODE] END ---
"""

# ==========================================
# 2. 注入器邏輯
# ==========================================
def inject_fuzz_code(source_code: str) -> str:
    """將 Fuzz 測試代碼注入到原始遊戲代碼中"""
    injected_code = source_code

    # A. 插入 Class 定義
    if "import pygame" in injected_code:
        # 使用正則表達式，插在 import pygame 之後
        injected_code = re.sub(r"(import\s+pygame.*)", r"\1\n" + CHAOS_PAYLOAD, injected_code, count=1)
    else:
        injected_code = "import pygame\n" + CHAOS_PAYLOAD + "\n" + injected_code

    # B. 插入執行掛鉤 (Hook into Game Loop)
    hook_code = "_tester.update(); "
    
    if "pygame.display.update()" in injected_code:
        injected_code = injected_code.replace("pygame.display.update()", hook_code + "pygame.display.update()")
    elif "pygame.display.flip()" in injected_code:
        injected_code = injected_code.replace("pygame.display.flip()", hook_code + "pygame.display.flip()")
    
    return injected_code

# ==========================================
# 3. 執行 Fuzz 測試
# ==========================================
def run_fuzz_test(full_path: str) -> dict:
    folder = os.path.dirname(full_path)      
    filename = os.path.basename(full_path) 
    
    print(f"💣 [Fuzzer] 正在對 {filename} 進行壓力測試 (Injection Mode)...")

    # 1. 讀取原始碼
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            original_code = f.read()
    except Exception as e:
        return {"state": False, "Text": f"File Read Error: {str(e)}"}
    
    # 2. 注入測試碼
    tested_code = inject_fuzz_code(original_code)
    
    # 3. 建立暫存檔
    temp_filename = f"_fuzz_{filename}"
    temp_full_path = os.path.join(folder, temp_filename)
    
    with open(temp_full_path, "w", encoding="utf-8") as f:
        f.write(tested_code)

    # 4. 設定環境變數 (關閉音效)
    my_env = os.environ.copy()
    my_env["SDL_AUDIODRIVER"] = "dummy"

    try:
        # 5. 執行測試
        result = subprocess.run(
            [sys.executable, temp_filename],
            capture_output=True,
            text=True,
            cwd=folder,
            timeout=10, # 外部保險超時
            env=my_env,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 清理暫存檔
        if os.path.exists(temp_full_path):
            os.remove(temp_full_path)

        # 6. 判斷結果
        if result.returncode == 0 and "[FUZZ] SUCCESS" in result.stdout:
            print("✨ Fuzz 測試通過：遊戲能承受隨機輸入攻擊。")
            return {
                "state": True,
                "Text": None
            }
        else:
            print("💥 Fuzz 測試失敗：遊戲在亂按之下崩潰了。")
            error_log = f"Fuzz Test Failed.\n[Stderr]:\n{result.stderr}\n[Stdout Last 500 chars]:\n{result.stdout[-500:]}"
            return {
                "state": False,
                "Text": error_log
            }

    except subprocess.TimeoutExpired:
        print("⚠️ Fuzz 測試超時：遊戲可能卡死，視為失敗。")
        if os.path.exists(temp_full_path):
            os.remove(temp_full_path)
        return {
                "state": False, 
                "Text": "TimeoutError: The game loop froze or is too slow during fuzzing."
        }
    except Exception as e:
        if os.path.exists(temp_full_path):
            os.remove(temp_full_path) 
        return {
            "state": False,
            "Text": str(e)
        }