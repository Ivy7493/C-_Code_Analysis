
def analyzeFriend(file):
    friendCount = 0;
    locationOccuration = []
    currentLine = 0
    for x in file:
        if ("friend" in x) and ('()'in x) and (not x == ""): #maybe not include () because a friend doesnt have to be a function but a friend is a friend
            friendCount = friendCount + 1 #inc in the case where we find the friend keyword
            locationOccuration.append(currentLine)
        currentLine = currentLine + 1 #inc in order to see where the occurance of the friend occures
    return friendCount,locationOccuration
