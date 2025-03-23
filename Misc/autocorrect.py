def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # deletion
                          d[i][j - 1] + 1,      # insertion
                          d[i - 1][j - 1] + substitution_cost)  # substitution
    
    return d[m][n]

def autocorrect(input_word, dictionary_file):
    with open(dictionary_file, 'r') as file:
        dictionary = file.read().splitlines()
    
    distances = [(word, levenshtein_distance(input_word, word)) for word in dictionary]
    distances.sort(key=lambda x: x[1])
    return distances[0][0] if distances else input_word

# use

# dictionary_file = "/Users/pratyushsinha/Github/quant/Misc/list.txt"  
#input_word = "aapll"
# corrected_word = autocorrect(input_word, dictionary_file)
# print(f"Did you mean: {corrected_word}?")