import ConfigParser
import os
from string import Template

def listFiles(directory):
	for root, subdirectories, files in os.walk(directory):
		for subdirectory in subdirectories:
			yield os.path.join(directory, subdirectory)
		for afile in files:
			yield os.path.join(subdirectory, afile)
	return

class SkelSettings:

	filepath = ''
	config = None

	def __init__(self, filepath):
		self.filepath = filepath

		self.config = ConfigParser.ConfigParser()
		self.config.read(self.filepath)

	def getSections(self):
		return self.config.sections()
	
	def getSection(self, section):
		sectionDict = {}
		options = self.config.options(section)
		for option in options:
			try:
				sectionDict[option] = self.config.get(section, option)
			except:
				print('exception on %s!' % option)
				sectionDict[option] = None
		return sectionDict


class Skeleton:
	
	name = ''
	directory = ''
	tag = ''
	template_variables = None	

	def __init__(self, name, directory, template_variables):
		self.name = name
		self.directory = directory
		self.template_variables = template_variables

	def setTag(self, tag):
		self.tag = tag

	def loadTemplateVariables(self):
		variables = {} 
		for variable in self.template_variables:
			variables[variable.get('name')] = str(raw_input(variable.get('prompt') + ' : '))

		return variables

	def createSkeleton(self, destination, template_vars):
		for f in listFiles(os.path.join(self.directory, 'skel')):
			# f is the file path from the skeleton directory root,
			# so get the file path relative to the current skeleton
			relative_f = f.replace(self.directory + '/skel/', '')
			relative_f = Template(relative_f).substitute(template_vars)
			if os.path.isdir(f):
				os.makedirs(os.path.join(destination, relative_f))
			
			else:
				with open (os.path.join(self.directory, 'skel', f), 'r') as skel_file:
					data = skel_file.read()
					data = Template(data).safe_substitute(template_vars)
					out = open(os.path.join(destination, relative_f), 'w')
					out.write(data)
					out.close()


def loadSkeletons(skeletons_directory):
	skeletons = []

	# loop through directories in skeletons directory
	for skel in os.listdir(skeletons_directory):
		
		if os.path.isdir(os.path.join(skeletons_directory, skel)):
			skel_dir = os.path.join(skeletons_directory, skel)

			for skel_file in os.listdir(skel_dir):
				skel_settings_filepath = os.path.join(skel_dir, skel_file)
				file_name, ext = os.path.splitext(skel_settings_filepath)

				# if skeleton directory has the .skel python settings file add it
				if ext == '.skel':
					skel_conf = SkelSettings(skel_settings_filepath)
					settings = None
					template_variables = []

					for section in skel_conf.getSections():
						if section == 'settings':
							settings = skel_conf.getSection(section)
						else:
							section_before = skel_conf.getSection(section)
							section = {
									'name' : section,
									'prompt' : section_before.get('prompt')
								}
							template_variables.append(section)
					skeleton = Skeleton(settings.get('name'), skel_dir, template_variables)
					skeleton.setTag(settings.get('tag'))
					skeletons.append(skeleton)
							
	return skeletons
	



