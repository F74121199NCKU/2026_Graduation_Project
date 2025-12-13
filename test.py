import google.generativeai as genai     #type: ignore
import os

# ⚠️ 請務必填入你的 API Key
os.environ["GEMINI_API_KEY"] = "AIzaSyAGhtZSuWUz5LfED3UPkPyjV85WtY2i-MA"
genai.configure(api_key = os.environ.get("GEMINI_API_KEY"))

print("🔍 正在連接 Google 伺服器查詢可用模型列表...\n")

try:
    # 列出所有模型
    found_any = False
    for m in genai.list_models():
        # 我們只關心支援 "generateContent" (文字/程式碼生成) 的模型
        if 'generateContent' in m.supported_generation_methods:
            found_any = True
            print(f"📌 Model ID (請複製這個): {m.name}")
            print(f"   顯示名稱: {m.display_name}")
            print(f"   描述: {m.description[:150]}...") # 只顯示前50個字
            print("-" * 30)
    
    if not found_any:
        print("⚠️ 沒有找到支援 generateContent 的模型，請檢查 API Key 是否正確或專案權限。")

except Exception as e:
    print(f"❌ 查詢發生錯誤: {e}")