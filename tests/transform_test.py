import transform
import json
import os

with open(os.path.join(*["tests", "generic_conf.json"])) as conf:
	conf = json.loads(conf.read())
	t = transform.Remodeler(conf)

	for t_case in ["1"]:		
		dir = ["tests", "test_cases", str(t_case)]
		old_struct, new_struct = "unprocessed.json", "expected.json"
		with open(os.path.join(*(dir + [old_struct]))) as old:
			with open(os.path.join(*(dir + [new_struct]))) as new:
				new_json = json.loads(new.read())
				old_json = json.loads(old.read())
				print(json.dumps(t.remodel_nested_dict(old_json, new_json), indent = 4))
				# print(t.remodel_nested_dict(old_json, new_json))
				# t.remodel_nested_dict(old_json, new_json)