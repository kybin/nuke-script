#####
#
#   Uses meta-data from the incoming image stream to break a PSD files into layers
#
#   Each layer is combined together with a PSDMerge node which emulates the blending modes
#
#####
import nuke
import random
import math
import threading
import os
import posixpath as path

class Layer():
	def __init__(self):
		self.attrs = {}

def getLayers(metadata):
	layers = []
	for key in metadata:
		if key.startswith('input/psd/layers/'):
			splitKey = key.split('/')
			num = int(splitKey[3])
			attr = splitKey[4]
			try:
				attr += '/' + splitKey[5]
			except:
				pass

			while (len(layers) <= num):
				layers.append(Layer())
			layers[num].attrs[attr] = metadata[key]
	return layers


def _newPsdMerge(layer, operation_overwrite=None):
	blendMap = {
		'norm': "normal",
		'scrn': "screen",
		'div ': "color dodge",
		'over': "overlay",
		'mul ': "multiply",
		'dark': "darken",
		'idiv': "color burn",
		'lbrn': "linear burn",
		'lite': "lighten",
		'lddg': "linear dodge",
		'lgCl': "lighter color",
		'sLit': "soft light",
		'hLit': "hard light",
		'lLit': "linear light",
		'vLit': "vivid light",
		'pLit': "pin light",
		'hMix': "hard mix",
		'diff': "difference",
		'smud': "exclusion",
		'fsub': "subtract",
		'fdiv': "divide",
		'hue ': "hue",
		'sat ': "saturation",
		'colr': "color",
		'lum ': "luminosity",
	}
	psdMerge = nuke.nodes.PSDMerge()
	if operation_overwrite:
		operation = operation_overwrite
	else:
		try:
			operation = blendMap[layer.attrs['blendmode']]
		except:
			print "unknown blending mode" + layer.attrs['blendmode']
			operation = "normal"
	psdMerge['operation'].setValue(operation)
	psdMerge['sRGB'].setValue(True)
	psdMerge['mix'].setValue( (layer.attrs['opacity'] / 255.0))
	try:
		if ( layer.attrs['mask/disable'] != True ):
			psdMerge['maskChannelInput'].setValue( name + '.mask' )
			if ( layer.attrs['mask/invert'] == True ) :
				psdMerge['invert_mask'].setValue( True )
	except:
		pass
	return psdMerge

def _parseLayers(node, items, exceptlayer=[], renderlayer='', extractposition=None, xspacing=80, yspacing=70, use_targa=False, geodir='c:/tmp'):
	metaData = node.metadata()
	layers = getLayers(metaData)

	dotXfudge = 34
	dotYfudge = 4
	backdropXfudge = -50
	backdropYfudge = -40
	yspacing = 70
	if extractposition:
		x, y = extractposition
	else:
		x, y = node.xpos(), node.ypos+yspacing*4
	left = x
	top = y
	bottom = y
	xstep = (xspacing*2 + backdropXfudge*2 + 50)
	bdleft = None
	bdtop = None
	groupstarted = False
	inputNode = node
	lastGroupLayer = None
	lastRenderLayer = None
	lastToneLayer = None
	backdrop = None
	for i, l in enumerate(layers):
		name = l.attrs['nukeName']
		print(i, l.attrs['nukeName']),
		try:
			print(l.attrs['divider/type'])
		except:
			print
		x += xstep
		y = top

		# only group type of layers have divider/type key
		grouplayer = False
		try:
			l.attrs['divider/type']
			grouplayer = True
		except KeyError:
			pass

		if grouplayer:
			if l.attrs['divider/type'] == 3: # GROUP START
				if groupstarted: # delete unclosed(incomplete) group 
					nuke.delete(backdrop)
				groupstarted = True
				backdrop = nuke.nodes.BackdropNode(tile_color = 2829621248, note_font_size=55)
				bdleft = x + xspacing
				bdtop = y
				backdrop.setXYpos(bdleft+backdropXfudge, bdtop+backdropYfudge)
				# reset some settings whenever group start
				inputNode = node
				lastGroupLayer = None
			elif l.attrs['divider/type'] in [1,2]: # GROUP END
				if not groupstarted:
					continue # unknown layer
				groupstarted = False
				backdrop['bdwidth'].setValue(x-bdleft-backdropXfudge)
				backdrop['bdheight'].setValue(bottom-top-backdropYfudge)
				backdrop['label'].setValue(name)
			continue 

		if items=='*':
			pass
		else:
			item_match = [i for i in items if name.lower().endswith(i)]
			if not item_match:
				continue
		except_match = [e for e in exceptlayer if name.lower().endswith(e)]
		if except_match:
			continue

		y += yspacing/2

		shuffle = nuke.nodes.Shuffle()
		shuffle.setName(name)
		shuffle['postage_stamp'].setValue(1)
		shuffle['in'].setValue(name)
		shuffle['in2'].setValue('none')
		shuffle['red'].setValue('red')
		shuffle['green'].setValue('green')
		shuffle['blue'].setValue('blue')
		shuffle['alpha'].setValue('alpha')

		# if no 'alpha' assume alpha of 1
		alphaChan = name + ".alpha"
		if not alphaChan in inputNode.channels():
			shuffle['alpha'].setValue( 'white' )

		shuffle['black'].setValue( 'red2' )
		shuffle['white'].setValue( 'green2' )
		shuffle['red2'].setValue( 'blue2' )
		shuffle['green2'].setValue( 'alpha2' )

		shuffle['out'].setValue( 'rgba' )
		shuffle['out2'].setValue( 'none' )

		shuffle.setInput(0, inputNode)
		shuffle['hide_input'].setValue(1)
		shuffle.setXYpos(x, y)
		inputNode = shuffle
		y += yspacing*1.5

		if use_targa:
			# try:
			# 	os.makedirs(writedir)
			# except WindowsError:
			# 	pass
			write = nuke.nodes.Write()
			write['channels'].setValue('rgba')
			write['file'].setValue(path.join(writedir,name+'.tga'))
			write.setInput(0, shuffle)
			write.setXYpos(x,y)
			y += yspacing

			read = nuke.nodes.Read()
			read['file'].setValue(path.join(writedir,name+'.tga'))
			read.setXYpos(x,y)
			y += yspacing*2

		crop = nuke.nodes.Crop()
		crop['box'].setValue(l.attrs['x'], 0)
		crop['box'].setValue(l.attrs['y'], 1)
		crop['box'].setValue(l.attrs['r'], 2)
		crop['box'].setValue(l.attrs['t'], 3)
		if use_targa:
			crop.setInput(0, read)
		else:
			crop.setInput(0, shuffle)
		crop.setXYpos(x, y)
		y += yspacing
		groupLayer = crop
		render_in = crop
		
		if lastGroupLayer:#is exists
			psdMerge = _newPsdMerge(l)
			psdMerge.setInput(0, lastGroupLayer)
			psdMerge.setInput(1, groupLayer)
			psdMerge.setXYpos(x, y)
			lastGroupLayer = psdMerge
			render_in = psdMerge
		else:
			dot = nuke.nodes.Dot()
			dot.setInput( 0, groupLayer )
			dot.setXYpos( x + dotXfudge, y + dotYfudge )
			lastGroupLayer = dot
		y += yspacing

		# renderlayer
		if renderlayer and name.lower().endswith(renderlayer):
			# premult = nuke.nodes.Premult()
			# premult['postage_stamp'].setValue(1)
			# premult.setInput(0, render_in)
			# premult.setXYpos(x, y)
			# y += yspacing*1.5

			# renderLayer = premult #to be delete

			proj = nuke.nodes.Project3D()
			proj.setInput(0, render_in)
			proj.setXYpos(x, y)
			y += yspacing

			readgeo = nuke.nodes.ReadGeo2()
			readgeo['file'].setValue(path.join(geodir,'_'.join(name.split('_')[:-1]))+'.abc') #or .obj or.. something
			readgeo.setInput(0, proj)
			readgeo['read_on_each_frame'].setValue(0)
			readgeo['sub_frame'].setValue(0)
			readgeo.setXYpos(x, y)
			y += yspacing

			# scene = nuke.nodes.Scene()
			# scene.setInput(0, readgeo)
			# scene.setXYpos(x, y)
			# y += yspacing*2

			scanline = nuke.nodes.ScanlineRender()
			scanline.setInput(1, readgeo)
			scanline.setXYpos(x, y)
			y += yspacing

			renderLayer = scanline
			
			psdMerge = _newPsdMerge(l, operation_overwrite='normal')
			psdMerge.setInput(0, lastRenderLayer)
			psdMerge.setInput(1, renderLayer)
			psdMerge.setXYpos(x,y)
			lastRenderLayer = psdMerge
		y += yspacing
		bottom = y

	return lastRenderLayer

def breakoutLayers(node):
	if not node:
		return
	use_targa = nuke.ask('tga파일로 뽑을까요?')
	if use_targa:
		writedir = nuke.getFilename('tga를 저장할 디렉토리를 선택해주세요')
		if not writedir:
			return
	# geodir = nuke.getFilename('geometry를 읽을 디렉토리를 선택해주세요')
	# if not geodir:
	# 	return
	# use_targa=False
	geodir='c:/tmp/'
	# nuke.Undo().begin()

	nodepos = (node.xpos(), node.ypos()+100)
	sketch = _parseLayers(node, items=['alpha','sketch'], renderlayer='sketch', extractposition=nodepos, geodir='c:/tmp/data/scene_cache', use_targa=False)
	nodepos = (node.xpos(), node.ypos()+1300)
	tone = _parseLayers(node, items=['alpha','tone'], renderlayer='tone', extractposition=nodepos, geodir='c:/tmp/data/scene_cache', use_targa=False)
	nodepos = (node.xpos(), node.ypos()+2600)
	etc = _parseLayers(node, items='*', exceptlayer=['alpha', 'sketch', 'tone'], extractposition=nodepos, geodir='c:/tmp/data/scene_cache', use_targa=False)

	merge = nuke.nodes.PSDMerge()
	x = tone.xpos()+600
	y = tone.ypos()
	merge.setXYpos(x, y)
	merge.setInput(0, sketch)
	merge.setInput(1, tone)

#run
breakoutLayers(nuke.selectedNode())