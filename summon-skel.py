#!/usr/bin/env python

import sys



if __name__ == '__main__':
	skel_name = sys.argv[1]
	
	if skel_name == 'drupal-module':
		from skeletons import drupalmodule as dm
		dm.create()












