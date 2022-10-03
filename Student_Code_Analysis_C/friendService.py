
def analyzeFriend(file):
    locationOccuration = []
    currentLine = 0
    for x in file:
        if (" friend " in x or "friend " in x) and ('()' not in x) and (not x == ""): #maybe not include () because a friend doesnt have to be a function but a friend is a friend
            locationOccuration.append(currentLine)
        currentLine = currentLine + 1 #inc in order to see where the occurance of the friend occures
    return locationOccuration
