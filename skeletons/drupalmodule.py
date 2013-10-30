import string
import os
import glob
import string
import shutil


basic_module_info_template = string.Template(
'''name = $module_name
core = 7.x
package = other
dependencies[] = node''')


basic_module_module_template = string.Template(
'''<?php
''')

migrate_module_info_template = string.Template(
'''name = $module_name
core = 7.x
package = other
dependencies[] = migrate''')

migrate_module_csv_node_module_template = string.Template(
'''<?php

function ${module_name}_migrate_api() {
	return array(
		'api' => 2,
		'migrations' => array(
			'${migrate_machine_name}' => array('class_name' => ${migrate_class_name}),
		),
	);
}

class ${migrate_class_name} extends Migration {
	public function __construct($arguments) {
		parent::__construct();
		$csv_filepath = '';
	
		$this->description = t('');

		$csv_columns = array();

		$this->source = new MigrateSourceCSV($csv_filepath, $columns, array('header_rows' => 1, 'embedded_newlines' => 1));

		$this->destination = new MigrateDestinationNode('${migrate_content_type}');
		
		$this-> map = new MigrateSQLMap($this->machineName,
			array(
				'csv_id' => array(
					'type' => 'int',
					'unsigned' => TRUE,
					'not null' => TRUE,
					'alias' => 'import',
				),
			),
			MigrateDestinationNode::getKeySchema()
		);

		$this->addSimpleMappings(array(
			'title',
		));

	}

	public function prepareRow($row) {
	  // Always include this fragment at the beginning of every prepareRow()
	  // implementation, so parent classes can ignore rows.
		if (parent::prepareRow($row) === FALSE) {
			return FALSE;
		}

		#title required
		if ($row->title	== '') {
			return FALSE; 
		}
		
		return TRUE;
	}

	function prepare(&$row) {
	}

}

''')



def create():
		module_name = raw_input('Enter module name: ')
		if module_name == '':
			module_name = 'temporary'

		module_type = raw_input('Module type (basic, migrate): ')
		if module_type != 'basic' and module_type != 'migrate':
			module_type = 'basic'

		module_dir = os.path.dirname(module_name)
		if not os.path.exists(module_dir):
			os.makedirs(module_name)

		#info file
		module_info_file = open(module_name + '/' + module_name + '.info', 'w')
		if module_type == 'basic':
			module_info_content = basic_module_info_template.safe_substitute(module_name = module_name)
		elif module_type == 'migrate':
			module_info_content = migrate_module_info_template.safe_substitute(module_name = module_name)

		module_info_file.write(module_info_content)
		module_info_file.close()


		#module file
		module_file = open(module_name + '/' + module_name + '.module', 'w')
		if module_type == 'basic':
			module_content = basic_module_module_template.safe_substitute()
		elif module_type == 'migrate':
			migrate_type = raw_input('migrate type (csv-node, ): ')
			if migrate_type != 'csv-node':
				migrate_type = 'csv-node'
			
			if migrate_type == 'csv-node':
				migrate_machine_name = raw_input('Migrate machine name: ')
				migrate_class_name = raw_input('Migrate class name: ')
				migrate_content_type = raw_input('Content type: ')
				
				d = {'module_name' : module_name,
					 'migrate_machine_name' : migrate_machine_name,
					 'migrate_class_name' : migrate_class_name,
					 'migrate_content_type' : migrate_content_type,
					 }
				module_content = migrate_module_csv_node_module_template.safe_substitute(d)

		module_file.write(module_content)
		module_file.close()
