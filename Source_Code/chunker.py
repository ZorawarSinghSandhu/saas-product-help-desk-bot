from pathlib import Path

folder_path = Path("../Raw_text")

def chunk_documents(folder_path):
    chunk_size = 500
    overlap = 100
    step_size = chunk_size - overlap
    total_chunks = 0
    chunks_list = []
    
    
    for file in folder_path.glob("*.txt"):
        content = ""
        heading = ""
        with open(file, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            
        url = lines[0].strip()
        heading = lines[3].strip()
        content = " ".join(lines[4:]).strip()
        
        start = 0
        chunk_index = 0
        
        while start < len(content):
            end = start + chunk_size
            sliced_content = content[start:end]
            chunks_list.append({"raw_chunk": sliced_content, "chunk_index": chunk_index, "file_name": file.name, "file_url": url, "file_heading": heading})
            total_chunks += 1
            start += step_size
            chunk_index += 1
    
    return chunks_list

chunk_documents(folder_path=folder_path)