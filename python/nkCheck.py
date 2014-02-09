import nuke

def selectedNodesAreSameClass():
	checkClass = nuke.selectedNode().Class()
	for n in nuke.selectedNodes():
		if n.Class() != checkClass:
			return False
	return True

def nodeInBackdrop(node, backdrop):
	bdleft = backdrop.xpos()
	bdtop = backdrop.ypos()
	bdright = bdleft + backdrop['bdwidth'].value()
	bdbottom = bdtop + backdrop['bdheight'].value()

	h_ok = bdleft < sel.xpos() < bdright
	w_ok = bdtop < sel.ypos() < bdbottom
	return h_ok and w_ok
