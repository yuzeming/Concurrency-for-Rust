
import sys
import re

from sets import Set

def printCommit(commit, setFile):
	#for line in commit:
	#	print line[:-1]

	reCommit = re.compile(r'commit ([0-9a-f]{40})')
	reDiff = re.compile(r'diff --git a/([^\s]+) ')
	match = reCommit.match(commit[0])

	print match.group(1),

	for f in setFile:
		print f,

	print
	

def containAny(sLine, wordList):
	for w in wordList:
		if sLine.find(w) >= 0:
			return True

	return False


if __name__ == "__main__":
	sFileName = sys.argv[1]
	sLang = sys.argv[2]

	lockList = ['lock()']

	if sLang == 'go':
		chanList = ['<-', '->']
	elif sLang == 'rust':
		chanList = ['send(', 'recv()']
	else:
		exit(0)


	commitList = []
	lineList = []

	#reCommit = r'commit [0-9a-f]{40}'

	numCommit = 0
	with open(sFileName, 'r') as f:
		while True:
			line = f.readline()
			if not line:
				break

			if line.startswith('commit'):
				numCommit += 1
				if len(lineList) != 0:
					commitList.append(lineList)
				lineList = []

			lineList.append(line)

		commitList.append(lineList)

	reDiff = re.compile(r'diff --git a/([^\s]+) ')


	for commit in commitList:
		setLockAdd = Set([])
		setLockRemove = Set([])
		setChanAdd = Set([])
		setChanRemove = Set([])

		setFiles = Set([])

		for line in commit:
			if line.startswith('diff'):
				if len(setLockAdd) > 0 and len(setChanRemove) > 0 or len(setLockRemove) > 0 and len(setChanAdd) > 0:
					match = reDiff.match(diffLine)
					sFileName = match.group(1)
					setFiles.add(sFileName)
			
				setLockAdd.clear()
				setLockRemove.clear()
				setChanAdd.clear()
				setChanRemove.clear()
				diffLine = line

			elif line.startswith('+') and containAny(line, lockList):
				setLockAdd.add(line)
			elif line.startswith('-') and containAny(line, lockList):
				setLockRemove.add(line)
			elif line.startswith('+') and containAny(line, chanList):
				setChanAdd.add(line)
			elif line.startswith('-') and containAny(line, chanList):
				setChanRemove.add(line)



		if len(setFiles) > 0:
			printCommit(commit, setFiles)