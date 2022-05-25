def splitShortAndName(nameRecord):
    split = nameRecord.split(" ")
    if len(split) > 1:
        split[1] = split[1][1:-1]
    else:
        split.append("") 
    return split