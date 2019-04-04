import logging

with open('tmpa', 'r') as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]
    print(lines)