import re
import statistics

count = 0
len_list = []

for line in open(file="C:\\Users\\Ethan Mach\\Downloads\\SRR17644439_1.fastq"):
    if line.startswith("@"):
        read_len = re.search(r'length=(\d+)', line).group(1)
        len_list.append(int(read_len))

print(len_list)
print(min(len_list))
