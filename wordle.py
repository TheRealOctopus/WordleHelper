words = []
includes = []
nincludes = []

def startup():
    global words
    words = []
    with open("./all-wordle-words.txt", "r") as file:
        for line in file:
            words.append(line.replace("\n", ""))

def in_includes(word):
    global includes

    for chs in includes:
        if(chs not in word):
            return False
    return True

def in_mincludes(word):
    global nincludes

    for chs in nincludes:
        if(chs in word):
            return True
    return False

def cleanup():
    global words
    global includes
    global nincludes
    
    for i in range(len(words)):
        if len(includes) == 2: # clean up for exact command
            if (type(includes[1]) == int and type(includes[0]) == str):
                if not words[i][includes[1]] == includes[0]: # if not exact char in include[1] equal include[0]
                    words[i] = ""
                    continue
                continue

        if len(includes) == 3: # clean up for not exact command
            if (type(includes[1]) == int and type(includes[0]) == str) and type(includes[2]) == str:
                if words[i][includes[1]] == includes[0]:
                    words[i] = ""
                    continue
            continue

        if includes != []: # clean up for include command
            if in_includes(words[i]):
                continue
            else:
                words[i] = ""
                continue
        
        if nincludes != []: # clean up for not include command
            if in_mincludes(words[i]):
                words[i] = ""
                continue
            else:
                continue

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
        includes.append(a[0]) # the char
        includes.append(int(a[1]) - 1) # the exact position
        changed = True

    elif (a.startswith("r")): # remove
        a = a[1:] # format a: ra2 (remove where a at 2)
        includes.append(a[0]) # same as the exact command
        includes.append(int(a[1]) - 1)
        includes.append("")
        changed = True

    if (a.startswith("show")):
         print(words)
    
    if (a.startswith("clear")):
        startup()

    if changed:
        cleanup()
        includes = []
        nincludes = []
    

