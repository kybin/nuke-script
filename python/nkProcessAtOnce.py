import nuke
import nukescripts
import nkCheck

# merge
def alternativeMerge():
	m = nuke.createNode('Merge')
	nukescripts.swapAB(m)

def invertDefaultMergeStyle():
	val = nuke.toNode('preferences')['goofy_foot'].getValue()
	invert = 1-val
	nuke.toNode('preferences')['goofy_foot'].setValue(invert)
	info = {0:'B under A', 1:'A over B'}
	print('merge style changed to {0}'.format(info[invert]))

def allMerge():
	sels = nuke.selectedNodes()
	sels = sorted(sels, key=lambda s: s.xpos())
	n = nuke.getInput('number of items in a group', '0')
	try:
		n = int(n)
	except:
		print('wrong input')
		raise
	if n == 0 or n > len(sels):
		n = len(sels)
	if n == 1:
		for s in sels:
			merge = nuke.createNode('Merge')
			merge.setInput(0, s)
			merge.setInput(1, None)
		return
	selGroup=zip(*[sels[i::n] for i in range(n)])
	for group in selGroup:
		A = None
		for B in group:
			if not A:
				A = B
			else:
				merge = nuke.createNode('Merge')
				merge.setInput(0, A)
				merge.setInput(1, B)
				A = merge

def destroyAndMerge():
	if check.selectedNodesAreSameClass():
		myclass = nuke.selectedNode().Class()
		merge = nuke.createNode(myclass)
		sels = nuke.selectedNodes()
		for s in sels:
			for d in s.dependent():
				for i in range(d.maxInputs()):
					if d.input(i) == myclass:
						d.setInput(i, merge)


# premult
def allPremult():
	sels = nuke.selectedNodes()
	for s in sels:
		postnodes = s.dependent()
		idxs = []
		for p in postnodes:
			idxs.append(p.dependecies().index(s))
		premul = nuke.createNode('Premult')
		premul.setInput(0, s)
		for p, i in zip(postnodes, idxs):
			p.setInput(i, s)
	return
