import nuke
import nkCheck

def nodeToBackdrop():
	sel = nuke.selectedNode()
	backdrops = [n for n in nuke.allNodes() if n.Class() == 'BackdropNode']

	for bd in backdrops:
		if nkCheck.nodeInBackdrop(sel, bd):
			return b
	return None
