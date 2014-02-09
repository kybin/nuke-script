import nuke
import nukescripts

import os
import os.path as ospath
import re
import glob
import random

def tempWrite():
	maxnum = 999999
	randnum = str(random.randint(1, maxnum)).zfill(len(str(maxnum)))

	# set cache directory
	try:
		scriptdir, _ = ospath.split(nuke.scriptName())
		cachedir = ospath.join(scriptdir, 'garbage_cache', randnum)
	except RuntimeError:
		cachedir = ospath.join(ospath.expanduser('~/garbage_cache'), randnum)

	# create the directory
	try:
		os.makedirs(cachedir)
	except OSError:
		if not ospath.isdir(cachedir):
			raise

	write = nuke.createNode('Write')
	write.setName('temp_write1')
	write['file'].setValue('{0}.####.tga'.format(ospath.join(cachedir, randnum))) # Join again(!) for the image seq's name.
	write['channels'].setValue('rgba')

def defaultWrite():
	if nuke.NUKE_VERSION_MAJOR >= 7:
		writepath = ''
		try:
			writepath, _ = ospath.splitext(nuke.scriptName())
		except RuntimeError:
			pass
	else:
		writepath = nuke.Root().name()

	write = nuke.createNode('Write')
	write['file'].setValue(writepath)

def pathRange(path):
	globfiles = glob.glob(re.sub('%0\dd', '*', path))
	try:
		frames = [re.findall('(\d+).\w+$', f)[0] for f in globfiles]
		fmin = int(min(frames))
		fmax = int(max(frames))
	except (IndexError, ValueError):
		return 1,1
	return fmin, fmax

def readFromWriteNode(writenode):
	rname =  '_'.join(['Read', writenode.name()])
	if nuke.toNode(rname):
		print('node already exists')
		return

	w = writenode
	r = nuke.createNode('Read')

	r['name'].setValue(rname)
	r['file'].setValue(w['file'].value())
	fmin, fmax = pathRange(w['file'].value())
	r['first'].setValue(fmin)
	r['last'].setValue(fmax)
	r['origfirst'].setValue(fmin)
	r['origlast'].setValue(fmax)
	r['xpos'].setValue(w['xpos'].value())
	r['ypos'].setValue(w['ypos'].value()+50)

def myRead():
	sels = nuke.selectedNodes()
	writes = []
	for s in sels:
		if s.Class()=='Write':
			writes.append(s)
	if writes:
		for w in writes:
			if s.Class()=='Write':
				readFromWriteNode(s)
	else:
		if len(sels)==1:
			sel = nuke.selectedNode()
			if sel.Class()=='Read':
				fmin, fmax = pathRange(sel['file'].value())
				sel['first'].setValue(fmin)
				sel['last'].setValue(fmax)
				sel['origfirst'].setValue(fmin)
				sel['origlast'].setValue(fmax)
		elif not sels:
			nukescripts.create_read()
