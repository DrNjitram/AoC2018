import re
from datetime import datetime

dt = datetime.now()

instructions = []
pattern = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')

with open("G:\\24daysofcode\\input7.txt", 'r') as f:
	for line in f:
		instructions.append(pattern.match(line.strip()).groups())

instructions = sorted(instructions)

completedInstructions = []
allInstructions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
currentInstructions = [I for I in allInstructions if I not in [F for (S, F) in instructions]]


# Step S must be finished before step F can begin
def get_instruction (instr):
	return [F for (S, F) in instructions if S == instr]


def prerequirement (instr):
	return [I for I in allInstructions if I in [F for (F, S) in instructions if S == instr] if I not in completedInstructions]


# for instruction in allInstructions:
#	print(instruction, prerequirement(instruction), get_instruction(instruction))

while len(currentInstructions) > 0:
	currentInstructions.sort()
	currentInstruction = currentInstructions.pop(0)
	completedInstructions.append(currentInstruction)
	for nextInstruction in get_instruction(currentInstruction):
		if len(prerequirement(nextInstruction)) == 0:
			currentInstructions.append(nextInstruction)
			continue
instructionString = ''
for instruction in completedInstructions:
	instructionString += instruction
print(instructionString)
print(datetime.now() - dt)
