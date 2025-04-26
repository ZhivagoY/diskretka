horizontal = 18
vertical = 16

# Инициализация 3D-массива: dp[i][j][k]
dp = [[[0] * 2 for _ in range(vertical + 1)] for _ in range(horizontal + 1)]
dp[0][0][0] = 1  # База: начало пути

for i in range(horizontal + 1):
    for j in range(vertical + 1):
        if i == 0 and j == 0:
            continue
        
        # Обработка горизонтальных шагов
        if i > 0:
            dp[i][j][0] = dp[i-1][j][0] + dp[i-1][j][1]
        
        # Обработка вертикальных шагов
        if j > 0:
            dp[i][j][1] = dp[i][j-1][0]

total = dp[horizontal][vertical][0] + dp[horizontal][vertical][1]
print(f"Количество путей с ограничением: {total}")
