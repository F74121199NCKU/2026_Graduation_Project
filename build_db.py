#建立database
import os
import chromadb
import google.generativeai as genai
from chromadb.utils import embedding_functions

# 1. 設定 Google API
# 為了安全，每次執行時輸入 Key，或者你可以寫死在這裡測試
api_key_user = input("Please enter your Google Gemini API Key: ").strip()
genai.configure(api_key=api_key_user)

# 設定我們要使用的 Embedding 模型 (這是專門把文字變數字的模型，不是對話模型)
EMBEDDING_MODEL = "models/text-embedding-004"

def build_knowledge_base():
    print("🚀 開始建立向量資料庫 (Knowledge Base)...")

    # 2. 初始化 ChromaDB
    #這會在你的資料夾產生一個 'chroma_db' 的目錄，裡面就是資料庫檔案
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # 建立或取得一個 Collection (類似 SQL 的 Table)
    # 我們叫它 "game_modules"
    collection = chroma_client.get_or_create_collection(name="game_modules")

    # 3. 讀取參考模組
    folder_path = "reference_modules"
    if not os.path.exists(folder_path):
        print(f"❌ 錯誤：找不到資料夾 {folder_path}")
        return

    # 準備批次資料
    documents = []  # 存程式碼內容
    ids = []        # 存檔名作為 ID
    metadatas = []  # 存額外資訊 (如 tags)

    print(f"📂 正在掃描 {folder_path}...")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            print(f"   -> 發現模組: {filename}")
            
            # 簡單解析一下開頭的 # tags: 
            # (這是一個小技巧，讓 AI 更好搜尋)
            tags = "general"
            first_line = content.split('\n')[0]
            if first_line.startswith("# tags:"):
                tags = first_line.replace("# tags:", "").strip()

            documents.append(content)
            ids.append(filename)
            metadatas.append({"source": filename, "tags": tags})

    if not documents:
        print("⚠️ 沒有找到任何 .py 檔案，請確認步驟是否正確。")
        return

    # 4. 生成向量 (Embeddings) 並存入資料庫
    print("🧠 正在呼叫 Gemini 生成向量 (這可能需要幾秒鐘)...")
    
    try:
        # 使用 Google GenAI 批次生成向量
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=documents,
            task_type="retrieval_document",
            title="Game Code Snippets"
        )
        
        embeddings = result['embedding']

        # 5. 寫入 ChromaDB
        print("💾 正在寫入 ChromaDB...")
        collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ 成功！已將 {len(documents)} 個模組存入資料庫。")
        print("   資料庫路徑: ./chroma_db")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    build_knowledge_base()