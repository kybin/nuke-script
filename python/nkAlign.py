import nuke

def horizontalAlign():
	base = nuke.selectedNode()
	basey = base.ypos()
	sels = nuke.selectedNodes()
	for s in sels:
		s.setYpos(basey)

def flipXY():
	sels = nuke.selectedNodes()
	for s in sels:
		x, y = s.xpos(), s.ypos()
		s.setXpos(y)
		s.setYpos(x)
