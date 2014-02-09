# This implementation is experimental, if it works oddly then turn off it.

import nuke

def changeEverySelectedKnobs():
	node = nuke.thisNode()
	if node not in nuke.Root().nodes():
		# there are many nodes that we can't see, cull them.
		return

	if node.Class() == 'BackdropNode':
		# I will not treat Backdrop as a Normal Node.
		return

	knob = nuke.thisKnob()
	kname, kval = knob.name(), knob.value()
	if kname in ['xpos', 'ypos', 'selected', 'name', 'hidePanel', 'showPanel', 'label', 'scene_view', 'note_font_size', 'inputChange', 'bdwidth', 'bdheight']:
		return

	print('command node : {0}'.format(node.name()))
	print('{0} : {1}'.format(kname, kval))

	for n in nuke.selectedNodes():
		n[kname].setValue(kval)
