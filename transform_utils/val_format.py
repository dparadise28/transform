boolean = {
	'SUCCESS': True,  'true' : True,  'True' : True,  'TRUE' : True,  '1': True,  1: True,  True : True,
	'FAILED' : False, 'false': False, 'False': False, 'FALSE': False, '0': False, 0: False, False: False,
}

# key = dollars_as_currency
def FORMATTER_FUNC_dollars_as_currency(amount, dirrection = 'unspecified', cents = False):
	# print(amount, type)
	if type(amount) in (int, float):
		# expects dollar amount (convert if told to do so)
		if cents: amount /= 100
		
		if amount < 0 or dirrection == 'neg':
			return '-${:,.2f}'.format(-amount)
		else:
			return '${:,.2f}'.format(amount)
	else:
		# might be useful to log information or raise an error?
		return None # Need to think about sensible return would be. configurable? explicit? static?

# key = cents_as_currency
def FORMATTER_FUNC_cents_as_currency(amount, dirrection = 'unspecified'):
	print(amount)
	return FORMATTER_FUNC_dollars_as_currency(amount, dirrection = 'unspecified', cents = True)

# key = as_free_or_currency
def FORMATTER_FUNC_as_free_or_currency(amount, dirrection = None):
	if amount:
		if dirrection == 'neg':
			return as_neg_currency(amount)
		else:
			return as_currency(amount)
	else:
		return 'FREE'

# key = as_pos_currency
def FORMATTER_FUNC_as_pos_currency(amount):
	return as_currency(amount, 'pos')

# key = as_neg_currency
def FORMATTER_FUNC_as_neg_currency(amount):
	return as_currency(amount, 'neg')

# key = as_free_or_pos_currency
def FORMATTER_FUNC_as_free_or_pos_currency(amount):
	as_free_or_currency(amount, 'pos')

# key = as_free_or_neg_currency
def FORMATTER_FUNC_as_free_or_neg_currency(amount):
	as_free_or_currency(amount, 'neg')

# key = to_string
def FORMATTER_FUNC_to_string(val):
	return str(val)

# key = to_number
def FORMATTER_FUNC_to_number(val):
	try:
		float(val)
	except:
		return 0


# elif fmat[key]       == 'str'           : val = str(val)
# elif fmat[key]       == 'd2l'           : val = val.values() 
# elif fmat[key]       == 'dk2l'          : val = sum([promo.keys() for promo in val], []) if type(val) == list else []
# elif fmat[key]       == 'boolean'       : val = boolean[val] if val in boolean.keys() else val
# elif fmat[key]       == 'promo'         : val = [{'name': promo, 'message': ''} for promo in val]
# elif fmat[key]       == 'int2date'      : val = datetime.datetime.utcfromtimestamp(int(str(val if val != '' else 0)[0:10])).strftime('%m/%d/%Y')
# elif fmat[key]       == 'decrypt'       :
   # try   : val = decrypt_password(val)
   # except: pass