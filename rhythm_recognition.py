

def check_rhythm(list1, list2, threshold):
    """
    Checks if 2 different rhythms match. Rhythms should be passed as a list of integers, where each integer
    represents the time in ms a button was held down or the gaps between presses.
    e.g [500, 1000, 500] would indicate the button was pressed for half a second, then the user waited for 1 second,
    then it was pressed for half a second again.

    :param list1: A rhythm represented in a python list
    :param list2: A different rhythm
    :param threshold: The maximum percent difference that can exist between two parts of a rhythm
    :return: True if the rhythms match, false otherwise
    """
    if len(list1) != len(list2):
        return False

    for i in range(len(list1)):
        print(abs((list1[i] - list2[i]) / list1[i]))
        if abs((list1[i] - list2[i]) / list1[i]) > threshold:
            return False

    return True


if __name__ == '__main__':
    #rhythms 1 and 2 should match, 3 and 4 should match
    rhythm1 = [372,225,110,369,423,522,94,274,70]
    rhythm2 = [387,258,111,322,414,530,78,274,62]

    rhythm3 = [83,249,87,241,103,233,87,234,78]
    rhythm4 = [73,225,71,225,95,229,91,209,103]

    print(check_rhythm(rhythm2, rhythm1, .5))