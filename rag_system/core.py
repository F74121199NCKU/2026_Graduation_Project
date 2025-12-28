import os
import google.generativeai as genai
import chromadb
# 這裡需要引用上一層的 config，因為我們需要知道用哪個模型
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EMBEDDING_MODEL

# === 這裡放入原來的 RAG 相關函式 ===

def select_relevant_modules(user_query: str) -> str:
    """
    第一階段：讓 LLM 根據需求，從現有檔案列表中挑選出可能需要的模組。
    這能大幅增加 RAG 的準確度 (Query Expansion)。
    """
    folder_path = "reference_modules"
    if not os.path.exists(folder_path):
        return ""

    # 1. 獲取所有現有的模組檔名
    available_files = [f for f in os.listdir(folder_path) if f.endswith(".py")]
    files_str = ", ".join(available_files)
    
    print(f"🤔 正在分析需求，思考需要哪些模組 (候選名單: {len(available_files)} 個)...")

    # 2. 詢問 LLM (使用快速模型即可)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    prompt = (
        "你是一個 Python 遊戲開發的技術選型專家。"
        f"目前我們的儲存庫中有以下模組檔案：[{files_str}]。"
        f"使用者的需求是：'{user_query}'。"
        
        "【任務】"
        "請判斷為了完成這個需求，我們**必須**或**強烈建議**使用哪些模組？"
        "請只列出檔名，用逗號分隔。"
        "如果不確定或都不需要，請回答 'NONE'。"
        
        "【範例輸出】"
        "camera_scroll.py, object_pool.py"
    )

    try:
        response = model.generate_content(prompt)
        selected = response.text.strip()
        
        if "NONE" in selected:
            print("   -> 分析結果：無需特定模組。")
            return ""
        else:
            print(f"   -> 💡 專家建議使用: {selected}")
            return selected
            
    except Exception as e:
        print(f"❌ 選型分析失敗: {e}")
        return ""

# --- RAG 核心功能 (加強版) ---
def get_rag_context(user_query: str) -> str:
    # 1. 先執行模組挑選 (Query Expansion)
    suggested_modules = select_relevant_modules(user_query)
    
    # 2. 組合新的搜尋語句
    enhanced_query = user_query
    if suggested_modules:
        enhanced_query = f"{user_query}. Strictly use these modules: {suggested_modules}"
    
    print(f"🔍 RAG 系統啟動：正在搜尋資料庫...")
    
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        collection = chroma_client.get_collection(name="game_modules")
        
        # 3. 生成向量
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=enhanced_query,
            task_type="retrieval_query"
        )
        query_embedding = result['embedding']
        
        # 4. 搜尋
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5, 
            include=['documents', 'distances'] 
        )
        
        DISTANCE_THRESHOLD = 1.0
        found_contents = []
        
        if results['documents']:
            num_results = len(results['documents'][0])
            for i in range(num_results):
                doc_content = results['documents'][0][i]
                doc_id = results['ids'][0][i]
                distance = results['distances'][0][i]
                
                final_threshold = DISTANCE_THRESHOLD
                if suggested_modules and doc_id in suggested_modules:
                    final_threshold = 1.5 # 放寬門檻
                    print(f"   -> 必選檔案發現: {doc_id} (門檻放寬至 1.5)")

                print(f"   -> 候選檔案: {doc_id:<20} | 距離: {distance:.4f}", end="")
                
                if distance < final_threshold:
                    print(" ✅ 採用")
                    formatted_doc = (
                        f"\n\n# ====== Reference Module: {doc_id} ======\n"
                        f"{doc_content}\n"
                        f"# ============================================\n"
                    )
                    found_contents.append(formatted_doc)
                else:
                    print(" ❌ 捨棄")

        if found_contents:
            return "".join(found_contents)
        else:
            return ""
            
    except Exception as e:
        print(f"❌ RAG 檢索失敗: {e}")
        return ""