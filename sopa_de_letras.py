
def check_line(line, result, checking, words):
    if not line: return result
    checking = line[0]
    for letter in line[1:]:
        checking += letter
        #print checking
        if checking in words: result.append(checking)
    return check_line(line[1:], result, None, words)

#w = ['word', 'caca']
#print check_line(['c', 'd', 'w', 'o', 'r', 'd', 'c', 'a', 'c', 'a'], [], None, w)

def transpose(sopa):
    sudokut = []
    for c in range(0, len(sopa[0])):
        column = []
        for fila in sudoku:
            column.append(fila[c])
        sudokut.append(column)
    return sopa

def diagonals(sopa):
