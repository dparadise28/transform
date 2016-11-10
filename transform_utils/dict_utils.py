from copy import deepcopy

def unpack(nested_dict, dict_name = 'main'):
	'''
		unpacks nested dicts
		
		example:
			nested_dict = {
				"1": "1",
				"2": {
					"2": ["4"]
				},
				"3": [{
					"1": "1",
					"3": [{
							"1": "1"
						}]
				}]
			}

		return:
			[
				{
					"main": {"2": {}, "1": "1", "3": []}
				},{
					"3": {"1": "1","3": []}
				},{
					"3": {"1": "1"}
				},{
					"2": {"2": ["4"]}
				}
			]
	'''
	extracted_lists = []
	def unpacked(r, key): #todo: reference to parent in dicts, removal of duplicates
		nonlocal extracted_lists
		def l(k, v):
			if isinstance(v[0], dict): extracted_dict.update({k: []}); unpacked(v[0], k)
			else: extracted_dict.update({k: v})
		def d(k, v): extracted_dict.update({k: unpacked(v, k)})
		def s(k, v): extracted_dict.update({k: v})

		protocol, extracted_dict = {list: l, dict: d, str : s,}, {}

		for k,v in r.items():
			protocol[type(v)](k, v)
		extracted_lists.append({key: extracted_dict}); return {}
	unpacked(nested_dict, dict_name); return list(reversed(extracted_lists))