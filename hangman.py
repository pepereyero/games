import random
# -*- coding: utf-8 -*-
words = "your art, my dearest father, you have Put the wild waters in this roar, allay them. The sky, it seems, would pour down stinking pitch, But that the sea, mounting to the welkin cheek, Dashes the fire out. O, I have sufferedWith those that I saw suffer: a brave vessel,Who had, no doubt, some noble creature in her, Dash'd all to pieces. O, the cry did knockAgainst my very heart. Poor souls, they perishd. Had I been any god of power, I wouldHave sunk the sea within the earth or ere It should the good ship so have swallow andThe fraughting souls within her."

def split_string(string, signo):
    palabra = ''
    lista_correcta = []
    for e in string:
        if e not in signo:
            palabra = palabra + e
        if e in signo:
            if palabra != '':
                lista_correcta.append(palabra)
            palabra = ''
    if palabra != '':
        lista_correcta.append(palabra)
    return lista_correcta

words = split_string(words, " ,.+:'")

def setting_lines(word):
    lines = ''
    idx = 0
    for e in word:
        lines = lines + '/'
        idx += 1
    return lines

def pos_in_lines(word, letter):
    all_idx = []
    idx = 0
    for e in word:
        if e == letter:
            all_idx.append(idx)
        idx += 1
    return all_idx

def reemplacing(lines, word, letter):
    all_indexes= pos_in_lines(word, letter)
    new = list(lines)
    for idx in all_indexes:
        new[idx] = letter
    return ''.join(new)

def setting_random_letter(lines, word):
    idx = random.choice(range(len(word)))
    new = list(lines)
    new[idx] = word[idx]
    return ''.join(new)

def growing_boddy(boddy_parts, counter):
    g_boddy = []
    for e in range(counter):
        g_boddy.append(boddy_parts[e])
    return g_boddy

#print growing_boddy(['cabeza', 'brazos', 'cuerpo', 'piernas'], )

def playing(word, lines, grow_boddy, counter):
    boddy_parts = ['head', 'boddy', 'one arm', 'the other arm', 'one leg', 'the other leg']
    if lines == word:
        return 'Well done! You saved the man!'

    letter = raw_input('Choose a letter: ')
    if letter in word:
        lines = reemplacing(lines, word, letter)
        print lines
        print
        return playing(word, lines, grow_boddy, counter)

    if letter not in word:
        grow_boddy = growing_boddy(boddy_parts, counter)
        if grow_boddy == boddy_parts:
            print
            print 'The word was ' + word
            return  '😑 💥 🔫 '
        else:
            print grow_boddy
            print
            return playing(word, lines, grow_boddy, counter+1)

#print playing_1('word', '////', [], 1)

def lets_play(word):
    lines = setting_lines(word)
    lines = setting_random_letter(lines, word)
    grow_boddy = []
    counter = 1
    print lines
    print
    return playing(word, lines, grow_boddy, counter)

print lets_play('word')
