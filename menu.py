nuke.pluginAddPath('python')

import nkUtil
import nkReadWrite
import nkCallback
import nkSelect
import nkAlign

# Callbacks
nuke.addKnobChanged(nkCallback.changeEverySelectedKnobs)

# Commands
nodes = nuke.menu('Nodes')
nodes.addCommand('Other/defaultWrite', 'nkReadWrite.defaultWrite()', 'w')
nodes.addCommand('Other/tempWrite', 'nkReadWrite.tempWrite()', 'alt+w')
nodes.addCommand('Other/myRead', 'nkReadWrite.myRead()', 'r')
nodes.addCommand('Other/selectSimilarType', 'nkSelect.selectSimilarType()', 'a')
nodes.addCommand('Other/selectSimilarName', 'nkSelect.selectSimilarName()', 'shift+a')
nodes.addCommand('Other/selectSimilarTypeInBackdrop', 'nkSelect.selectSimilarTypeInBackdrop()', 'alt+a')
nodes.addCommand('Other/selectSimilarTypeAndNameInBackdrop', 'nkSelect.selectSimilarTypeAndNameInBackdrop()', 'alt+shift+a')
nodes.addCommand('Other/flipXY', 'nkAlign.flipXY()', 'alt+f')
