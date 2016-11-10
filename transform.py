import os, datetime, functools
from transform_utils import val_format
from copy import deepcopy

# need to change to local class variable (was used for testing but no good reason to stay in global scope)
config  = {}

class Remodeler:
	def __init__(self, configs):
		global config
		config = deepcopy(configs)
		self.formatter = {
			f_name.strip('FORMATTER_FUNC_'): f_val  
				for
			f_name, f_val in val_format.__dict__.items() 
				if
			'FORMATTER_FUNC_' in f_name
		}

	def remodel_flat_dict(self, original, template):
		'''
			configures api input arguments:

				original = inputs by user to be remapped with 
				template = key or key list to mapping dict

					eg:
					flat
						config: {
							template_desired: {
								new_key_1: old_key_1,
								new_key_1: old_key_2,
								...
							},
							map_i: {
								new_key_1: old_key_1,
								new_key_2: old_key_2,
								...
							},
							...
						}# template = template_desired or touple(template_desired)

					nested:

						config: {
							templates: {
								map1: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								}, map2: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								},
								...
								, template_desired: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								}, #config you need
								...
							}
						}# in this case template = (templates, template_desired)
		'''
		expected = deepcopy(config[template] if type(template) == str else self.retrieve(template, config, template))
		for key in expected:
			if type(expected[key]) == dict and expected[key].get('value', '') in original:
				expected[key] = self.format_val(original[expected[key]['value']], key)
			elif key in original:
				expected[key] = self.format_val(original[key], key)
			else:
				expected[key] = self.format_val('', key)
		return expected


	def retrieve(self, key_list, resp, ret_key, skip = False):
		'''
			retrieves a value from an arbitratily nested dict. the value returned will
			either be any valid field a dict/json object acceps, or false if no value
			was found given the dictionary and key list specified.

			inputs:
				key_list = tuple or list of keys used to traverse the dict
						   holding the desired value

				resp     = dict holding desired value

				ret_key  = key name for specific value to be returned for formatting purposes
		'''
		val = '' if not skip else resp
		try:
			val = functools.reduce(lambda d, k: d[k], key_list.split(config.get('key_delimiter', ' > ')), resp)
			return self.format_val(val, ret_key)
		except:
			return self.format_val(val, ret_key)


	def remodel_nested_dict(self, resp, ret, key = ''):
		'''
			This methos constructs the expected response the app is expecting
			(however flat or nested they may be)

			NOTE: It is highly dependant on the configuration setup

			inputs:
				resp = response from the api. Given the recursive nature of this
					   implementation this value will first be the full response
					   from the api; if the configuration calls for a list it will
					   retrieve a subset of the results to iterate through as multiple
					   values will be required for that response.
				ret  = the original config that is to be to basis for the remodelled
					   result
					   
			#TODO: rewrite to not need recursion. To do this you need to divide
				   into flat components, format each individually and reassemble
		'''
		configed_ret = deepcopy(ret)
		for result in ret:
			if type(result) == str and config.get('key_delimiter', ' > ') in result:
				configed_ret = [self.retrieve(result, val, key) for val in resp]
			elif type(ret[result]) == str:
				configed_ret[result] = self.retrieve(configed_ret[result], resp.copy(), result)
			elif type(ret[result]) == dict:
				configed_ret[result] = self.remodel_nested_dict(resp, configed_ret[result], result)
				if config.get('resp_structure_change', {}).get(result):
						configed_ret[result] = self.retrieve(['fail'], configed_ret[result], result, True)
			elif type(ret[result]) == list:
				temp, loop_through = [], config['loop_through_vals']
				for val in ret[result]:
					temp += [
						self.retrieve(val, val_in_list, result) 
							if type(val) == str
							else self.remodel_nested_dict(val_in_list, val, result)
						for val_in_list
							in self.retrieve(loop_through[result], resp, '')
					]
				configed_ret[result] = temp

		return configed_ret


	def format_val(self, val, key):
		'''
			val    = value to be formated if needed
			key    = key in the val_format dict to specify if and how the value
					 needs formating
		'''
		fmat_key = config.get('val_format', {}).get(key)
		if fmat_key and fmat_key in self.formatter:
			'''
				thinking of adding a type check on the value associated with the key to be formatted
					if type(fmat[key]) == str:
				
				for cases when you would like to perform multiple manipulations or have methods with
				more explicit instruction built or passed in
				
				eg:
					'name': [{
						"strip": ["MR. ", "MRS. ", ...],
					}, {
						"replace": [(' - ', ' '), ...],
					}...]
				
				the above is a list to retain order since the methods may be order dependant. Not
				sure if its worth is but figured I'd jot it down so I wouldn't forget.
			'''
			
			# this is ok for now but it might be useful to construct another structure for generic
			# inputs to the methods to retain more useful information in case its needed at times
			# (just another though)
			val = self.formatter[fmat_key](val)
		return val