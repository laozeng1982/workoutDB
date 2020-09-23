import pandas as pd

df = pd.DataFrame(data={'books': ['bk1', 'bk2', 'bk1', 'bk2', 'bk1', 'bk3'], 'price': [12, 12, 12, 15, 15, 17],
                        'num': [2, 1, 1, 4, 2, 2]})
print(df)

print(len(df.groupby('books')))

for idx, x in enumerate(df.groupby('books', as_index=True)):
    print(idx, "x[0]", x[0], len(x[1]), type(x[1]))
    print(x[1])
