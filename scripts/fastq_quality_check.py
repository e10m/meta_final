import statistics

qual_bool = False
phred_scores = []

for line in open(file="C:\\Users\\Ethan Mach\\Downloads\\SRR17644439_1.fastq"):
    if line.startswith("+"):
        qual_bool = True
        continue
    if qual_bool is True:
        avg = [ord(char) - 33 for char in line]
        phred_scores.append(statistics.mean(avg))
        qual_bool = False

print(min(phred_scores))