from sympy import symbols, Eq, solve

p = 0.59
V0, V1, V2 = symbols('V0 V1 V2')

eq1 = Eq(V2, -1 + (1 - p) * V1)
eq2 = Eq(V1, -1 + p * V0 + (1 - p) * V2)
eq3 = Eq(V0, -1/p + V1)

solution = solve([eq1, eq2, eq3], (V0, V1, V2))
solution[V0]
