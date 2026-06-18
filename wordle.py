words = []
includes = []
nincludes = []

def startup():
    global words
    with open("./words.txt", "r") as file:
        for line in file:
            words.append(line.replace("\n", ""))

def cleanup():
    global words
    global includes
    global nincludes
    
    for i in range(len(words)):
        if len(includes) == 2: # clean up for exact command
            if not words[i][includes[1]] == includes[0]: # if not exact char in include[1] equal include[0]
                words[i] = ""
                continue
            continue

        if len(includes) == 3: # clean up for not exact command
            if words[i][includes[1]] == includes[0]:
                words[i] = ""
                continue
            continue

        
        for c in range(len(words[i])): 
            if nincludes != []: # clean up for not include command
                if words[i][c] in nincludes:
                    words[i] = ""
                    break
            if includes != []: # clean up for include command
                if words[i][c] in includes:
                    break
                
                if ((words[i][c] not in includes) and (c == len(words[i]) - 1)):
                    words[i] = ""
                    break
    words = [w for w in words if w != ""]

startup()

while True: 
    a = input()
    changed = False

    if (a.startswith("i")): # include
         a = a[1:]
         includes.append(a)
         changed = True

    elif (a.startswith("n")): # not include
        a = a[1:]
        nincludes.append(a)
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
        ninclude = []
    

