f = open('lemmas.dict', 'r')
lemma2 = open('lemmas2.dict', 'w')
i = 0
values = {
  'PRO': 0,
  'PREP': 0,
  'DET+Art': 0,
  'DET+Num': 0,
  'A': 0,
  'V': 0,
  'N': 0,
}
total_lines = 1
for line in f:
  total_lines += 1
  splited = line.split('\t')
  value = splited[1]
  if values[value] < 3:
    values[value] = values[value] + 1
    lemma2.write(line)
  i+=1
  if (i == 50000):
    print("_______________________")
    print(values)
    print("_______________________")
    i = 0
print(total_lines)
f.close()