from collections import Counter

def count_permutations(word, k):
    letter_counts = Counter(word)
    
    def backtrack(counts, remaining):
        if remaining == 0:
            return 1
        total = 0
        for char in counts:
            if counts[char] > 0:
                counts[char] -= 1
                total += backtrack(counts, remaining - 1)
                counts[char] += 1
        return total
    
    return backtrack(letter_counts, k)

word = "АБРАКАДАБРА"
k = 6
result = count_permutations(word, k)
print(f"Количество различных слов: {result}")  # Вывод: 3864
