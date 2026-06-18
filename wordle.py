words = []
includes = []
nincludes = []
temp = []
debuging = False

def startup():
    global words
    words = []
    with open("./all-wordle-words.txt", "r") as file:
        for line in file:
            words.append(line.replace("\n", ""))

def in_includes(word):
    global includes

    for chs in includes:
        if(str(chs) not in word):
            return False
    return True

def in_mincludes(word):
    global nincludes

    for chs in nincludes:
        if(str(chs) in word):
            return True
    return False

def cleanup():
    global words
    global includes
    global nincludes
    
    for i in range(len(words)):
        if len(temp) == 2: # clean up for exact command
            if (type(temp[1]) == int and type(temp[0]) == str):
                if not words[i][temp[1]] == temp[0]: # if not exact char in include[1] equal include[0]
                    words[i] = ""
                    continue
                

        if len(temp) == 3: # clean up for not exact command
            if (type(temp[1]) == int and type(temp[0]) == str) and type(temp[2]) == str:
                if words[i][temp[1]] == temp[0]:
                    words[i] = ""
                    continue
            

        if not in_includes(words[i]):
            words[i] = ""
        
        if in_mincludes(words[i]):# clean up for not include command
            words[i] = ""

    words = [w for w in words if w != ""]

startup()

while True: 
    a = input()
    changed = False

    if (a.startswith("i")): # include
         a = a[1:]
         for ch in a:
            includes.append(ch)
         changed = True

    elif (a.startswith("n")): # not include
        a = a[1:]
        for ch in a:
            nincludes.append(ch)
        changed = True

    elif (a.startswith("e")): # exact
        a = a[1:] # format a: ea2 (exact a at 2)
        includes.append(a[0])
        temp.append(a[0]) # the char
        temp.append(int(a[1]) - 1) # the exact position
        changed = True

    elif (a.startswith("r")): # remove
        a = a[1:] # format a: ra2 (remove where a at 2)
        includes.append(a[0])
        temp.append(a[0]) # same as the exact command
        temp.append(int(a[1]) - 1)
        temp.append("")
        changed = True

    if (a.startswith("show")):
         print(words)
    
    if (a.startswith("clear")):
        includes = []
        nincludes = []
        startup()

    if changed:
        includes = list(set(includes))
        nincludes = list(set(nincludes))
        if debuging: print(includes, nincludes, temp)
        cleanup()
        temp = []
    

