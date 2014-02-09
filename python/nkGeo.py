import nuke

def centerpivot():
    sel = nuke.selectedNode()

    if sel.Class()!='ReadGeo2':
        return
    selknob = sel['geo_select']
    geo = selknob.getGeometry()
    ngeo = len(selknob.getGeometry())
    geocenter = nuke.math.Vector3(0,0,0)
    for g in geo:
        transform = g.transform()
        worldpos_sum = nuke.math.Vector3(0,0,0)
        npt = len(g.points())
        for pos in g.points():
            worldpos = transform*nuke.math.Vector4(pos.x, pos.y, pos.z, 1)
            worldpos = nuke.math.Vector3(worldpos.x, worldpos.y, worldpos.z)
            worldpos_sum += worldpos
        geocenter += worldpos_sum/npt
    sel['pivot'].setValue(geocenter/ngeo)
