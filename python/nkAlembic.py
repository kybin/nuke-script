import nuke

def alembicMerge():
    mainNode = nuke.selectedNode()
    mainScene = mainNode['scene_view']
    mainItems = mainScene.getSelectedItems()
    items = []
    selNodes = nuke.selectedNodes()
    for node in selNodes:
        item = node['scene_view'].getSelectedItems()
        print(item)
        items.extend(item)
    mainScene.setSelectedItems(items)
    delNodes = [n for n in selNodes if n is not mainNode]
    print(selNodes, delNodes)
    for d in delNodes:
        nuke.delete(d)


s = nuke.selectedNode()
items = s['scene_view'].getSelectedItems()
nuke.nodeCopy('%clipboard%')
for i in items:
    p=nuke.nodePaste('%clipboard%')
    p['scene_view'].setSelectedItems([i])
