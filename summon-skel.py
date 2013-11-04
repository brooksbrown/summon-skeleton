#!/usr/bin/env python

import sys
import os
import fnmatch
import skellib 


skel_dir = 'skeletons'


if __name__ == '__main__':
	
	skeletons = skellib.loadSkeletons(os.path.join(os.path.dirname(__file__), skel_dir))

	tag_objects = {} 
	tag_list = []
	for skel in skeletons:
		if skel.tag not in tag_list:
			tag_list.append(skel.tag)
			tag_objects[skel.tag] = [skel]
		else:
			tag_objects[skel.tag].append(skel)

	print ''
	i = 0
	for tag in tag_list:
		print str(i) + ' : ' + tag
		i += 1
	tag_selection = int(raw_input('Select a skeleton tag (0 - ' + str(i - 1) + ') : '))
	print ''

	print ''
	i = 0
	for skel in tag_objects[tag_list[tag_selection]]:
		print str(i) + ' : ' + skel.name
		i += 1
	print ''
	selection = int(raw_input('Select a skeleton (0 - ' + str(i - 1) + ') : '))
	if selection < 0 or selection > i:
		print 'selection out of range, exiting'
		exit

	skeleton = tag_objects[tag_list[tag_selection]][selection]
	skeleton_template_vars = skeleton.loadTemplateVariables()

	skeleton.createSkeleton('.', skeleton_template_vars)

		



