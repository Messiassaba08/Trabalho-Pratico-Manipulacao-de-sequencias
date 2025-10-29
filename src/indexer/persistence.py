def load_inverted_index(file_path):
    inverted_index = {}
    with open(file_path, 'r') as file:
        for line in file:
            term, doc_ids = line.strip().split(':')
            inverted_index[term] = list(map(int, doc_ids.split(',')))
    return inverted_index

def save_inverted_index(inverted_index, file_path):
    with open(file_path, 'w') as file:
        for term, doc_ids in inverted_index.items():
            file.write(f"{term}:{','.join(map(str, doc_ids))}\n")