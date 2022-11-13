
def analyzeFriend(file):
    locationOccuration = []
    currentLine = 0
    scope = 0;
    for x in file:
        #  print("We working with line: ", x)
        if (" friend " in x or "friend " in x) and (x.find("friend") == 0) and (not x == "") and len(x) >= 4 and " " and len(x.split(" ")) >= 2:
            locationOccuration.append(currentLine)
        currentLine = currentLine + 1 #inc in order to see where the occurance of the friend occures

    return locationOccuration
