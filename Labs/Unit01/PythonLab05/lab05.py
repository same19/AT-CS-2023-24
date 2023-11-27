def print_sum(in_path):
    with open(in_path, 'r') as f:
        sum = 0
        s = ''
        while True:
            s = f.readline()
            if not s:
                break
            try:
                sum += int(s)
            except ValueError:
                print(s.strip(), "is not a number.")
    print("Sum is",sum)

print_sum("data/numbers.txt")


def calculate_costs(purchase_path, cost_path, out_path):
    purchase = open(purchase_path, 'r')
    cost = open(cost_path, 'r')
    out = open(out_path, 'w')

    cost_dict = {}
    for item in cost.readlines():
        item_split = item.split(' ')
        cost_dict[item_split[0]] = float(item_split[1].strip())

    for person in purchase.readlines():
        sum = 0
        person_split = person.split(' ')
        for item in person_split[1:]:
            sum += cost_dict[item.strip()]
        out.write(person_split[0] + " " + str(sum) + "\n")
    purchase.close()
    cost.close()
    out.close()
calculate_costs('data/raw_purchases.txt', 'data/costs.txt', 'data/total_spent.txt')

def rna_to_aa(rna_path, aa_path, out_path):
    rna = open(rna_path, 'r')
    aa = open(aa_path, 'r')
    out = open(out_path, 'w')
    aa_dict = {}
    for line in aa.readlines():
        line_split = line.strip().split(' ')
        for amino_acid in line_split[1:]:
            aa_dict[amino_acid] = line_split[0]
    rna_str = rna.readline().strip()
    start = rna_str.index('AUG')
    stop = rna_str.index('UAG')
    rna_str = rna_str[start:stop]
    rna_split = [rna_str[i] + rna_str[i+1] + rna_str[i+2] for i in range(len(rna_str)-2) if i % 3 == 0]
    out_list = []
    for rna_piece in rna_split:
        out_list.append(aa_dict[rna_piece])
    for out_item in out_list:
        out.write(out_item)
    rna.close()
    aa.close()
    out.close()

rna_to_aa('data/rna.txt', 'data/codons.txt', 'data/amino_acids.txt')
