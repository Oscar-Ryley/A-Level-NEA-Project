from webbrowser import open_new

def open_file(filename: str):
    """Function: open_file
    @params
    filename: name of text file

    Returns a list of the lines from a file.
    """
    lines = []
    file = open(filename, "r")
    iread = file.readlines()
    for line in iread:
        lines.append(line.strip())
    file.close()
    return lines

def open_web(link: str):
    """Function: open_web
    @params
    link: url to the website to be opened in a new chrome tab

    Opens a new chrome tab of the webpage given by the link input
    (open_new is from the web browser import)
    """
    open_new(str(link))

def half_list(hlist: list):
    """Function: half_list
    @params
    hlist: list input to be halved

    Returns the first and second halves of the list as two list variables.
    """
    length = len(hlist)
    if length <= 1:
        return hlist
    elif length == 2:
        return [hlist[0]], [hlist[1]]
    middle_index = int( (length/2) )
    first = hlist[:middle_index]
    second = hlist[middle_index:]
    return first, second

def mergesort(mlist: list):
    """Function: mergesort
    @params
    mlist: list input to be sorted

    Returns a sorted list that has been produced via a merge sort algorithm.
    The mergesort splits the list down into sublists and then joins these sublists whilst sorting until it has sorted the full list.
    """
    if len(mlist) <= 1:
        return mlist
    first, second = half_list(mlist)

    # iteration of the mergesort function back into the first and second halves of the list
    first = mergesort(first)
    second = mergesort(second)
    
    f = 0
    s = 0
    m = 0
    # sorts items from the first and second halves and places them back into the main list
    while f < len(first) and s < len(second):
        if first[f] <= second[s]:
            mlist[m] = second[s]
            s += 1
        else:
            mlist[m] = first[f]
            f += 1
        m += 1

    # clears up the last items
    while f < len(first):
        mlist[m] = first[f]
        f += 1
        m += 1
    while s < len(second):
        mlist[m] = second[s]
        s += 1
        m += 1
        
    return mlist