
# https://www.python-course.eu/levenshtein_distance.php
# 莱温斯坦距离

cities = {"Pittsburgh": "Pennsylvania",
          "Tucson": "Arizona",
          "Cincinnati": "Ohio",
          "Albuquerque": "New Mexico",
          "Culpeper": "Virginia",
          "Asheville": "North Carolina",
          "Worcester": "Massachusetts",
          "Manhattan": "New York",
          "Phoenix": "Arizona",
          "Niagara Falls": "New York"}


def LD(s, t):
    if s == '':
        return len(t)
    if t == '':
        return len(s)

    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1

    res = min([LD(s[:-1], t) + 1,
               LD(s, t[:-1]) + 1,
               LD(s[:-1], t[:-1]) + cost])
    return res


print(LD('Python', 'Peithen'))
