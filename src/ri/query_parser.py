def parse_query(query):

    tokens = []
    current_token = ""
    in_parentheses = 0

    for char in query:
        if char in " ()":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if char == "(":
                in_parentheses += 1
                tokens.append(char)
            elif char == ")":
                in_parentheses -= 1
                tokens.append(char)
            elif char == " ":
                continue
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    # Convert tokens into a structured format
    structured_query = []
    for token in tokens:
        if token.upper() in ["AND", "OR"]:
            structured_query.append(token.upper())
        else:
            structured_query.append(token)

    return structured_query