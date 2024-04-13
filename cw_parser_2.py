import re
import os
from typing import Generator
from typing import Optional as Opt

workshop_path = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\281990"
mod_docs_path = "C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod"
vanilla_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stellaris"

# dummies so I can refer to these before they're properly defined
class mod():
	pass
class CWElement():
	pass

def quote(s:str) -> str:
	'''puts quote marks around a string'''
	s = s.replace( '\"' , '\\\"' )
	return "\"{}\"".format(s)

def indent( s:str, count:int=1 ) -> str:
	tabs = '\n'
	for i in range(count):
		tabs += '\t'
	return s.replace("\n",tabs)

def quoteIfNecessary(s:str) -> str:
	'''puts a quote around a string iff it is empty or contains whitespace'''
	if " " in s or "\n" in s or "\t" in s or s=="":
		return quote(s)
	else:
		return(s)

def decomposeWord(s:str):
	units = ['']
	for char in s:
		if char in ['@','.',':']:
			units.append(char)
			units.append('')
		else:
			units[-1].append(char)


def generate_joined_folder(path:str,*args) -> str:
	'''like os.path.join, except it only takes 2 arguments and it will create a folder if it doesn't already exists'''
	for folder in args:
		path = os.path.join(path,folder)
		if not os.path.exists(path):
			os.mkdir(path)
	return path

class mod():
	'''class for representing mods.
	parameters:
	workshop_item (optional): The number for this mod in Steam Workshop.
	mod_path (optional): The path for this mod. If not specified it will be derived from workshop_item.
	parents (optional): List of other mods to assume are also loaded if this one is, in reverse load order. Default [].
	is_vanilla (optional): Boolean that indicates whether a mod object is vanilla. Default False.
	vanilla_object (optiona): overwrites the default vanilla mod object
	'''
	def __init__( self, workshop_item:Opt[str] = None, mod_path:Opt[str] = None, parents:list[mod] = [], is_vanilla:bool=False, vanilla_object = None ) -> None:
		if mod_path is None:
			self.mod_path = os.path.join( workshop_path, workshop_item )
		else:
			self.mod_path = mod_path
		if is_vanilla:
			self.inheritance_list = [self]+parents
		else:
			if vanilla_object is None:
				vanilla_object = vanilla_mod_object
			self.inheritance_list = [self]+parents+[vanilla_object]
		self.is_vanilla = is_vanilla

	def inheritance(self) -> Generator[mod,None,None]:
		'''yields the mod, then each of its parents in reverse load order, then vanilla'''
		for mod in self.inheritance_list:
			yield mod

	def lookupInline(self,inline:str) -> str:
		'''returns the path to the file an inline script would find if used with this mod, its parents, and no other mods
		parameters:
		inline'''
		inline_breakdown = inline.split('/')
		inline_path = os.path.join('common','inline_scripts')
		for folder in inline_breakdown:
			inline_path = os.path.join( inline_path, folder )
		inline_path = inline_path+'.txt'
		for mod in self.inheritance():
			try_path = os.path.join( mod.mod_path, inline_path )
			if os.path.exists(try_path):
				return try_path
			
	def folder( self, path:str ) -> str:
		return os.path.join( self.mod_path, path )
	
	def getFiles( self, path:str, exclude_files:list[str]=[], include_parents:bool=False, file_suffix:str='.txt' ):
		exclude_files = exclude_files.copy()
		for mod in self.inheritance_list:
			if (mod is self) or include_parents:
				folder = mod.folder(path)
				if os.path.exists(folder):
					for file in os.listdir(path=folder):
						if file.endswith(file_suffix) and not file in exclude_files:
							filepath = os.path.join(folder,file)
							exclude_files.append(file)
							yield filepath

	def read_folder(self, path:str, exclude_files:list[str]=[], replace_local_variables:bool=False, include_parents:bool=False, file_suffix:str='.txt', parser_commands=None, overwrite_type:Opt[str]='LIOS' ) -> list[CWElement]:
		'''reads and parses the files in the specified folder in this mod into a list of CWElements
		parameters:
		path: the path to the specified folder, relative to the mod
		exclude_files (optional): a lost of filenames to skip, e.g. because the entries within are dummy elements or because they're assumed to have been overwritten
		replace_local_variables (optional): if True, locally-defined scripted variables will be replaced with their values.
		include_parents (optional): if True, also load contents of parent folders that aren't file-overwritten
		file_suffix (optional): only files with this suffix will be read. Default '.txt'
		parser_commands (optional): if this is set to a string or list of strings, the following tags will be enabled (where KEY stands for any of the entered strings):
		"#KEY:skip", "#KEY:/skip": ignore everything between these tags (or from the "#KEY:skip" to the end of the string if "#KEY:/skip" is not encountered)
		"#KEY:add_metadata:<metadata key>:<metadata value>": set the specified attribute in the "metadata" dictionary to the specified value for the next object
		"#KEY:add_block_metadata:<metadata key>:<metadata value>", "#KEY:/add_block_metadata:<metadata key>": set the specified attribute in the "metadata" dictionary to the specified value for each top-level object between these tags
		'''
		CW_list = []
		for filepath in self.getFiles( path, exclude_files=exclude_files, include_parents=include_parents, file_suffix=file_suffix ):
			CW_list = CW_list + fileToCW( filepath, replace_local_variables=replace_local_variables, parser_commands=parser_commands, overwrite_type=overwrite_type )
		return CW_list


vanilla_mod_object = mod( mod_path = vanilla_path, is_vanilla = True )

dlc_list = [
	'Arachnoid Portrait Pack',
	'Plantoids Species Pack',
	'Creatures of the Void Portrait Pack',
	'Leviathans Story Pack',
	'Horizon Signal',
	'Utopia',
	'Anniversary Portraits',
	'Synthetic Dawn Story Pack',
	'Apocalypse',
	'Humanoids Species Pack',
	'Distant Stars Story Pack',
	'Ancient Relics Story Pack',
	'Lithoids Species Pack',
	'Federations',
	'Necroids Species Pack',
	'Nemesis',
	'Aquatics Species Pack',
	'Overlord',
	'Toxoids Species Pack',
	'Symbols of Domination',
	'Paradox Account Sign-up Bonus',
	'Original Game Soundrack',
]

government_triggers = {
	'country_type':'is_country_type',
	'species_class':'is_species_class',
	'species_archetype':'is_species_class',
	'origin':'has_origin',
	'ethics':'has_ethic',
	'authority':'has_authority',
	'civics':'has_civic',
}

def match( string1:Opt[str], string2:Opt[str] ) -> bool:
	'''checks that, of two strings, either both exist or nether exists, and both are the same except for case'''
	if string1 is None:
		return string2 is None
	else:
		m = string1.lower() == string2.lower()
		return m

def to_yesno(bool:bool) -> str:
	'''converts a boolean to the string "yes" or "no", to match Stellaris syntax'''
	if bool:
		return "yes"
	else:
		return "no"

def getQuotedString(tokens):
	words = []
	while len(tokens)>0:
		nextToken = tokens.pop(0)
		if nextToken == "\"":
			return " ".join(words)
		else:
			nextToken = nextToken.replace("\\\"","\"")
			words.append(nextToken)

class CWElement():
	'''class representing a Clausewitz script element of form "<key> = <value>", "<key> <= <value>", <key> = { <parameters> } etc.'''
	def __init__( self, name:str, comparison:Opt[list[str]]=None, value:Opt[str]=None, subelements:Opt[list[CWElement]]=None, parent:Opt[CWElement]=None, filename:Opt[str]=None, overwrite_type:Opt[str]=None, mod:Opt[mod]=None ):
		self.name = name
		self.comparison = comparison
		self.value = value
		self.subelements = subelements
		self.parent = parent
		self.metadata = {}
		self.filename = filename
		self.overwrite_type = overwrite_type
		self.mod = mod
	
	def __str__(self) -> str:
		return self.getString()
	
	def __repr__(self) -> str:
		return self.name
	
	def set_name(self,name):
		self.name = name

	def parse( self, tokens:list[str], replace_local_variables:bool=False, local_variables:dict[str,str]={}, mod:Opt[mod]=None ) -> CWElement:
		while len(tokens)>0:
			nextToken = tokens.pop(0)
			if nextToken.startswith('@') and replace_local_variables:
				if nextToken in local_variables:
					nextToken = local_variables[nextToken]
			if nextToken == "\"":
				nextToken = getQuotedString(tokens)
			if nextToken in ("=","<",">"):
				self.comparison.append(nextToken)
			elif nextToken == "{":
				self.subelements = parseCW( tokens, parent=self, filename=self.filename, replace_local_variables=replace_local_variables, local_variables=local_variables, mod=mod )
				return self
			elif nextToken == "hsv":
				self.value = "hsv"
			else:
				self.value = nextToken
				if self.name.startswith('@') and replace_local_variables:
					local_variables[self.name]=nextToken
				return self

	def getElements(self,key:str) -> Generator[CWElement,None,None]:
		'''yields each subelement of this block with the specified key'''
		for element in self.subelements:
			if match( element.name, key ):
				yield element

	def hasAttribute(self,key:str) -> bool:
		'''checks if a block contains a subelement with the given key'''
		if not self.hasSubelements():
			return False
		for element in self.getElements(key):
			return True
		return False

	def getElement(self,key:str) -> CWElement:
		'''returns the first subelement of this block with the specified key'''
		if not self.hasSubelements():
			return CWElement("",parent=self)
		for element in self.getElements(key):
			return element
		return CWElement("",parent=self)

	def getValue(self,key:str,default:str="no",if_complex=None) -> str:
		'''returns the right-hand value of the first subelement of this block with the specified key'''
		if not self.hasSubelements():
			return default
		for element in self.getElements(key):
			if element.value is None:
				if if_complex is None:
					return default
				else:
					return if_complex
			else:
				return element.value
		return default
	
	def hasKeyValue(self,key:str,value:str):
		for element in self.getElements(key):
			if match( element.value, value ):
				return True
		return False

	def getValues(self,key:str) -> Generator[str,None,None]:
		'''yields the right-hand value of each subelement of this block with the specified key'''
		for element in self.getElements(key):
			yield element.value

	def getValueBoolean(self,key:str,default:bool=False) -> bool:
		'''returns the boolean value of the first subelement of this block with the specified key'''
		for element in self.getElements(key):
			return element.value != "no"
		return default

	def getArrayContents(self,key:str) -> Generator[str,None,None]:
		'''yields each string within the specified array subelement'''
		for element in self.getElements(key):
			for entry in element.subelements:
				yield entry.name

	def getArrayContentsFirst( self, key:str, default:str="no" ) -> str:
		'''returns the first string within the specified array subelement'''
		for element in self.getElements(key):
			for entry in element.subelements:
				return entry.name
		return default

	def getArrayContentsElements(self,key:str) -> Generator[CWElement,None,None]:
		'''yeilds each element within the specified array subelement'''
		for element in self.getElements(key):
			for entry in element.subelements:
				yield entry


	def hasSubelements(self) -> bool:
		'''yeilds True for objects of form <key> = { <contents> } (including empty blocks), false for attributes of form <key> = <value> or <key>'''
		if self.subelements is not None:
			return True
		else:
			return False

	def expand(self) -> bool:
		'''Returns a boolean which should generally indicate whether this object's text form should contain linebreaks'''
		if not self.hasSubelements():
			return False
		elif len(self.subelements) == 0:
			return False
		elif len( self.subelements ) > 1:
			return True
		elif self.subelements[0].hasSubelements():
			return True
		else:
			return False

	def getString(self) -> str:
		'''Converts the CWobject back into a Clausewitz script string.'''
		if self.name is not None:
			words = [ quoteIfNecessary(self.name) ]
		else:
			words = [ ]
		if self.comparison is not None:
			words.append("".join(self.comparison))
		if self.value is not None:
			words.append( quoteIfNecessary(self.value) )
		if self.subelements is not None:
			if self.expand():
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				bracketContentsString = "\n".join(bracketContents)
				bracketContentsString = indent(bracketContentsString)
				subelementString = "{{\n\t{}\n}}".format(bracketContentsString)
			else:
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				bracketContentsString = " ".join(bracketContents)
				subelementString = "{{ {} }}".format(bracketContentsString)
			words.append(subelementString)
		return(" ".join(words))

	def getContentsString( self, include_brackets:bool=True ) -> str:
		words = []
		if self.subelements is not None:
			if self.expand():
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				subelementString = "\n".join(bracketContents)
				subelementString = indent(subelementString)
				if include_brackets:
					subelementString = "{{\n\t{}\n}}".format(subelementString)
			else:
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				subelementString = " ".join(bracketContents)
				if include_brackets:
					subelementString = "{{ {} }}".format(subelementString)

			words.append(subelementString)
		elif self.value is not None:
			words.append(self.value)
		return(" ".join(words))

	def convertGovernmentTrigger(self,trigger:str=None) -> CWElement:
		# print(self)
		'''returns a copy of a government requirements block converted to normal trigger syntax'''
		# text = <loc key> handled separately, at the next level up
		if match( self.name, 'text' ):
			return ""
		# convert "value = <whatever>" to "has_ethic = <whatever>", "has_authority = whatever" etc.
		elif match( self.name, 'value' ):
			output = CWElement(trigger,['='],self.value)
		# "always = yes/no" remains unchanged
		elif match( self.name, 'always' ):
			output = CWElement('always',['='],self.value)
		# convert "ethic" blocks, "authority" blocks etc. into AND blocks if necessary
		elif self.name in government_triggers:
			output = CWElement('AND',['='],subelements=[])
			for element in self.subelements:
				if not match( element.name, 'text' ):
					output.subelements.append( element.convertGovernmentTrigger( government_triggers[self.name] ) )
			# no AND block needed for a single trigger
			if len( output.subelements ) == 1:
				output = output.subelements[0]
		# AND, OR etc. blocks remain unchanged
		else:
			output = CWElement(self.name,['='],subelements=[])
			for element in self.subelements:
				if not match( element.name, 'text' ):
					output.subelements.append( element.convertGovernmentTrigger( trigger ) )
		# convert "text = <loc key>" to custom_tooltip
		if self.hasAttribute('text'):
			text_element = CWElement('text',['='],self.getValue('text'))
			if output.name == 'AND':
				return CWElement('custom_tooltip',['='],subelements=[text_element]+output.subelements)
			else:
				return CWElement('custom_tooltip',['='],subelements=[text_element,output])
		else:
			return output

	def getRoot(self) -> CWElement:
		'''returns the top-level object containing this one'''
		if self.parent is None:
			return self
		else:
			return self.parent.getRoot()

	def replaceInlines( self, mod:mod, parser_commands=None ) -> None:
		'''Expands all inline scripts within this element.
		parameters:
		mod: the function will assume this mod, its parents, and no other mods are installed'''
		if self.hasSubelements():
			self.subelements = replaceInlines(self.subelements,mod,parser_commands=parser_commands)

	def getArrayTriggers( self, block:str, trigger:str, mode=None, default='no' ) -> str:
		'''generates a trigger or effect block (in string form) from the contents of an array, e.g. you can use this to convert a prerequisite block to something of the form
		"AND = { has_technology = <tech> has_technology = <tech> }"
		block: the name of the array, e.g. "prerequisities"
		trigger: the name of the trigger to use in the output, e.g. "has_technology"
		mode: whether the triggers should be combined as "AND", "OR", "NAND", or "NOR". Default is appropriate for effect blocks.
		default: value to return if the array is nonexistant or empty
		'''
		lines = []
		for item in self.getArrayContents(block):
			lines.append( '{} = {}'.format( trigger, item ) )
		if mode == 'OR':
			if len(lines) == 0:
				return default
			elif len(lines) == 1:
				return lines[0]
			else:
				lines_block = ' '.join(lines)
				return 'OR = {{ {} }}'.format(lines_block)
		elif mode == 'NOR':
			if len(lines) == 0:
				return default
			elif len(lines) == 1:
				return 'NOT = {{ {} }}'.format(lines[0])
			else:
				lines_block = ' '.join(lines)
				return 'NOR = {{ {} }}'.format(lines_block)
		elif mode == 'AND':
			if len(lines) == 0:
				return default
			elif len(lines) == 1:
				return lines[0]
			else:
				lines_block = ' '.join(lines)
				return 'AND = {{ {} }}'.format(lines_block)
		elif mode == 'NAND':
			if len(lines) == 0:
				return default
			elif len(lines) == 1:
				return 'NOT = {{ {} }}'.format(lines[0])
			else:
				lines_block = ' '.join(lines)
				return 'NAND = {{ {} }}'.format(lines_block)
		else:
			if len(lines) == 0:
				return default
			elif len(lines) == 1:
				return lines[0]
			else:
				lines_block = ' '.join(lines)
				return lines_block
			
	def parent_hierarchy( self ):
		next_obj = self
		while next_obj is not None:
			yield next_obj
			next_obj = next_obj.parent


def replaceInlines( CWList:list[CWElement], mod:mod, parser_commands=None, filter=lambda x:True ) -> list[CWElement]:
	'''Given a list of CWElement, returns a copy of the list with any inline scripts expanded, including inline scripts in subelements. Mutates subelements of the list but not the list itself.
	parameters:
	CWList: the list to expand
	mod: the function will assume this mod, its parents, and no other mods are installed'''
	expanded = []
	for element in CWList:
		# if an inline script is found, try to expand it
		if match( element.name, 'inline_script' ) and filter(element):
			# if there are parameters, replace them before parsing
			if element.hasSubelements():
				script = mod.lookupInline( element.getValue('script') )
				if script is None:
					expanded.append(element)
				else:
					# found an inline, so we need to keep iterating
					found_inlines = True
					file = open(script,"r")
					script = file.read()
					file.close()
					for param in element.subelements:
						if param.value is None:
							val = ''
						else:
							val = param.value
						script = script.replace( '${}$'.format(param.name), val )
					inline_contents = stringToCW(script,filename=element.filename,parent=element.parent,parser_commands=parser_commands,overwrite_type=element.overwrite_type,mod=element.mod)
					inline_contents = replaceInlines(inline_contents,mod,parser_commands=parser_commands)
					expanded = expanded + inline_contents
			# if there are no parameters, read the file immediately
			else:
				script = mod.lookupInline( element.value )
				if script is None:
					expanded.append(element)
				else:
					# found an inline, so we need to keep iterating
					found_inlines = True
					inline_contents = fileToCW(script,filename=element.filename,parent=element.parent,parser_commands=parser_commands,overwrite_type=element.overwrite_type,mod=element.mod)
					inline_contents = replaceInlines(inline_contents,mod,parser_commands=parser_commands)
					expanded = expanded + inline_contents
			# print("replacing with script "+str(script))
		else:
			element.replaceInlines(mod,parser_commands=parser_commands)
			expanded.append(element)
	return expanded


def parseCW( tokens:list[str], parent:Opt[CWElement]=None, filename:Opt[str]=None, replace_local_variables=False, local_variables:dict[str,str]={}, overwrite_type:Opt[str]=None, mod:Opt[mod]=None ):
	'''creates a list of CWElements from a list of tokens'''
	elements = []
	block_metadata = {}
	unit_metadata = {}
	while len(tokens)>0:
		nextToken = tokens.pop(0)
		if nextToken == "":
			pass
		elif nextToken.startswith('|(PARSER:add_block_metadata:'):
			command_params = nextToken[28:-2] # strips initial "|(Parser:add_block_metadata:" and final ")|"
			command_params = command_params.split(':')
			if len(command_params)==1:
				block_metadata[command_params[0]] = True
			else:
				block_metadata[command_params[0]] = command_params[1]
		elif nextToken.startswith('|(PARSER:add_metadata:'):
			command_params = nextToken[22:-2] # strips initial "|(Parser:add_metadata:" and final ")|"
			command_params = command_params.split(':')
			if len(command_params)==1:
				unit_metadata[command_params[0]] = True
			else:
				unit_metadata[command_params[0]] = command_params[1]
		elif nextToken.startswith('|(PARSER:/add_block_metadata:'):
			command_params = nextToken[29:-2] # strips initial "|(Parser:/add_block_metadata:" and final ")|"
			command_params = command_params.split(':')
			block_metadata.pop(command_params[0])
		else:
			if nextToken == "\"":
				nextToken = getQuotedString(tokens)
			if nextToken in ("=","<",">"):
				lastElement.comparison = [nextToken]
				lastElement.parse( tokens, replace_local_variables=replace_local_variables, local_variables=local_variables )
			elif nextToken == "}":
				return elements
			elif nextToken == "{":
				e = CWElement(None,parent=parent,filename=filename,overwrite_type=overwrite_type,mod=mod)
				elements.append(e)
				for key in block_metadata:
					e.metadata[key] = block_metadata[key]
				for key in unit_metadata:
					e.metadata[key] = unit_metadata[key]
				unit_metadata = {}
				e.subelements = parseCW( tokens, e, filename=filename, replace_local_variables=replace_local_variables, local_variables=local_variables, mod=mod )
			else:
				e = CWElement(nextToken,parent=parent,filename=filename,overwrite_type=overwrite_type,mod=mod)
				elements.append(e)
				for key in block_metadata:
					e.metadata[key] = block_metadata[key]
				for key in unit_metadata:
					e.metadata[key] = unit_metadata[key]
				unit_metadata = {}
			lastElement = elements[-1]
	return elements
			

def stringToCW( string:str, filename:Opt[str]=None, parent:Opt[CWElement]=None, replace_local_variables:bool=False, parser_commands=None, overwrite_type:Opt[str]=None, mod:Opt[mod]=None ) -> list[CWElement]:
	'''parses a string into a list of CWElement objects
	parameters:
	string: The string to convert.
	filename (optional): Marks CWElements as being from the specified file.
	parent (optional): Marks CWElements as being children of the specified CWElement.
	replace_local_variables (optional): if True, locally-defined scripted variables will be replaced with their values.
	parser_commands (optional): if this is set to a string or list of strings, the following tags will be enabled (where KEY stands for any of the entered strings):
	"#KEY:skip", "#KEY:/skip": ignore everything between these tags (or from the "#KEY:skip" to the end of the string if "#KEY:/skip" is not encountered)
	"#KEY:add_metadata:<metadata key>:<metadata value>": set the specified attribute in the "metadata" dictionary to the specified value for the next object
	"#KEY:add_block_metadata:<metadata key>:<metadata value>", "#KEY:/add_block_metadata:<metadata key>": set the specified attribute in the "metadata" dictionary to the specified value for each top-level object between these tags
	'''
	# replace parser command tokens with something that doesn't start with "#" so they don't get removed with comments
	if parser_commands is not None:
		if isinstance(parser_commands,str):
			parser_command_template = r"#{}:([^ \n]*)".format(parser_commands)
			string = re.sub( parser_command_template, r"\|\(PARSER:$1\)\|", string )
		elif isinstance(parser_commands,list):
			for key in parser_commands:
				parser_command_template = r"#{}:([^ \n]*)".format(key)
				string = re.sub( parser_command_template, r"\|\(PARSER:$1\)\|", string )
	# remove comments
	string = string+"\n"
	string = re.sub(r"#.*\n",r" ",string)
	# put spaces around special characters so split(' ') makes them into separate tokens
	string = string.replace("="," = ")
	string = string.replace("<"," < ")
	string = string.replace(">"," > ")
	string = string.replace("{"," { ")
	string = string.replace("}"," } ")
	string = string.replace("\""," \" ")
	string = string.replace("\\ \""," \" ")
	# split by whitespace blocks to generate token list
	tokenList = re.split("\s+",string)
	# apply parser commands
	if parser_commands is not None:
		i = 0
		while i < len(tokenList):
			token = tokenList[i]
			if token == '|(PARSER:skip)|':
				while token != '|(PARSER:/skip)|' and i < len(tokenList):
					token = tokenList.pop(i)
			else:
				i += 1
	# parse token list
	cw = parseCW( tokenList, filename=filename, parent=parent, replace_local_variables=replace_local_variables, overwrite_type=overwrite_type, mod=mod )
	return cw


def fileToCW( path:str, filename=None, parent:Opt[CWElement]=None, replace_local_variables:bool=False, parser_commands=None, overwrite_type:Opt[str]='LIOS', mod:Opt[mod]=None )->list[CWElement]:
	'''reads and parses a file into a list of CWElement objects
	parameters:
	path: The file path.
	parent (optional): Marks CWElements as being children of the specified CWElement (for use in the CWElement.replaceInlines method).
	replace_local_variables (optional): if True, locally-defined scripted variables will be replaced with their values.
	parser_commands (optional): if this is set to a string or list of strings, the following tags will be enabled (where KEY stands for any of the entered strings):
	"#KEY:skip", "#KEY:/skip": ignore everything between these tags (or from the "#KEY:skip" to the end of the string if "#KEY:/skip" is not encountered)
	"#KEY:add_metadata:<metadata key>:<metadata value>": set the specified attribute in the "metadata" dictionary to the specified value for the next object
	"#KEY:add_block_metadata:<metadata key>:<metadata value>", "#KEY:/add_block_metadata:<metadata key>": set the specified attribute in the "metadata" dictionary to the specified value for each top-level object between these tags
	'''
	file = open(path,"r")
	try:
		fileContents = file.read()
	except:
		fileContents = ""
	if filename is None:
		filename = os.path.basename(path)
	cw = stringToCW( fileContents, filename=filename, parent=parent, replace_local_variables=replace_local_variables, parser_commands=parser_commands, overwrite_type=overwrite_type, mod=mod )
	file.close()
	return cw

def CWToString(elements:list[CWElement]) -> str:
	# converts a list of CWElements into a Clausewitz script string
	cwStrings = []
	for e in elements:
		cwStrings.append(e.getString())
	return "\n\n".join(cwStrings)

