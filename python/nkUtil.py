import nuke

def ndir(findstr='', ignorecase=True):
	if ignorecase:
		return [i for i in dir(nuke) if findstr.lower() in i.lower()]

	return [i for i in dir(nuke) if findstr in i]
