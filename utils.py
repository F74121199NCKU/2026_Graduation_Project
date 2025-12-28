import os
import re

# 工具箱

#儲存為 .py 檔案
def code_to_py(code, filename = "generated_app.py", folder = "dest"):
    os.makedirs(folder, exist_ok = True)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"📁 檔案已儲存至: {file_path}")
    return file_path 

#刪除LLM提供的垃圾訊息
def clean_code(raw_text: str) -> str:                       
    clean_text = re.sub(r'^```python\s*', '', raw_text)   
    clean_text = re.sub(r'^```\s*', '', clean_text)       
    clean_text = re.sub(r'```$', '', clean_text)          
    return clean_text.strip()