inp = "아이 씨발 행복하네 존나"
# => "아이 ** 행복하네 **"

lst = ["시발", "씨발", "존나", "개새끼", "병신", "장애", "개씨발", "개병신"]

new_inp = []
inp = inp.split()
for i in inp:
  if i in lst:
    i = "*" * len(i)
  new_inp.append(i)

print(' '.join(new_inp))