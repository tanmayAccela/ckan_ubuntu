'''
Created on Feb 9, 2015

@author: tthakur
'''
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import formencode.validators as v

def create_access_levels():
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'access_levels'}
        tk.get_action('vocabulary_show')(context, data)
    except tk.ObjectNotFound:
        data = {'name': 'access_levels'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'Public', u'Restricted Public', u'Non Public'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)

def access_levels():
    create_access_levels()
    try:
        tag_list = tk.get_action('tag_list')
        access_levels = tag_list(data_dict={'vocabulary_id': 'access_levels'})
        return access_levels
    except tk.ObjectNotFound:
        return None

class MyPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    
    #add all the extra fields here
    def _modify_package_schema(self, schema):
        schema.update({ 
                       'modified': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')], 
                       'publisher': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
                       'identifier': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
                       'Access Level': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_tags')('access_levels')],
                       'bureau_code': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
                       'prog_code': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
                       'contact_name': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
                       'contact_email': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')]
        })
        # Add our custom_resource_text metadata field to the schema
        '''
        schema['resources'].update({
                'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
                })
        '''
        return schema
    
    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(MyPlugin, self).create_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema
    
    def update_package_schema(self):
        schema = super(MyPlugin, self).update_package_schema()
        #our custom field
        schema = self._modify_package_schema(schema)
        return schema
    
    def show_package_schema(self):
        schema = super(MyPlugin, self).show_package_schema()
        schema.update({ 
                       'modified': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
                       'publisher': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing') ],
                       'identifier': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
                       'bureau_code': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
                       'prog_code': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
                       'contact_name': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
                       'contact_email': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')]
        })
        
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
        schema.update({
                       'access_level' : [ tk.get_converter('convert_from_tags')('access_levels'), tk.get_validator('ignore_missing')]
                       })
        '''
        schema['resources'].update({
                'custom_resource_text' : [ tk.get_validator('ignore_missing') ]
            })
        '''
        return schema
    
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        
    
    p.implements(p.ITemplateHelpers)
    def get_helpers(self):
        return {'access_levels': access_levels}