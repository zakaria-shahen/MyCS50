import csv
import sys
import re


def main():
    
    # check input lenght
    if len(sys.argv) != 3:
        print('Usage: python dna.py data.csv sequence.txt')
        return
    
    # reading dan and loading RAM     
    dna = ''
    with open(sys.argv[2], "r") as file_dna:
        dna = file_dna.read().strip('\n')

    # reading databases and loading RAM
    data = []
    field_name = []
    with open(sys.argv[1], "r") as file_data:
        reader = csv.DictReader(file_data)
        field_name = reader.fieldnames[1:]
        for line in reader:
            for n in field_name:
                line[n] = int(line[n])   
            data.append(line)

    # calc STRs
    dna_STR = {}
    for name in field_name:
        dna_STR[name] = calc_STRs(dna, name)[0]

    # Find match
    for d in data:
        bool = []
        for name in field_name:
            bool.append(d[name] == dna_STR[name])
                
        if sum(bool) == len(field_name):
            print(d["name"])
            return

    # if no match
    print("No match")


def calc_STRs(dna, regEx):
    """ calc STRs  """
    # get Match
    match = re.search(regEx, dna)
    if match == None:
        return [0]
    
    # get Start match position
    position = match.start()

    # get length STRs
    count_STR = 0
    while dna[position:(position+len(regEx))] == regEx:
        count_STR += 1
        position += len(regEx)
    
    # add STR to STRs list
    list_STRs = [count_STR]
    
    # looping other dna
    list_STRs += calc_STRs(dna[position:], regEx)

    # if list length > 1 => return get Big Nuumber as list (length 1)
    if len(list_STRs) > 1:
        list_STRs.sort(reverse=True)
        # print(list_STRs)
        return [list_STRs[0]]
    
    # if list length 1 element 
    return list_STRs


if __name__ == "__main__":
    main()