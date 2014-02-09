import nuke
import find

def selectSimilarType():
	if nuke.selectedNodes():
		nuke.selectSimilar(nuke.MATCH_CLASS)
	else:
		nuke.selectAll()

def selectSimilarName():
	try:
		sel = nuke.selectedNode()
	except ValueError:
		return
	for n in nuke.allNodes():
		if sel.Class() == n.Class() and sel.name().rstrip('1234567890') == n.name().rstrip('1234567890'):
			n.setSelected(1)

def selectSimilarTypeInBackdrop():
	try:
		sel = nuke.selectedNode()
	except ValueError:
		return
	backdrop = find.myBackdrop()
	if backdrop:
		left = backdrop['xpos'].value()
		top = backdrop['ypos'].value()
		right = left + backdrop['bdwidth'].value()
		bottom = top + backdrop['bdheight'].value()
		nodes = []
		for n in nuke.allNodes():
			if sel.Class() == n.Class():
				if left < n.xpos() < right and top < n.ypos() < bottom:
					n.setSelected(1)
	else:
		for n in nuke.allNodes():
			if sel.Class() == n.Class():
				n.setSelected(1)

def selectSimilarTypeAndNameInBackdrop():
	try:
		sel = nuke.selectedNode()
	except ValueError:
		return
	backdrop = find.myBackdrop()
	if backdrop:
		left = backdrop['xpos'].value()
		top = backdrop['ypos'].value()
		right = left + backdrop['bdwidth'].value()
		bottom = top + backdrop['bdheight'].value()
		nodes = []
		for n in nuke.allNodes():
			if sel.Class() == n.Class() and sel.name().rstrip('1234567890') == n.name().rstrip('1234567890'):
				if left < n.xpos() < right and top < n.ypos() < bottom:
					n.setSelected(1)
	else:
		for n in nuke.allNodes():
			if sel.Class() == n.Class() and sel.name().rstrip('1234567890') == n.name().rstrip('1234567890'):
				n.setSelected(1)