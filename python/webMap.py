content = open("output.txt").readlines()

lookup = 'deez'

lines = [line_num for line_num, line_content in enumerate(content) if lookup in line_content]

print(lines)