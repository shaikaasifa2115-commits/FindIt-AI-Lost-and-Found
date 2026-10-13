from ai_matching import calculate_text_similarity


text1 = "Black JBL headphones lost near GITAM library"

text2 = "Black wireless JBL headphones found near the library"


score = calculate_text_similarity(text1, text2)


print(f"Similarity Score: {score}%")