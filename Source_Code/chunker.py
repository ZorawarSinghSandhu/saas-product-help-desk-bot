from pathlib import Path

folder_path = Path("../Raw_text")

def chunk_documents(folder_path):
    chunk_size = 500
    overlap = 100
    step_size = chunk_size - overlap
    total_chunks = 0
    chunks_list = []
    # sentences = []
    
    for file in folder_path.glob("*.txt"):
        with open(file, mode='r', encoding='utf-8') as f:
            content = f.read().strip()
        start = 0
        chunk_index = 0
        
        while start < len(content):
            end = start + chunk_size
            sliced_content = content[start:end]
            chunks_list.append({"raw_chunk": sliced_content, "chunk_index": chunk_index, "file_name": file.name})
            # sentences.append(sliced_content)
            total_chunks += 1
            start += step_size
            chunk_index += 1
    return chunks_list
    # print(total_chunks)
    # for chunk_obj in chunks_list:
    #     for key, value in chunk_obj.items():
    #         print(f"{key}: {value}")
    #     print("\n")


# chunk_documents(folder_path)