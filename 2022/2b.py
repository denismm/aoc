#!/usr/bin/env python3
import sys

choice_value:dict[str,int] = { 
    'A':1, 'B':2, 'C': 3,
}
result_for_code:dict[str,int] = {
    'X':0, 'Y':1, 'Z': 2,
}

def move_score(move:str) -> int:
    elf, result_code = move.split(' ')
    elf_value = choice_value[elf]
    result = result_for_code[result_code]
    score = 3 * result
    me_value = (elf_value + result + 1) % 3 + 1
    score += me_value
    return score

filename = sys.argv[1]
with open(filename, 'r') as f:
    total_score:int = 0
    for line in f:
        total_score += move_score(line.rstrip())
    print( total_score )
