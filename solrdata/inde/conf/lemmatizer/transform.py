lemmas = open('lemmas.dict', 'r')
lemmasResult = open('lemmas-pt.dict', 'w')

for line in lemmas:
  print(line)
  line = line.replace('\tA\t', '\tadj\t')
  line = line.replace('\tN\t', '\tn\t')
  line = line.replace('\tV\t', '\tv-fin\t')
  line = line.replace('\tPREP\t', '\tn\t')
  line = line.replace('\tPRO\t', '\tart\t')
  line = line.replace('\tDET+Art\t', '\tart\t')
  line = line.replace('\tDET+Num\t', '\tn\t')
  lemmasResult.write(line)

lemmasResult.close()
lemmas.close()