import re
import os
from types import MethodType
from shutil import rmtree
from copy import deepcopy

logfile = open('cw_converter_log.txt','w')
logfile.write('')
logfile.close()

logfile = open('cw_converter_log.txt','a')
def log(s):
	logfile.write(s+'\n')

workshop_path = "C:\Program Files (x86)\Steam\steamapps\workshop\content\\281990"
mod_docs_path = "C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod"

def quote(s):
	return "\"{}\"".format(s)

def quoteIfNecessary(s):
	s = s.replace( '\"' , '\\\"' )
	if " " in s or "\n" in s or "\t" in s or s=="":
		return quote(s)
	else:
		return(s)

def generate_joined_folder(location,name):
	path = os.path.join(location,name)
	if not os.path.exists(path):
		os.mkdir(path)
	return path

class mod():
	def __init__(self,key,workshop_item=None,mod_path=None,output_folder=None,parents=['vanilla'],vanilla=False,can_write=True,exported_file_index='01',overwrite=False) -> None:
		self.can_write = can_write
		self.overwrite = overwrite
		self.key = key
		if mod_path is None:
			self.mod_path = os.path.join( workshop_path, workshop_item )
		else:
			self.mod_path = mod_path
		if output_folder is None:
			output_folder = 'rstm_'+key
		output_folder = os.path.join( mod_docs_path, output_folder )
		# if can_write:
		# 	rmtree( os.path.join( output_folder, "common" ) )
		if can_write:
			output_folder = generate_joined_folder(output_folder,"common")
			inline_script_path = generate_joined_folder(output_folder,"inline_scripts")
			self.inline_script_path = generate_joined_folder(inline_script_path,"foreach")
			self.scripted_effect_path = generate_joined_folder(output_folder,"scripted_effects")
			self.scripted_trigger_path = generate_joined_folder(output_folder,"scripted_triggers")
			self.static_modifier_path = generate_joined_folder(output_folder,"static_modifiers")

			exported_triggers_file = os.path.join( self.scripted_trigger_path, '{}_rst_{}_exported_triggers.txt'.format(exported_file_index,key) )
			self.exported_triggers_file = exported_triggers_file
			exported_triggers_file = open(exported_triggers_file,'w')
			exported_triggers_file.write("")
			exported_triggers_file.close()

			exported_modifiers_file = os.path.join( self.static_modifier_path, '{}_rst_{}_exported_modifiers.txt'.format(exported_file_index,key) )
			self.exported_modifiers_file = exported_modifiers_file
			exported_modifiers_file = open(exported_modifiers_file,'w')
			exported_modifiers_file.write("")
			exported_modifiers_file.close()

			
		self.inheritance_list = [key]+parents
		self.vanilla = vanilla

	def inheritance(self):
		if self.vanilla:
			yield undercoat
		for key in self.inheritance_list:
			yield mod_data[key]

	def lookupInline(self,inline:str):
		inline_breakdown = inline.split('/')
		inline_path = 'common\inline_scripts'
		for folder in inline_breakdown:
			inline_path = os.path.join( inline_path, folder )
		inline_path = inline_path+'.txt'
		for mod in self.inheritance():
			try_path = os.path.join( mod.mod_path, inline_path )
			if os.path.exists(try_path):
				return try_path





mod_data = {
	'vanilla':mod( 'vanilla',
		vanilla=True,
		output_folder="repeating_script_templates",
		mod_path="C:\Program Files (x86)\Steam\steamapps\common\Stellaris",
		parents=[],
		exported_file_index="00",
	),
	'plandiv':mod( 'plandiv',
		workshop_item='819148835',
		exported_file_index="01",
	),
	'plandiv_hab':mod( 'plandiv_hab',
		workshop_item='1878751971',
		parents=["plandiv","vanilla"],
		exported_file_index="02",
	),
	'plandiv_unique':mod( 'plandiv_unique',
		workshop_item='1740165239',
		parents=["plandiv","vanilla"],
		exported_file_index="02",
	),
	'gigas':mod( 'gigas',
		workshop_item='1121692237',
		exported_file_index="01",
	),
	'ancientcaches':mod( 'ancientcaches',
		output_folder="rstm_acot",
		workshop_item='1419304439',
		exported_file_index="01",
	),
	'ancientcaches_sofe':mod( 'ancientcaches_sofe',
		output_folder="rstm_acot_sofe",
		workshop_item='1481972266',
		parents=["ancientcaches","vanilla"],
		exported_file_index="02",
	),
	'evolved':mod( 'evolved',
		output_folder="rstm_sevo",
		workshop_item='2602025201',
		parents=["plandiv_unique",
		"plandiv","vanilla"],
		exported_file_index="01",
	),
	'planetarywonders':mod( 'planetarywonders',
		workshop_item='2305790641',
		exported_file_index="01",
	),
	'guillismodifiers':mod( 'guillismodifiers',
		output_folder="rstm_guillis",
		workshop_item='865040033',
		exported_file_index="01",
	),
	'expandedespionage':mod( 'expandedespionage',
		workshop_item='2574175110',
		exported_file_index="01",
	),
	'bugbranch':mod( 'bugbranch',
		workshop_item='2517213262',
		exported_file_index="01",
	),
	'more_events':mod( 'more_events',
		workshop_item='727000451',
		exported_file_index="01",
	),
	'dynamic_political_events':mod( 'dynamic_political_events',
		workshop_item='1227620643',
		exported_file_index="01",
	),
	'plentiful_traditions':mod( 'plentiful_traditions',
		workshop_item='1311725711',
		exported_file_index="01",
	),
	'forgotten_queens':mod( 'forgotten_queens',
		workshop_item='1715190550',
		exported_file_index="01",
	),
	'leader_ethics':mod( 'leader_ethics',
		output_folder="leader_ethics_3",
		mod_path="C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod\\leader_ethics_3",
		exported_file_index="01",
	),
}
vanilla = mod_data['vanilla']
undercoat = mod( 'undercoat', vanilla=True, mod_path="C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod\\scripted_trigger_undercoat", can_write=False )

exclude_files = [
	'!!_order_ascension_perks.txt',
	'!!_evolved_placeholder_buildings.txt',
	'!!_evolved_placeholder_colony_types.txt',
	'!!_evolved_placeholder_deposits.txt',
	'!!00_order_districts.txt',
	'!!_evolved_placeholder_civics.txt',
	'mem_!!_evolved_placeholder_civics.txt',
	'NDO_!!_evolved_placeholder_origins.txt',
	'originsextended_!!evolved_placeholder_origins.txt',
	'pd_!!_evolved_placeholder_origins.txt',
	'!00_a_policies_organized.txt',
	'!!_evolved_placeholder_jobs.txt',
	'!!_evolved_placeholder_pd_traditions.txt',
	'000_i_matrioshka_brain_dummy.txt',
	'000_i_nicoll_dyson_beam_dummy.txt',
	'000_i_nidavellir_forge_dummy.txt',
	'000_i_stellar_systemcraft_dummy.txt',
	'000_o_birch_world_dummy.txt',
	'000_o_quasi_stellar_obliterator_dummy.txt',
	'000_z_giga_compat_dummy_megas.txt',
]

inline_script_unit_template = """inline_script = {{
	script = $unit$
	not_overwritten_trigger = "{}"
	{}source_mod = {}
	$additional_parameters$
}}
"""
placeholder_inline_script_template = "# $unit$$additional_parameters$"

script_unit_template = """	$unit$ = {{
		[[check_overwrite]not_overwritten_trigger = "{}"]
		{}[[enable_parameter_source_mod]source_mod = {}]
		[[additional_parameters]$additional_parameters$]
	}}
"""

scripted_effect_template = """{} = {{
{}}}"""
placeholder_scripted_effect_template = """{} = {{
	[[unit] ]
	[[check_overwrite] ]
	{}[[enable_parameter_source_mod] ]
	[[additional_parameters] ]
}}
"""
	# if = {{
	# 	limit = {{ always = no }}
	# 	set_global_flag = "$unit${}$enable_parameter_source_mod$$additional_parameters$"
	# }}

scripted_trigger_template = """{} = {{ [[AND]AND][[NAND]AND][[OR]OR][[NOR]OR] = {{
{}	hidden_trigger = {{
	[[AND]always = yes]
	[[NAND]always = yes]
	[[OR]always = no]
	[[NOR]always = no]
	}}
}} }}"""
placeholder_scripted_trigger_template = """{} = {{
	hidden_trigger = {{
		[[AND]always = yes]
		[[NAND]always = yes]
		[[OR]always = no]
		[[NOR]always = no]
		[[mode] ]
		[[unit] ]
		[[check_overwrite] ]
		{}[[enable_parameter_source_mod] ]
		[[additional_parameters] ]
	}}
}}
"""
		# if = {{
		# 	limit = {{ always = no }}
		# 	has_global_flag = "$unit$$mode${}$enable_parameter_source_mod$$additional_parameters$"
		# }}

master_inline_script_unit_template = """inline_script = {{
	script = foreach/{}/{}
	unit = $unit$
	additional_parameters = "$additional_parameters$"
}}
"""
master_scripted_effect_unit_template = """	{} = {{
		unit = $unit$
		check_overwrite = $check_overwrite|yes$
		{}enable_parameter_source_mod = $enable_parameter_source_mod|no$
		[[additional_parameters]additional_parameters = "$additional_parameters$"]
	}}
"""
master_scripted_trigger_unit_template = """	{} = {{
		unit = $unit$
		$mode$ = yes
		check_overwrite = $check_overwrite|yes$
		{}enable_parameter_source_mod = $enable_parameter_source_mod|no$
		[[additional_parameters]additional_parameters = "$additional_parameters$"]
	}}
"""
master_scripted_effect_template = """for_each_{} = {{
{}}}

"""
master_scripted_trigger_template = """for_each_{} = {{ $mode$ = {{
{}}} }}

"""

numbered_inline_script_unit_template = """inline_script = {{
	script = $unit$
	index = {}
	$additional_parameters$
}}
"""
numbered_script_unit_template = """	$unit$ = {{
		index = {}
		[[additional_parameters]$additional_parameters$]
	}}
"""



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

civic_potential_types = {
	"not = { has_ethic = ethic_gestalt_consciousness } not = { has_authority = auth_corporate }":'regular',
	"not = { has_ethic = ethic_gestalt_consciousness } nor = { has_authority = auth_corporate has_authority = auth_tec_patrocorporate has_authority = auth_tec_ai_corporate }":'regular',
	"nor = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial } not = { has_ethic = ethic_gestalt_consciousness }":'regular',
	"not = { has_ethic = ethic_gestalt_consciousness } nor = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial }":'regular',
	"has_authority = auth_hive_mind":'hive',
	"or = { has_authority = auth_hive_mind has_authority = auth_tec_hive_biological has_authority = auth_tec_hive_cybernetic }":'hive',
	"or = { has_authority = auth_hive_mind has_authority = auth_tec_hive_biological }":'biohive',
	"has_authority = auth_tec_hive_cybernetic":'cybernetic_hive',
	"or = { has_authority = auth_ancient_machine_intelligence has_authority = auth_machine_intelligence }":'machine',
	"has_authority = auth_machine_intelligence":'machine',
	"or = { has_authority = auth_corporate has_civic = civic_galactic_sovereign_megacorp }":'corporate',
	"or = { or = { has_authority = auth_corporate has_authority = auth_tec_patrocorporate has_authority = auth_tec_ai_corporate } has_civic = civic_galactic_sovereign_megacorp }":'corporate',
	"or = { or = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial } has_civic = civic_galactic_sovereign_megacorp }":'corporate',
	"or = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial }":'corporate',
}

defined_triggers = {
	'export_modifier':{
	"":'no',
	},
	'export_trigger':{
	"":'always',
	"always = no":'never',

	"""exists = $country$
	""":'exists_country',
	"""exists = $country$
	nor = {  }""":'exists_country',
	"""exists = $planet$
	""":'exists_planet',
	"""exists = $species$
	exists = $planet$
	""":'exists_species_exists_planet',
	"""exists = $country$
	exists = $species$
	""":'exists_country_exists_species',
	"""exists = $faction$
	""":'exists_faction',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $country$
	exists = $starbase$
	""":'consider_ai_exists_country_exists_starbase',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $country$
	exists = $starbase$
	exists = owner
	""":'consider_ai_exists_country_exists_starbase_exists_owner',
	"""exists = $country$
	exists = $leader$
	""":'exists_country_exists_leader',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	""":'consider_ai_exists_planet',

	"""exists = $country$
	always = no""":'exists_country_never',
	"""exists = $species$
	exists = $planet$
	always = no""":'exists_species_exists_planet_never',
	"""exists = $country$
	exists = $species$
	always = no""":'exists_country_exits_species_never',

	"""exists = $country$
	has_overlord_dlc = yes""":'exists_country_has_overlord_dlc',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_overlord_dlc = yes""":'exists_planet_has_overlord_dlc',
	"""exists = $country$
	host_has_dlc = Federations""":'exists_country_has_federation_dlc',

	"""exists = $country$
	not = { is_machine_empire = yes }""":'exists_country_not_machine',
	"""exists = $country$
	is_machine_empire = yes""":'exists_country_is_machine',
	"""exists = $country$
	is_hive_empire = yes""":'exists_country_is_hive',
	"""exists = $country$
	is_gestalt = yes""":'exists_country_is_gestalt',
	"""exists = $country$
	or = {
		is_machine_empire = yes
		is_hive_empire = yes
	}""":'exists_country_is_gestalt',

	"""exists = $country$
	nor = { exists_country_is_gestalt = { country = $country$ } }""":'exists_country_not_gestalt',
	"""exists = $country$
	nor = { exists_country_is_machine = { country = $country$ } exists_country_is_hive = { country = $country$ } }""":'exists_country_not_gestalt',
	"""exists = $country$
	nor = { exists_country_is_hive = { country = $country$ } exists_country_is_machine = { country = $country$ } }""":'exists_country_not_gestalt',
	"""exists = $country$
	nor = { exists_country_is_machine = { country = $country$ } }""":'exists_country_not_machine',


	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_upgraded_capital = yes""":'exists_planet_has_upgraded_capital',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_major_upgraded_capital = yes""":'exists_planet_has_major_upgraded_capital',

	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_branch_office = yes
	branch_office_owner = { is_criminal_syndicate = no }""":'consider_ai_exists_planet_has_non_criminal_branch_owner',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_branch_office = yes
	branch_office_owner = {
		$consider_ai|never$ = no
		is_criminal_syndicate = no
	}""":'consider_ai_exists_planet_has_non_criminal_player_branch_owner',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_branch_office = yes
	branch_office_owner = { is_criminal_syndicate = yes }""":'consider_ai_exists_planet_has_criminal_branch_owner',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $planet$
	has_branch_office = yes
	branch_office_owner = {
		$consider_ai|never$ = no
		is_criminal_syndicate = yes
	}""":'consider_ai_exists_planet_has_criminal_player_branch_owner',


	"""exists = $planet$
	exists = owner
	nor = {
		uses_district_set = city_world
		uses_district_set = ring_world
		uses_district_set = habitat
	}
	is_special_colony_type = no""":'rst_standard_colony_type_trigger',
	"""exists = $planet$
	uses_district_set = habitat""":'rst_habitat_colony_type_trigger',
	"""exists = $planet$
	uses_district_set = ring_world""":'rst_ring_colony_type_trigger',
	"""exists = $planet$
	uses_district_set = city_world""":'rst_ecu_colony_type_trigger',

	"""exists = $country$
	has_technology = tech_ascension_theory""":'rst_standard_ambition_trigger',

	"host_has_dlc = Utopia":'has_utopia',
	"host_has_dlc = \"Synthetic Dawn Story Pack\"":'has_synthethic_dawn',
	"host_has_dlc = Megacorp":'has_megacorp_dlc', # not in vanilla
	"host_has_dlc = Apocalypse":'has_apocalypse', # not in vanilla
	"host_has_dlc = \"Necroids Species Pack\"":'has_necroids',
	"host_has_dlc = Federations":'has_federations_dlc',
	"host_has_dlc = \"Plantoids Species Pack\"":'has_plantoids',
	"host_has_dlc = \"Humanoids Species Pack\"":'has_humanoids',
	"host_has_dlc = \"Lithoids Species Pack\"":'has_lithoids',

	"""exists = $target$
	exists = $observer$
	has_policy_flag = enlightenment_allowed
	custom_tooltip = {
		fail_text = cannot_enlighten_fanatic_xenophobe
		$target$ = {
			exists = owner
			owner = {
				not = { has_ethic = ethic_fanatic_xenophobe }
			}
		}
	}
	nor = {
		has_valid_civic = civic_fanatic_purifiers
		has_valid_civic = civic_hive_devouring_swarm
		has_valid_civic = civic_machine_terminator
	}""":'rst_enlightenment_allowed_trigger',

	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $country$
	exists = $starbase$
	is_orbital_ring = yes
	""":'consider_ai_exists_country_exists_starbase_is_orbital_ring',
	"""[[consider_ai]hidden_trigger = { if = { limit = { always = no } has_global_flag = $consider_ai$ } }]
	exists = $country$
	exists = $starbase$
	is_orbital_ring = no
	""":'consider_ai_exists_country_exists_starbase_not_orbital_ring',

	"""exists = $country$
	exists = $species$
	exists = $country$
	$country$ = {
		or = {
			is_machine_empire = yes
			has_technology = tech_droid_workers
		}
		not = { has_policy_flag = ai_outlawed }
	}""":'rst_droid_trait_trigger',
	"""exists = $country$
	exists = $species$
	exists = $country$
	$country$ = {
		or = {
			is_machine_empire = yes
			has_technology = tech_synthetic_leaders
		}
		not = { has_policy_flag = ai_outlawed }
	}""":'rst_synthetic_leader_species_trait_trigger',
	"""exists = $country$
	exists = $species$
	exists = $country$
	$country$ = { has_technology = tech_lithoid_transgenesis }""":'rst_lithoid_transgenic_trait_trigger',
	"""exists = $country$
	exists = $species$
	exists = $country$
	$country$ = { has_technology = tech_plantoid_transgenesis }""":'rst_plantoid_transgenic_trait_trigger',
	"""exists = $country$
	exists = $species$
	exists = $country$
	$country$ = { has_origin = origin_overtuned }""":'rst_overtuned_trait_trigger',

	"""exists = $country$
	exists = $leader$
	not = {
		$country$ = { is_machine_empire = yes }
	}""":'exists_country_exists_leader_not_machine',
	"""exists = $country$
	exists = $leader$
	not = {
		$country$ = { is_gestalt = yes }
	}""":'exists_country_exists_leader_not_gestalt',
	"""exists = $country$
	exists = $leader$
	$country$ = { is_machine_empire = yes }""":'exists_country_exists_leader_machine',
	"""exists = $country$
	exists = $leader$
	not = { leader_class = ruler }
	not = {
		$country$ = { is_gestalt = yes }
	}""":'rst_standard_ruler_trait_trigger',
	}
}

def match(string1,string2):
	if string1 is None:
		return string2 is None
	else:
		m = string1.lower() == string2.lower()
		return m

def to_yesno(bool):
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
	def __init__(self,name,comparison=None,value=None,subelements=None,parent=None,filename=None):
		self.name = name
		self.comparison = comparison
		self.value = value
		self.subelements = subelements
		self.parent = parent
		self.metadata = {}
		self.filename = filename
	
	def __str__(self) -> str:
		return self.getString()
	
	def __repr__(self) -> str:
		return self.name
	
	def parse(self,tokens,local_variables={}):
		while len(tokens)>0:
			nextToken = tokens.pop(0)
			if nextToken.startswith('@'):
				if nextToken in local_variables:
					nextToken = local_variables[nextToken]
			if nextToken == "\"":
				nextToken = getQuotedString(tokens)
			if nextToken in ("=","<",">"):
				self.comparison.append(nextToken)
			elif nextToken == "{":
				self.subelements = parseCW(tokens,parent=self,filename=self.filename,local_variables=local_variables)
				return self
			elif nextToken == "hsv":
				self.value = "hsv"
			else:
				self.value = nextToken
				if self.name.startswith('@'):
					local_variables[self.name]=nextToken
				return self

	def hasAttribute(self,key):
		if not self.hasSubelements():
			return False
		for element in self.subelements:
			if match( element.name, key ):
				return True
		return False

	def getElement(self,key):
		if not self.hasSubelements():
			return CWElement("",parent=self)
		for element in self.subelements:
			if match( element.name, key ):
				return element
		return CWElement("",parent=self)

	def getElements(self,key):
		for element in self.subelements:
			if match( element.name, key ):
				yield element

	def getValue(self,key,default="no"):
		if not self.hasSubelements():
			return default
		for element in self.subelements:
			if match( element.name, key ):
				return element.value
		return default

	def getValues(self,key):
		for element in self.subelements:
			if match( element.name, key ):
				yield element.value

	def getValueBoolean(self,key,default=False):
		for element in self.subelements:
			if match( element.name, key ):
				return element.value != "no"
		return default

	def getArrayContents(self,key):
		for element in self.subelements:
			if match( element.name, key ):
				for entry in element.subelements:
					yield entry.name

	def getArrayContentsFirst(self,key,default="no",log_if_empty=None,log_if_multiple=True):
		for element in self.subelements:
			if match( element.name, key ):
				if log_if_multiple and len(element.subelements) > 1:
					log("element {} array {} contains multiple elements".format(self.name,key))
				for entry in element.subelements:
					return entry.name
		if log_if_empty is not None:
			log(log_if_empty)
		return default

	def getArrayContentsElements(self,key):
		for element in self.subelements:
			if match( element.name, key ):
				for entry in element.subelements:
					yield entry


	def hasSubelements(self):
		if self.subelements is not None:
			return True
		else:
			return False

	def expand(self):
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

	def getString(self):
		if self.name is not None:
			words = [ quoteIfNecessary(self.name) ]
		else:
			words = [ 'NULL' ]
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
				bracketContentsString = bracketContentsString.replace("\n","\n\t")
				subelementString = "{{\n\t{}\n}}".format(bracketContentsString)
			else:
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				bracketContentsString = " ".join(bracketContents)
				subelementString = "{{ {} }}".format(bracketContentsString)
			words.append(subelementString)
		return(" ".join(words))

	def getContentsString( self, include_brackets=True ):
		words = []
		if self.subelements is not None:
			if self.expand():
				bracketContents = []
				for e in self.subelements:
					bracketContents.append(e.getString())
				subelementString = "\n".join(bracketContents)
				subelementString = subelementString.replace("\n","\n\t")
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

	def convertGovernmentTrigger(self,trigger=None):
		# print("converting element '{}'".format(self.getString(),)) 
		if match( self.name, 'text' ):
			return ""
		elif match( self.name, 'value' ):
			output = CWElement(trigger,['='],self.value)
		elif match( self.name, 'always' ):
			output = CWElement('always',['='],self.value)
		elif self.name in government_triggers:
			output = CWElement('AND',['='],subelements=[])
			for element in self.subelements:
				if not match( element.name, 'text' ):
					output.subelements.append( element.convertGovernmentTrigger( government_triggers[self.name] ) )
			if len( output.subelements ) == 1:
				output = output.subelements[0]
		else:
			output = CWElement(self.name,['='],subelements=[])
			for element in self.subelements:
				if not match( element.name, 'text' ):
					output.subelements.append( element.convertGovernmentTrigger( trigger ) )
		if self.hasAttribute('text'):
			text_element = CWElement('text',['='],self.getValue('text'))
			if output.name == 'AND':
				return CWElement('custom_tooltip',['='],subelements=[text_element]+output.subelements)
			else:
				return CWElement('custom_tooltip',['='],subelements=[text_element,output])
		else:
			return output

	def getCaller(self):
		return self.metadata['caller']

	def getRoot(self):
		if self.parent is None:
			return self
		else:
			return self.parent.getRoot()

	def replaceInlines(self,mod:mod):
		found_inlines = True
		while found_inlines:
			found_inlines = False
			if self.hasSubelements():
				inline_contents = []
				for element in self.subelements:
					if match( element.name, 'inline_script' ):
						found_inlines = True
						# print("replacing inline script '{}'".format(element.getString()))
						if element.hasSubelements():
							script = mod.lookupInline( element.getValue('script') )
							if script is None:
								script = []
							else:
								file = open(script,"r")
								script = file.read()
								file.close()
								for param in element.subelements:
									if param.value is None:
										val = ''
									else:
										val = param.value
									script = script.replace( '${}$'.format(param.name), val )
								script = stringToCW(script,mod,parent=self)
						else:
							script = mod.lookupInline( element.value )
							if script is None:
								script = []
							else:
								script = fileToCW(script,mod,parent=self)
						# print("replacing with script "+str(script))
						inline_contents = inline_contents + script
						self.subelements.remove(element)
					else:
						element.replaceInlines(mod)
				self.subelements = self.subelements+inline_contents

	def getArrayTriggers(self,block,trigger,mode='OR'):
		lines = []
		for item in self.getArrayContents(block):
			lines.append( '{} = {}'.format( trigger, item ) )
		if mode == 'OR':
			if len(lines) == 0:
				return 'no'
			elif len(lines) == 1:
				return lines[0]
			else:
				lines_block = ' '.join(lines)
				return 'OR = {{ {} }}'.format(lines_block)
		if mode == 'NOR':
			if len(lines) == 0:
				return 'no'
			elif len(lines) == 1:
				return 'NOT = {{ {} }}'.format(lines[0])
			else:
				lines_block = ' '.join(lines)
				return 'NOR = {{ {} }}'.format(lines_block)
		if mode == 'AND':
			if len(lines) == 0:
				return 'no'
			elif len(lines) == 1:
				return lines[0]
			else:
				lines_block = ' '.join(lines)
				return 'AND = {{ {} }}'.format(lines_block)
		if mode == 'NAND':
			if len(lines) == 0:
				return 'no'
			elif len(lines) == 1:
				return 'NOT = {{ {} }}'.format(lines[0])
			else:
				lines_block = ' '.join(lines)
				return 'NAND = {{ {} }}'.format(lines_block)


def parseCW(tokens,parent=None,filename=None,local_variables={}):
	elements = []
	while len(tokens)>0:
		nextToken = tokens.pop(0)
		if nextToken == "":
			pass
		else:
			if nextToken == "\"":
				nextToken = getQuotedString(tokens)
			if nextToken in ("=","<",">"):
				lastElement.comparison = [nextToken]
				lastElement.parse(tokens,local_variables=local_variables)
			elif nextToken == "}":
				return elements
			elif nextToken == "{":
				e = CWElement(None,parent=parent,filename=filename)
				elements.append(e)
				e.subelements = parseCW(tokens,e,filename=filename,local_variables=local_variables)
			else:
				elements.append(CWElement(nextToken,parent=parent,filename=filename))
			lastElement = elements[-1]
	return elements
			

def stringToCW(string,mod=None,filename=None,parent=None)->list[CWElement]:
	"""Returns a list of CWElements"""
	# print("reformatting parser commands")
	string = re.sub(r"#(RST:[^ \n]*)",r"\|\($1\)\|",string) # processor commands
	# print("removing comments")
	string = re.sub(r"#.*\n",r" ",string) # remove comments
	# print("separating special characters")
	string = string.replace("="," = ") # put spaces around special characters
	string = string.replace("<"," < ")
	string = string.replace(">"," > ")
	string = string.replace("{"," { ")
	string = string.replace("}"," } ")
	string = string.replace("\""," \" ")
	string = string.replace("\\ \""," \" ")
	# print("generating tokens")
	tokenList = re.split("\s+",string)
	# print("executing parser commands")
	i = 0
	while i < len(tokenList):
		token = tokenList[i]
		if token == '|(RST:skip)|':
			while token != '|(RST:/skip)|' and i < len(tokenList):
				token = tokenList.pop(i)
		elif token.startswith('|(RST:'):
			token = tokenList.pop(i)
		else:
			i += 1
	# print("parsing tokens")
	cw = parseCW(tokenList,filename=filename,parent=parent)
	# print("substituting inline scripts")
	if mod is not None:
		for element in cw:
			element.replaceInlines(mod)
	return cw


def fileToCW(path,mod=None,parent=None)->list[CWElement]:
	# print("opening file")
	file = open(path,"r")
	try:
		fileContents = file.read()
	except:
		fileContents = ""
	filename = os.path.basename(path)
	# print("generating CW objects")
	cw = stringToCW(fileContents,mod,filename=filename,parent=parent)
	file.close()
	return cw

def CWToString(elements:list[CWElement])->str:
	cwStrings = []
	for e in elements:
		cwStrings.append(e.getString())
	return "\n\n".join(cwStrings)

class CWDatabase():
	def __init__(
		self,
		key,
		script_params,
		primary_key,
		read_files=None,
		get_contents=None,
		get_subelements=None,
		filter=lambda x:True,
		input_folder=None,
		file_suffix = '.txt',
		singular=None,
		inline_script_path=None,
		additional_templates=[],
		subunits=[],
		can_write=True,
		top_level=True,
		array_key=None,
		subelement_name=None,
		debug=False,
		reverse=False,
		overwrite=False,
		on_process=None,
	):
		self.key = key
		self.script_params = script_params
		self.primary_key_name = primary_key
		self.primary_key = script_params[primary_key]['val']
		self.filter = filter
		if input_folder is None:
			self.input_folder = os.path.join("common",key)
		else:
			self.input_folder = input_folder
		self.file_suffix = file_suffix
		if singular is None:
			self.singular = key[:-1]
		else:
			self.singular = singular
		if inline_script_path is None:
			self.inline_script_path = [self.singular]
		else:
			self.inline_script_path = inline_script_path
		self.additional_templates = additional_templates
		self.subunits = subunits
		self.contents = {}
		self.master_inline_script_units = []
		self.master_scripted_effect_units = []
		self.master_scripted_trigger_units = []
		if read_files is not None:
			self.readFiles = MethodType(read_files,self)
		if get_contents is not None:
			self.getContents = MethodType(get_contents,self)
		if get_subelements is not None:
			self.getSubelements = MethodType(get_subelements,self)
		elif array_key is not None:
			self.getSubelements = self.forArrayLookup
		elif subelement_name is not None:
			self.getSubelements = self.getSubelementsByName
		self.can_write = can_write
		self.overwrite = overwrite
		self.top_level = top_level
		self.array_key = array_key
		self.subelement_name = subelement_name
		self.vanilla_inline_script_path = None
		self.reverse = reverse
		self.debug = debug
		if on_process is not None:
			self.onProcess = MethodType(on_process,self)
		for template_key, encoding in self.additional_templates:
			output_path = os.path.join( 'Autogenerated', template_key )+'.txt'
			output_file = open(output_path,'w',encoding=encoding)
			output_file.write( "" )
			output_file.close()


	def readFiles(self,mod:mod):
		print("reading files for mod {} database {}".format(mod.key,self.key))
		path = os.path.join(mod.mod_path,self.input_folder)
		if os.path.exists(path):
			CW_list = []
			for file in os.listdir(path=path):
				# print(file)
				if file.endswith(self.file_suffix) and not file in exclude_files:
					undercoat_filepath = os.path.join( undercoat.mod_path, self.input_folder, file )
					if mod.vanilla and os.path.exists( undercoat_filepath ):
						filepath = undercoat_filepath
					else:
						filepath = os.path.join(path,file)
					# print(filepath)
					CW_list = CW_list + fileToCW( filepath, mod )
			for element in CW_list:
				element.metadata['written_flag'] = False
				if self.debug:
					log('> '+str(element))
			if self.reverse:
				CW_list.reverse()
			self.contents[mod.key] = CW_list

	def getContents(self,mod:mod):
		if mod.key in self.contents:
			for element in self.contents[mod.key]:
				if element.hasSubelements() and self.filter(element):
					yield element

	def lookup(self,key,mod:mod,attribute=None,default=None):
		if attribute is None:
			attribute = self.primary_key
		else:
			attribute = self.script_params[attribute]['val']
		for mod_key in mod.inheritance_list:
			for element in self.getContents(mod_data[mod_key]):
				if match( attribute(element,mod,self), key ):
					return element
		if default is not None:
			return CWElement(default)

	def scriptLines(self,element:CWElement,mod:mod,spacing,bracket):
		lines = ""
		for param in self.script_params:
			if self.debug:
				print(param)
			param_data = self.script_params[param]
			# print("element {} parameter '{}'".format(self.primary_key(element,mod,self),param))
			if element is None:
				value = 'no'
			else:
				value = quoteIfNecessary( param_data['val'](element,mod,self) )
			if 'foreign_key' in param_data:
				foreign_db = databases[ param_data['foreign_key'] ]
				linked_element = foreign_db.lookup( value, mod )
				if linked_element is None:
					log("could not find data {} for {} {}".format(value,self.key,self.primary_key(element,mod,self)))
				lines = lines+foreign_db.scriptLines( linked_element, mod, spacing, bracket )
			else:
				param_line = "{} = {}".format( param, value )
				if bracket:
					param_line = "[[enable_parameter_{}]{}]".format(param,param_line)
				lines = lines+param_line+spacing
		return lines

	def parameterLines(self):
		parameter_list = []
		for param_key in self.script_params:
			param = self.script_params[param_key]
			if 'foreign_key' in param:
				for foreign_param_key in databases[param['foreign_key']].script_params:
					parameter_list.append(foreign_param_key)
			else:
				parameter_list.append(param_key)
		lines = ""
		for param_key in parameter_list:
			if param_key == self.primary_key_name:
				lines = lines + "enable_parameter_{} = $enable_parameter_{}|yes$\n\t\t".format(param_key,param_key)
			else:
				lines = lines + "enable_parameter_{} = $enable_parameter_{}|no$\n\t\t".format(param_key,param_key)
		return lines

	def parameterSoakLine(self):
		line = ""
		for param_key in self.script_params:
			param_data = self.script_params[param_key]
			if 'foreign_key' in param_data:
				line = line + databases[param_data['foreign_key']].parameterSoakLine()
			else:
				line = line + "[[enable_parameter_{}] ]\n\t".format(param_key)
		return line

	def overwrites(self,element_key,mod:mod):
		for mod_key in mod.inheritance_list[1:]:
			if mod_key in self.contents:
				for item in self.contents[mod_key]:
					if match( self.primary_key(item,mod_data[mod_key],self), element_key ):
						return item

	def parameterValues(self,element:CWElement,mod:mod):
		for param in self.script_params:
			param_data = self.script_params[param]
			value = quoteIfNecessary( param_data['val'](element,mod,self) )
			if 'foreign_key' in param_data:
				foreign_db = databases[ param_data['foreign_key'] ]
				linked_element = foreign_db.lookup( value, mod )
				if linked_element is None:
					print("could not find data for {} {}".format(self.key,value))
					log("could not find data for {} {}".format(self.key,value))
					for param in foreign_db.script_params:
						yield (param,'no')
				else:
					for param_val in foreign_db.parameterValues(linked_element,mod):
						yield param_val
			else:
				yield (param,value)

	def processCW(
		self,
		mod:mod,
		data_source,
		output_key:str,
		caller_overwrites = False,
		caller_not_overwritten_check = None
	):
		
		print("processing mod {} database {}".format(mod.key,self.key))
		inline_script_units = []
		script_units = []
		additional_template_text = {}
		for template, encoding in self.additional_templates:
			additional_template_text[template]=[]

		found_elements = False
		overwrites = False

		for element in data_source:
			element.metadata['subelement_index'] = 0
			if element.parent is not None and 'sublement_index' in element.parent.metadata:
				element.parent.metadata['subelement_index'] +=1
			if self.filter(element):
				element.metadata['written_flag'] = True
				element_key = self.primary_key(element,mod,self)
				skip = False
				overwrite_checks = []
				overwrites = None
				for mod_key in mod_data:
					if mod_key != mod.key and mod_key in self.contents:
						for compare_element in self.contents[mod_key]:
							if match( self.primary_key(compare_element,mod_data[mod_key],self), self.primary_key(element,mod,self) ):
								ow = overwrite_precedence( element, mod, compare_element, mod_data[mod_key] )
								if not ow:
									overwrite_checks.append( "rst_has_{} = no".format(mod_key) )
								elif mod_key in mod.inheritance_list:
									overwrites = compare_element
				if overwrites is not None:
					log("mod {} overwrites {} {}".format(mod.key,self.singular,element_key))
				if not skip:
					found_elements = True
					if caller_not_overwritten_check is not None:
						not_overwritten_check = caller_not_overwritten_check
					elif len( overwrite_checks ) == 0:
						not_overwritten_check = 'always = yes'
					else:
						not_overwritten_check = ' '.join( overwrite_checks )
					inline_script_units.append(
						inline_script_unit_template.format(
							not_overwritten_check,
							self.scriptLines(element,mod,"\n\t",bracket=False),
							mod.key,
						)
					)
					script_units.append(
						script_unit_template.format(
							not_overwritten_check,
							self.scriptLines(element,mod,"\n\t\t",bracket=True),
							mod.key,
						)
					)

					for template_key, encoding in self.additional_templates:
						unit = templates[template_key]
						for value in self.parameterValues(element,mod):
							unit = unit.replace( '<{}>'.format(value[0]), value[1] )
						unit = unit.replace( '<mod>', mod.key )
						additional_template_text[template_key].append(unit)

				for subunit_key in self.subunits:
					subunit_db = databases[subunit_key]
					subunit_db.processCW(
						mod,
						subunit_db.getSubelements(mod,element),
						element_key,
						overwrites is not None,
						not_overwritten_check
					)

				
		if self.can_write and found_elements:

			inline_script = "".join(inline_script_units)
			inline_script_path = mod.inline_script_path
			for folder in self.inline_script_path:
				inline_script_path = generate_joined_folder(inline_script_path,folder)
			if mod.vanilla:
				self.vanilla_inline_script_path = inline_script_path
			inline_script_path = os.path.join( inline_script_path, output_key )+'.txt'
			inline_script_file = open(inline_script_path,'w')
			inline_script_file.write( inline_script )
			inline_script_file.close()

			extended_output_key = "for_each_{}_{}".format(self.singular,output_key)

			scripted_effect = scripted_effect_template.format( extended_output_key, "".join(script_units) )
			scripted_effect_path = os.path.join( mod.scripted_effect_path, extended_output_key )+'.txt'
			scripted_effect_file = open(scripted_effect_path,'w')
			scripted_effect_file.write( scripted_effect )
			scripted_effect_file.close()

			scripted_trigger = scripted_trigger_template.format( extended_output_key, "".join(script_units) )
			scripted_trigger_path = os.path.join( mod.scripted_trigger_path, extended_output_key )+'.txt'
			scripted_trigger_file = open(scripted_trigger_path,'w')
			scripted_trigger_file.write( scripted_trigger )
			scripted_trigger_file.close()

			for template_key, encoding in self.additional_templates:
				output_string = "".join( additional_template_text[template_key] )
				output_path = os.path.join( 'Autogenerated', template_key )+'.txt'
				output_file = open(output_path,'a',encoding=encoding)
				output_file.write( output_string )
				output_file.close()				

			if not mod.vanilla and not caller_overwrites:
				vanilla_inline_script_path = self.vanilla_inline_script_path
				vanilla_inline_script_path = os.path.join( vanilla_inline_script_path, output_key )+'.txt'
				vanilla_inline_script_file = open( vanilla_inline_script_path, 'w' )
				vanilla_inline_script_file.write( placeholder_inline_script_template )
				vanilla_inline_script_file.close()

				placeholder_scripted_effect = placeholder_scripted_effect_template.format( extended_output_key, self.parameterSoakLine() )
				vanilla_scripted_effect_file = open( placeholder_scripted_effects_path,'a' )
				vanilla_scripted_effect_file.write( placeholder_scripted_effect )
				vanilla_scripted_effect_file.close()

				placeholder_scripted_trigger = placeholder_scripted_trigger_template.format( extended_output_key, self.parameterSoakLine() )
				vanilla_scripted_trigger_file = open( placeholder_scripted_triggers_path, 'a' )
				vanilla_scripted_trigger_file.write( placeholder_scripted_trigger )
				vanilla_scripted_trigger_file.close()

			if not caller_overwrites:
				master_inline_script_unit = master_inline_script_unit_template.format( '/'.join(self.inline_script_path), output_key )
				self.master_inline_script_units.append(master_inline_script_unit)
				master_scripted_effect_unit = master_scripted_effect_unit_template.format( extended_output_key, self.parameterLines() )
				master_scripted_trigger_unit = master_scripted_trigger_unit_template.format( extended_output_key, self.parameterLines() )
				self.master_scripted_effect_units.append(master_scripted_effect_unit)
				self.master_scripted_trigger_units.append(master_scripted_trigger_unit)


	def checkWritten(self,mod):
		if self.can_write:
			for element in self.getContents(mod):
				if not element.metadata['written_flag']:
					log( "{} {} in mod {} was not written".format( self.key, self.primary_key(element,mod,self), mod.key ) )

	def forArrayLookup(self,mod:mod,element:CWElement):
		for i in element.getArrayContentsElements(self.array_key):
			found_element = self.lookup(i.name,mod)
			if found_element is not None:
				found_element.metadata['caller'] = element
				yield found_element
			else:
				yield i

	def getSubelementsByName(self,mod:mod,element:CWElement):
		for i in element.getElements(self.subelement_name):
			yield i

class numberedEntryGenerator():
	def __init__( self, i, additional_templates=[] ):
		self.count = i
		self.additional_templates = additional_templates
		self.top_level = True
		self.can_write = False

	def readFiles(self,mod:mod):
		pass

	def getContents(self,mod:mod):
		pass

	def processCW(
		self,
		mod:mod,
		data_source,
		output_key:str,
	):
		print("processing mod {} numbers {}".format(mod.key,self.count))
		inline_script_units = []
		script_units = []
		additional_template_text = {}
		for template, encoding in self.additional_templates:
			additional_template_text[template]=[]

		if mod.vanilla:
			for i in range(self.count):
				inline_script_units.append(
					numbered_inline_script_unit_template.format( str(i) )
				)
				script_units.append(
					numbered_script_unit_template.format( str(i) )
				)

				for template_key, encoding in self.additional_templates:
					unit = templates[template_key]
					unit = unit.replace( '<N>', str(i) )
					additional_template_text[template_key].append(unit)
				
			inline_script = "".join(inline_script_units)
			inline_script_path = mod.inline_script_path
			inline_script_path = generate_joined_folder(inline_script_path,'number')
			inline_script_path = os.path.join( inline_script_path, str(self.count) )+'.txt'
			inline_script_file = open(inline_script_path,'w')
			inline_script_file.write( inline_script )
			inline_script_file.close()

			extended_output_key = "for_each_number_{}".format(str(self.count))

			scripted_effect = scripted_effect_template.format( extended_output_key, "".join(script_units) )
			scripted_effect_path = os.path.join( mod.scripted_effect_path, extended_output_key )+'.txt'
			scripted_effect_file = open(scripted_effect_path,'w')
			scripted_effect_file.write( scripted_effect )
			scripted_effect_file.close()

			scripted_trigger = scripted_trigger_template.format( extended_output_key, "".join(script_units) )
			scripted_trigger_path = os.path.join( mod.scripted_trigger_path, extended_output_key )+'.txt'
			scripted_trigger_file = open(scripted_trigger_path,'w')
			scripted_trigger_file.write( scripted_trigger )
			scripted_trigger_file.close()

			for template_key, encoding in self.additional_templates:
				output_string = "".join( additional_template_text[template_key] )
				output_path = os.path.join( 'Autogenerated', template_key )+'.txt'
				output_file = open(output_path,'w',encoding=encoding)
				output_file.write( output_string )
				output_file.close()				

	def checkWritten(self,mod):
		pass

def overwrite_precedence( element_1:CWElement, mod_1:mod, element_2:CWElement, mod_2:mod ):
	if element_1.filename > element_2.filename:
		return True
	if element_2.filename > element_1.filename:
		return False
	if mod_2.key in mod_1.inheritance_list:
		return True
	if mod_1.key in mod_2.inheritance_list:
		return False
	log( "overwrite depends on mod order for file {} mods {}, {}".format( element_1.filename, mod_1.key, mod_2.key ) )
	return True

def getTechBackground(tech:CWElement,mod,db):
	if tech.getValueBoolean("is_insight"):
		return "insight"
	elif tech.getValueBoolean("is_dangerous"):
		return "dangerous"
	elif tech.getValueBoolean("is_rare"):
		return "rare"
	else:
		return tech.getValue("area")

def getSign(trait:CWElement,mod,db):
	cost = trait.getValue("cost",default="0")
	if cost is None:
		cost = trait.getElement("cost").getValue("base",default="0")
	cost = float(cost)
	if cost > 0:
		return "1"
	elif cost == 0:
		return "0"
	else:
		return "-1"

def generateBlockString(CWElement:CWElement,mod:mod,db:CWDatabase,input_key,output_key=None,root_scope=None,from_scope=None,output_mode='export_trigger',government=False,convert_cw=None,ai_check=False):
	str=""
	if output_key is None:
		if output_mode == 'export_trigger':
			output_key = "{}_{{}}_{}_trigger".format(db.singular,input_key)
		else:
			output_key = "{}_{{}}_{}".format(db.singular,input_key)
	if convert_cw is None:
		if output_mode == 'export_modifier':
			convert_cw = cleanModifierBlock
		else:
			convert_cw = lambda x,y:x
	cw_list = []
	for block in CWElement.getElements(input_key):
		if government:
			cw_list = cw_list + block.convertGovernmentTrigger().subelements
		else:
			cw_list = cw_list + deepcopy(block.subelements)
	convert_cw(cw_list,CWElement)
	str_list = []
	for element in cw_list:
		str_list.append( element.getString() )
	str = "\n".join(str_list)
	str = str.lower()
	if root_scope is not None:
		root_scope = '${}$'.format(root_scope)
		str = str.replace('root',root_scope)
	if from_scope is not None:
		from_scope = '${}$'.format(from_scope)
		str = str.replace('from',from_scope)
	for dlc in dlc_list:
		dlc_check = 'host_has_dlc = '+quoteIfNecessary(dlc)
		str = str.replace( dlc_check.lower(), dlc_check )
	if output_mode == 'flatten':
		return str.replace('\n',' ').replace('\t','')
	output_key = output_key.format( db.primary_key(CWElement,mod,db) )
	if ai_check:
		str = str.replace('is_ai','$consider_ai|never$')
	# str = str.replace('\n','\n\t')
	# if not 'triggers_written' in CWElement.metadata:
	# 	CWElement.metadata['triggers_written'] = []
	# if not input_key in CWElement.metadata['triggers_written']:
	if root_scope is not None:
		str = "exists = {}\n{}".format(root_scope,str)
	if from_scope is not None:
		str = "exists = {}\n{}".format(from_scope,str)
	if ai_check:
		str = "[[consider_ai]hidden_trigger = {{ if = {{ limit = {{ always = no }} has_global_flag = $consider_ai$ }} }}]\n{}".format(str)
	breakdown = str.split(' ')
	if len(breakdown) == 3 and breakdown[2] == 'yes':
		return breakdown[0]
	str = str.replace('\n','\n\t')
	if output_mode in defined_triggers and str in defined_triggers[output_mode]:
		return defined_triggers[output_mode][str]
	if not 'exported_{}'.format(output_key) in CWElement.metadata:
		CWElement.metadata['exported_{}'.format(output_key)]=True
		if output_mode == 'export_trigger':
			output_file = mod.exported_triggers_file
		if output_mode == 'export_modifier':
			output_file = mod.exported_modifiers_file
			exported_modifier_names_file = open(exported_modifier_names_path,'a')
			exported_modifier_names_file.write( " {}: \"${}$\"\n".format(output_key,db.primary_key(CWElement,mod,db)) )
			exported_modifier_names_file.close()
		file = open(output_file,'a')
		file.write( "{} = {{\n\t{}\n}}\n".format(output_key,str) )
		file.close()
		# CWElement.metadata['triggers_written'].append(input_key)
	return output_key

def getYesNoTrigger(CWElement:CWElement,mod:mod,db:CWDatabase,input_key,output_key=None,root_scope=None,from_scope=None,default="never"):
	if CWElement.hasAttribute(input_key):
		subelement = CWElement.getElement(input_key)
		if subelement.hasSubelements():
			return generateBlockString(CWElement,mod,db,input_key,output_key,root_scope,from_scope)
		if match( subelement.value, 'yes' ):
			return "always"
		if match( subelement.value, 'no' ):
			return "never"
	return default

def getTraitType(trait:CWElement,mod,db):
	if trait.getArrayContentsFirst('allowed_archetypes',log_if_multiple=False) in ['ROBOT','MACHINE']:
		return 'robotic'
	if match( trait.getValue('sapient',default='yes'), 'no' ):
		return 'presapient'
	potential_add_trigger = trait.getElement('species_potential_add')
	if match( trait.getValue('advanced_trait'), 'yes' ):
		if match( potential_add_trigger.getValue('always',default='yes'), 'no' ):
			return 'no_modification'
		return 'genetic_ascension'
	if trait.hasAttribute('species_potential_add'):
		if match( potential_add_trigger.getValue('always',default='yes'), 'no' ):
			return 'no_modification'
		if match( potential_add_trigger.getElement('from').getValue('has_origin'), 'origin_overtuned' ):
			return 'overtuned'
		if match( potential_add_trigger.getValue('can_add_cybernetic_traits'), 'yes' ):
			return 'cybernetic'
	if match( trait.getValue('initial'), 'no' ):
		return 'special'
	return 'generic'

def getLeaderClass(trait:CWElement,mod,db):
	if trait.getElement("leader_trait").hasSubelements():
		return trait.getArrayContentsFirst("leader_trait")
	else:
		return trait.getValue("leader_trait")

def extractSprites(db:CWDatabase,mod:mod):
	path = os.path.join(mod.mod_path,'interface')
	CW_list = []
	if os.path.exists(path):
		for file in os.listdir(path=path):
			if file.endswith('.gfx'):
				CW_list = CW_list + fileToCW( os.path.join(path,file), mod )
	for sts in CW_list:
		for element in sts.getElements('spriteType'):
			yield element

def getPortraits(db:CWDatabase,mod:mod,species_class:CWElement,):
	for portrait in species_class.getArrayContentsElements('portraits'):
		yield portrait
	for cpg in species_class.getElements('custom_portraits'):
		for portrait in cpg.getArrayContentsElements('portraits'):
			yield portrait
	for portrait in species_class.getArrayContentsElements('non_randomized_portraits'):
		yield portrait

def getPortraitTrigger(portrait:CWElement,mod:mod,db:CWDatabase,input_key,output_key=None,nrp_value="always"):
	grandparent = portrait.parent.parent
	if match( grandparent.name, 'custom_portraits' ):
		return generateBlockString( grandparent, mod, db, input_key, output_key, output_mode='flatten' )
	elif match( portrait.parent.name, 'non_randomized_portrait' ):
		return nrp_value
	else:
		return "always"

def getTraditions(db:CWDatabase,mod:mod,tradition_category:CWElement):
	base_tradition = db.lookup( tradition_category.getValue('adoption_bonus'), mod )
	base_tradition.metadata['adopt']='yes'
	base_tradition.metadata['finish']='no'
	base_tradition.metadata['caller']=tradition_category
	yield base_tradition
	for swap in base_tradition.getElements('tradition_swap'):
		yield swap
	for base_tradition in db.forArrayLookup(mod,tradition_category):
		if base_tradition.hasSubelements():
			base_tradition.metadata['adopt']='no'
			base_tradition.metadata['finish']='no'
			base_tradition.metadata['tree_position']='sta'
			yield base_tradition
			for swap in base_tradition.getElements('tradition_swap'):
				yield swap
	base_tradition = db.lookup( tradition_category.getValue('finish_bonus'), mod )
	base_tradition.metadata['adopt']='no'
	base_tradition.metadata['finish']='yes'
	base_tradition.metadata['caller']=tradition_category
	yield base_tradition
	for swap in base_tradition.getElements('tradition_swap'):
		yield swap

def getTraditionAttribute(tradition:CWElement,inherit_key):
	if not match(tradition.name,'tradition_swap'):
		return tradition.name
	elif match( tradition.getValue(inherit_key), 'yes' ):
		return tradition.parent.name
	else:
		return tradition.getValue('name')

def getTraditionProperty(tradition:CWElement,base_tradition_value,swap_value):
	if match(tradition.name,'tradition_swap'):
		return swap_value
	else:
		return base_tradition_value

def getTraditionTrigger(tradition:CWElement,mod:mod,db:CWDatabase):
	if not match(tradition.name,'tradition_swap'):
		swap_triggers = []
		for swap in tradition.getElements('tradition_swap'):
			swap_trigger_block = "{} = {{ country = $country$ }}".format( generateBlockString(swap,mod,db,'trigger',root_scope='country',output_mode='export_trigger') )
			swap_triggers.append( swap_trigger_block )
		swap_trigger_block = " ".join(swap_triggers)
		str = "exists = $country$\n\tNOT = {{ {} }}".format( swap_trigger_block  )
		str = str.lower().replace('root','$country$')
		for dlc in dlc_list:
			dlc_check = 'host_has_dlc = '+quoteIfNecessary(dlc)
			str = str.replace( dlc_check.lower(), dlc_check )
		output_key = "tradition_{}_swap_trigger".format( db.primary_key(tradition,mod,db) )
		if str in defined_triggers['export_trigger']:
			return defined_triggers[str]
		if not 'exported_{}'.format(output_key) in tradition.metadata:
			tradition.metadata['exported_{}'.format(output_key)]=True
			file = open(mod.exported_triggers_file,'a')
			file.write( "{} = {{\n\t{}\n}}\n".format(output_key,str) )
			file.close()
		# CWElement.metadata['triggers_written'].append(input_key)
		return output_key
	else:
		return generateBlockString(tradition,mod,db,'trigger',root_scope='country')

def getCountCWE(db:CWDatabase,mod:mod):
	path = os.path.join(mod.mod_path,'interface')
	CW_list = []
	if os.path.exists(path):
		for file in os.listdir(path=path):
			if file.endswith('.gfx'):
				CW_list = CW_list + fileToCW( os.path.join(path,file), mod )
	for sts in CW_list:
		for element in sts.getElements('spriteType'):
			yield element

def getAPTier(ap:CWElement,mod:mod,db:CWDatabase):
	if ap.hasAttribute('possible'):
		for element in ap.getElement('possible').getElements('custom_tooltip'):
			if element.hasAttribute('num_ascension_perks'):
				ap_tier = int( element.getValue('num_ascension_perks') ) + 1
				return str(ap_tier)
	return '0'

def removeAPTier(cw_list:list[CWElement],parent:CWElement):
	for element in cw_list:
		if match( element.name, 'custom_tooltip' ) and element.hasAttribute('num_ascension_perks'):
			cw_list.remove(element)
			return cw_list

def removeNegated(cw_list:list[CWElement],filter):
	for element in cw_list:
		if match( element.name, 'not' ) or match( element.name, 'nor' ):
			for subelement in element.subelements:
				if filter(subelement):
					element.subelements.remove(subelement)
					break
	for element in cw_list:
		if match( element.name, 'not' ) or match( element.name, 'nor' ):
			if len( element.subelements ) == 1:
				element.name = 'not'
			elif len( element.subelements ) == 0:
				cw_list.remove(element)
				return cw_list
	return cw_list

def removeNoSelfRestriction(cw_list:list[CWElement],parent:CWElement):
	filter = lambda x: match( x.name, 'has_ascension_perk' ) and match( x.value, parent.name )
	removeNegated(cw_list,filter)

def getAllowedOnSpecialColony(building:CWElement,modifier,trigger_type='potential'):
	if building.hasAttribute(trigger_type):
		for clause in building.getElement(trigger_type).getArrayContentsElements('nor'):
			if match( clause.name, 'has_modifier' ) and match( clause.value, modifier ):
				return 'no'
		for clause in building.getElement(trigger_type).getArrayContentsElements('not'):
			if match( clause.name, 'has_modifier' ) and match( clause.value, modifier ):
				return 'no'
	return 'yes'

def getRequiredCapitalTier(building:CWElement,mod:mod,db:CWDatabase):
	tiers = { 'has_upgraded_capital':'1', 'has_major_upgraded_capital':'2', 'has_fully_upgraded_capital':'3', 'has_enigmatic_capital':'4', 'has_ascended_capital':'5' }
	for clause in building.getArrayContentsElements('allow'):
		if clause.name.lower() in tiers:
			return tiers[clause.name.lower()]
	return '0'

def getOrbitalCounterpart(building:CWElement,mod:mod,db:CWDatabase):
	for if_block in building.getElements('if'):
		for orbital_defence_block in if_block.getElements('orbital_defence'):
			for starbase_block in orbital_defence_block.getElements('starbase'):
				for nor_block in starbase_block.getElements('no'):
					if nor_block.hasAttribute('has_starbase_building'):
						return nor_block.getValue('has_starbase_building')
	return 'no'
		
def getBranchOfficeSubtype(building:CWElement,mod:mod,db:CWDatabase):
	criminal_attribute = building.getElement('potential').getElement('branch_office_owner').getElement('is_criminal_syndicate')
	if criminal_attribute is not None:
		if match( criminal_attribute.value, 'yes' ):
			return "criminal_corp"
		elif match( criminal_attribute.value, 'no' ):
			return "non_criminal_corp"
	return 'no'

def cleanBuildingPotentialBlock(cw_list:list[CWElement],parent:CWElement):
	for modifier in ['resort_colony','slave_colony','crucible_colony']:
		filter = lambda x: match( x.name, 'has_modifier' ) and match( x.value, modifier )
		removeNegated(cw_list,filter)
	for clause in cw_list:
		if match( clause.name, 'branch_office_owner' ) and clause.hasAttribute('is_criminal_syndicate'):
			clause.subelements.remove( clause.getElement('is_criminal_syndicate') )
			if len( clause.subelements ) == 0:
				cw_list.remove(clause)
				for element in cw_list:
					if match( element.name, 'exists' ) and match( element.value, 'branch_office_owner' ):
						cw_list.remove(element)
						break
				break
	return cw_list

def cleanModifierBlock(cw_list:list[CWElement],parent:CWElement):
	for word in ['description','description_parameters']:
		for element in cw_list:
			if match( element.name, word ):
				cw_list.remove(element)
				break

def cleanBuildingPossibleBlock(cw_list:list[CWElement],parent:CWElement):
	for element in cw_list:
		if match( element.name, 'num_pops' ):
			cw_list.remove(element)
			break
	for tier in ['has_upgraded_capital','has_major_upgraded_capital','has_fully_upgraded_capital','has_enigmatic_capital','has_ascended_capital']:
		for element in cw_list:
			if match( element.name, tier ):
				cw_list.remove(element)
				break
	for if_block in cw_list:
		if (
			match( if_block.name, 'if' )
			and len( if_block.getElement('limit').subelements ) == 1
			and match( if_block.getElement('limit').getValue('exists'), 'orbital_defence' )
		):
			orbital_defence_block = if_block.getElement('orbital_defence')
			starbase_block = orbital_defence_block.getElement('starbase')
			if starbase_block.name != '':
				for filter in [lambda x:match( x.name, 'has_starbase_building' ), lambda x:match( x.name, 'is_starbase_building_building' ),]:
					removeNegated( starbase_block.subelements, filter )
				if len(starbase_block.subelements) == 0:
					orbital_defence_block.subelements.remove(starbase_block)
				if len(orbital_defence_block.subelements) == 1 and match( orbital_defence_block.getValue('exists'), 'starbase' ):
					if_block.subelements.remove(orbital_defence_block)
				if len(if_block.subelements) == 1:
					cw_list.remove(if_block)
					break
	return cw_list

def removeDistrictSetRestriction(cw_list:list[CWElement],parent:CWElement):
	for clause in cw_list:
		if match( clause.name, 'uses_district_set' ):
			cw_list.remove(clause)
			return cw_list
	return cw_list

def cleanColonyTypePotentialBlock(cw_list:list[CWElement],parent:CWElement):
	for condition in ['uses_district_set','has_modifier','is_special_colony_type','is_capital']:
		for clause in cw_list:
			if match( clause.name, condition ):
				cw_list.remove(clause)
				break
	return cw_list

def getEdictStrategicResource(edict:CWElement,mod:mod,db:CWDatabase):
	for potential_block in edict.getElements('potential'):
		for or_block in potential_block.getElements('or'):
			for resource_block in or_block.getElements('has_resource'):
				return resource_block.getValue('type')
	return 'no'

def cleanEdictPotentialBlock(cw_list:list[CWElement],parent:CWElement):
	for clause in cw_list:
		if match( clause.name, 'has_technology' ):
			if clause.value in [ 'tech_planetary_unification', 'tech_ascension_theory' ]:
				cw_list.remove(clause)
			break
	for or_block in cw_list:
		if match( or_block.name, 'or' ):
			if or_block.hasAttribute('has_resource'):
				or_block.subelements.remove( or_block.getElement('has_resource') )
				for condition in or_block.getElements('has_edict'):
					if match( condition.value, parent.name ):
						or_block.subelements.remove(condition)
						if len( or_block.subelements ) == 0:
							cw_list.remove(or_block)
						return cw_list
				return cw_list
	return cw_list

def cleanStarbaseBuildingPotentialBlock(cw_list:list[CWElement],parent:CWElement):
	for clause in cw_list:
		if match( clause.name, 'is_orbital_ring' ) and match( clause.value, 'yes' ):
			cw_list.remove(clause)
			break
	for owner_block in cw_list:
		if match( owner_block.name, 'owner' ):
			if owner_block.hasAttribute('has_technology'):
				owner_block.subelements.remove( owner_block.getElement('has_technology') )
				if len( owner_block.subelements ) == 0:
					cw_list.remove(owner_block)
				return cw_list
	return cw_list

def cleanStarbaseModulePotentialBlock(cw_list:list[CWElement],parent:CWElement):
	for clause in cw_list:
		if match( clause.name, 'is_orbital_ring' ):
			cw_list.remove(clause)
			break
	for owner_block in cw_list:
		if match( owner_block.name, 'owner' ):
			if owner_block.hasAttribute('has_technology'):
				owner_block.subelements.remove( owner_block.getElement('has_technology') )
				if len( owner_block.subelements ) == 0:
					cw_list.remove(owner_block)
				return cw_list
	return cw_list

def getCivicPotentialType(civic:CWElement,mod:mod,db:CWDatabase):
	potential_str = generateBlockString(civic,mod,db,'potential',government=True,output_mode='flatten')
	if potential_str in civic_potential_types:
		return civic_potential_types[potential_str]
	elif potential_str.startswith("or = { or = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial } and = { has_civic = civic_galactic_sovereign_megacorp"):
		return 'corporate'
	elif potential_str.startswith("nor = { has_authority = auth_bugged_corporate_democratic has_authority = auth_corporate has_authority = auth_bugged_corporate_imperial } not = { has_ethic = ethic_gestalt_consciousness }"):
		return 'regular'
	return 'special'

def getEspionageCategory2(operation:CWElement,mod:mod,db:CWDatabase):
	categories = operation.getElement('categories').subelements
	if len(categories) > 1:
		return categories[1].name
	else:
		return 'no'

def generateDemandTrigger(demand:CWElement,mod:mod,db:CWDatabase,input_key,output_key):
	output_key = output_key.format(demand.parent.name,demand.parent.metadata['subelement_index'])
	return generateBlockString(demand,mod,db,input_key,output_key=output_key,root_scope='faction')

def cleanTraitPotentialAddBlock(cw_list:list[CWElement],parent:CWElement):
	for trigger in ['can_do_advanced_gene_modding','can_add_cybernetic_traits',]:
		for clause in cw_list:
			if match( clause.name, trigger ):
				cw_list.remove(clause)
				break
	return cw_list

def cleanTraitPossibleRemoveBlock(cw_list:list[CWElement],parent:CWElement):
	for trigger in ['can_remove_beneficial_genetic_traits','can_remove_cybernetic_traits','can_remove_overtuned_traits','can_remove_presapient_genetic_traits',]:
		for clause in cw_list:
			if match( clause.name, trigger ):
				cw_list.remove(clause)
				break
	return cw_list


databases = {
	'sprites':CWDatabase(
		key='sprites',
		primary_key='sprite',
		get_contents=extractSprites,
		can_write=False,
		script_params={
			'sprite':{'val':lambda x,y,z:x.getValue('name'),},
			'texturefile':{'val':lambda x,y,z:x.getValue('texturefile'),},
		},
	),
	'strategic_resources':CWDatabase(
		key='strategic_resources',
		additional_templates=[('resource_string','utf-8-sig'),('resource_scripted_loc','utf-8'),],
		primary_key='resource',
		filter=lambda x:not x.name in ['time','menace'],
		script_params={
			'resource':{'val':lambda x,y,z:x.name,'index':True,},
			'category':{'val':lambda x,y,z:x.getValue('category'),'index':True,},
			'tradable':{'val':lambda x,y,z:x.getValue('tradable'),},
			'market_amount':{'val':lambda x,y,z:x.getValue('market_amount'),},
			'ai_weight':{'val':lambda x,y,z:x.getElement('ai_weight').getValue('weight'),},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
		},
	),
	# 'agreement_presets':CWDatabase(
	# 	key='agreement_presets',
	# 	primary_key='preset',
	# 	script_params={
	# 		'preset':{'val':lambda x,y,z:x.name,},
	# 		'icon':{'val':lambda x,y,z:x.getValue('icon'),},
	# 		'specialist_type':{'val':lambda x,y,z:x.getValue('specialist_type',),},
	# 		'hidden':{'val':lambda x,y,z:x.getValue('hidden'),},
	# 		'parent':{'val':lambda x,y,z:x.getValue('parent',default=x.name),'index':True,},
	# 		'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential', 'can_propose_{}_agreement', root_scope='subject',from_scope='overlord'),},
	# 	},
	# ),
	'agreement_terms':CWDatabase(
		key='agreement_terms',
		primary_key='term',
		script_params={
			'term':{'val':lambda x,y,z:x.name,'index':True,},
			'term_type':{'val':lambda x,y,z:x.getValue('term_type'),'index':True,},
			'hidden':{'val':lambda x,y,z:x.getValue('hidden'),},
		},
	),
	'agreement_term_values':CWDatabase(
		key='agreement_term_values',
		additional_templates=[('term_string','utf-8-sig'),],
		primary_key='value',
		script_params={
			'value':{'val':lambda x,y,z:x.name,},
			'term':{'val':lambda x,y,z:x.getValue('term'),'foreign_key':'agreement_terms',},
			'monthly_loyalty':{'val':lambda x,y,z:x.getElement('target_modifier').getValue('monthly_loyalty',default='0'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='country'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',root_scope='country'),},
		},
	),
	'archaeological_site_types':CWDatabase(
		key='archaeological_site_types',
		primary_key='site_type',
		script_params={
			'site_type':{'val':lambda x,y,z:x.name,},
		},
	),
	'army_types':CWDatabase(
		key='army_types',
		input_folder="common\\armies",
		primary_key='army_type',
		script_params={
			'army_type':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'defensive':{'val':lambda x,y,z:x.getValue('defensive'),},
			'pop_spawned':{'val':lambda x,y,z:x.getValue('is_pop_spawned'),},
			'pop_limited':{'val':lambda x,y,z:x.getValue('pop_limited',default='yes'),},
			'has_species':{'val':lambda x,y,z:x.getValue('has_species',default='yes'),},
			'has_morale':{'val':lambda x,y,z:x.getValue('has_morale',default='yes'),},
			'health':{'val':lambda x,y,z:x.getValue('health',default='1'),},
			'damage':{'val':lambda x,y,z:x.getValue('damage',default='1'),},
			'morale':{'val':lambda x,y,z:x.getValue('morale',default='-1'),},
			'morale_damage':{'val':lambda x,y,z:x.getValue('morale_damage',default='-1'),},
			'collateral_damage':{'val':lambda x,y,z:x.getValue('collateral_damage',default='1'),},
			'war_exhaustion':{'val':lambda x,y,z:x.getValue('war_exhaustion',default='1'),},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'minerals_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('minerals',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'potential_country_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential_country','can_recruit_{}',root_scope='country'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential','can_recruit_{}_on_planet',root_scope='planet',from_scope='species'),},
		},
	),
	'ascension_perks':CWDatabase(
		key='ascension_perks',
		primary_key='ascension_perk',
		script_params={
			'ascension_perk':{'val':lambda x,y,z:x.name,},
			'required_ap_count':{'val':getAPTier,},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='country',convert_cw=removeNoSelfRestriction),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',root_scope='country',convert_cw=removeAPTier),},
		},
	),
	'bombardment_stances':CWDatabase(
		key='bombardment_stances',
		primary_key='bombardment_stance',
		script_params={
			'bombardment_stance':{'val':lambda x,y,z:x.name,},
			'stop_when_armies_dead':{'val':lambda x,y,z:x.getValue('stop_when_armies_dead'),},
			'abduct_pops':{'val':lambda x,y,z:x.getValue('abduct_pops'),},
			'planet_damage':{'val':lambda x,y,z:x.getValue('planet_damage'),},
			'army_damage':{'val':lambda x,y,z:x.getValue('army_damage'),},
			'min_pops_to_kill_pop':{'val':lambda x,y,z:x.getValue('min_pops_to_kill_pop'),},
			'kill_pop_chance':{'val':lambda x,y,z:x.getElement('kill_pop_chance').getValue('base'),},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
		},
	),
	'buildings':CWDatabase(
		key='buildings',
		primary_key='building',
		script_params={
			'building':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'owner_type':{'val':lambda x,y,z:x.getValue('owner_type'),},
			'branch_office_sybtype':{'val':getBranchOfficeSubtype,},
			'category':{'val':lambda x,y,z:x.getValue('category'),'index':True,},
			'capital':{'val':lambda x,y,z:x.getValue('capital'),},
			'can_build':{'val':lambda x,y,z:x.getValue('can_build',default='yes'),},
			'can_demolish':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'can_be_ruined':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'can_be_disabled':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'base_buildtime':{'val':lambda x,y,z:x.getValue('base_buildtime',default='0'),},
			'upgrade':{'val':lambda x,y,z:x.getArrayContentsFirst('upgrades'),},
			'upgrade_from':{'val':lambda x,y,z:z.lookup(x.name, y, attribute='upgrade', default='no').name,},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'minerals_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('minerals',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'allow_on_resort_colony':{'val':lambda x,y,z:getAllowedOnSpecialColony(x,'resort_colony'),},
			'allow_on_slave_colony':{'val':lambda x,y,z:getAllowedOnSpecialColony(x,'slave_colony'),},
			'allow_on_crucible_colony':{'val':lambda x,y,z:getAllowedOnSpecialColony(x,'crucible_colony'),},
			'minimum_pops':{'val':lambda x,y,z:x.getElement('allow').getValue('num_pops'),},
			'required_capital_level':{'val':getRequiredCapitalTier,},
			'orbital_counterpart':{'val':getOrbitalCounterpart,},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='planet',ai_check=True),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'allow',root_scope='planet',ai_check=True),},
		},
	),
	'districts':CWDatabase(
		key='districts',
		primary_key='district',
		script_params={
			'district':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'can_demolish':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'can_be_ruined':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'can_be_disabled':{'val':lambda x,y,z:x.getValue('can_demolish',default='yes'),},
			'base_buildtime':{'val':lambda x,y,z:x.getValue('base_buildtime',default='0'),},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'minerals_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('minerals',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'allow_on_slave_colony':{'val':lambda x,y,z:getAllowedOnSpecialColony(x,'slave_colony',trigger_type='allow'),},
			'district_set':{'val':lambda x,y,z:x.getElement('potential').getValue('uses_district_set',default='no'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='planet',ai_check=True),},
		},
	),
	'casus_belli':CWDatabase(
		key='casus_belli',
		singular="casus_belli",
		primary_key='casus_belli',
		script_params={
			'casus_belli':{'val':lambda x,y,z:x.name,},
		},
	),
	'colony_types':CWDatabase(
		key='colony_types',
		primary_key='colony_type',
		script_params={
			'colony_type':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'capital':{'val':lambda x,y,z:x.getElement('potential').getValue('is_capital'),},
			'required_modifier':{'val':lambda x,y,z:x.getElement('potential').getValue('has_modifier'),},
			'nonstandard_district_set':{'val':lambda x,y,z:x.getElement('potential').getValue('uses_district_set',default='no'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='planet'),},
		},
	),
	'deposit_categories':CWDatabase(
		key='deposit_categories',
		singular = "deposit_category",
		primary_key='deposit_category',
		script_params={
			'deposit_category':{'val':lambda x,y,z:x.name,'index':True,},
			'blocker':{'val':lambda x,y,z:x.getValue('blocker'),},
			'important':{'val':lambda x,y,z:x.getValue('important'),},
		},
	),
	'colony_deposit_types':CWDatabase(
		key='colony_deposit_types',
		input_folder="common\\deposits",
		filter=lambda x:match( x.getValue('is_for_colonizable'), 'yes' ),
		primary_key='deposit_type',
		script_params={
			'deposit_type':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'category':{'val':lambda x,y,z:x.getValue('category'),'foreign_key':'deposit_categories'},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'natural_blocker':{'val':lambda x,y,z:to_yesno( match( x.getElement('resources').getValue('category'), 'deposit_blockers_natural' ) ),},
			'energy_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('energy',default='0'),},
		},
	),
	'orbital_deposit_types':CWDatabase(
		key='orbital_deposit_types',
		input_folder="common\\deposits",
		filter=lambda x:match( x.getValue('is_for_colonizable'), 'no' ) and not match(x.name,'d_null_deposit'),
		primary_key='deposit_type',
		script_params={
			'deposit_type':{'val':lambda x,y,z:x.name,},
			# 'resource':{'val':lambda x,y,z:x.getElement('resources').getArrayContentsFirst('produces'),},
			'research_station':{'val':lambda x,y,z:to_yesno( match (x.getValue('station'), 'research_station' ) ),},
		},
	),
	'edicts':CWDatabase(
		key='edicts',
		primary_key='edict',
		script_params={
			'edict':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'length':{'val':lambda x,y,z:x.getValue('length'),},
			'unity_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('unity',default='0'),},
			'is_campaign':{'val':lambda x,y,z:to_yesno( match( x.getElement('potential').getValue('has_technology'), 'tech_planetary_unification' ) ),},
			'is_ambition':{'val':lambda x,y,z:to_yesno( match( x.getElement('potential').getValue('has_technology'), 'tech_ascension_theory' ) ),},
			'strategic_resource':{'val':getEdictStrategicResource,},
			'is_sacrifice':{'val':lambda x,y,z:to_yesno( 'sacrifice' in x.name ),},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='country'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'allow',root_scope='country'),},
		},
	),
	'espionage_operation_types':CWDatabase(
		key='espionage_operation_types',
		primary_key='operation_type',
		script_params={
			'operation_type':{'val':lambda x,y,z:x.name,},
			'primitive_target':{'val':lambda x,y,z:x.getElement('potential').getElement('target').getValue('is_primitive'),},
			'spy_power_cost':{'val':lambda x,y,z:x.getValue('spy_power_cost',default='0'),},
			'operation_category':{'val':lambda x,y,z:x.getArrayContentsFirst('categories'),},
			'intel_category':{'val':getEspionageCategory2,},
			'influence_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('influence',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
		},
	),
	'event_chains':CWDatabase(
		key='event_chains',
		primary_key='event_chain',
		script_params={
			'event_chain':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
		},
	),
	'federation_laws':CWDatabase(
		key='federation_laws',
		primary_key='law',
		array_key='laws',
		script_params={
			'law':{'val':lambda x,y,z:x.name,},
			'required_centralization':{'val':lambda x,y,z:x.getElement('required_centralization').getValue('base',default='0'),},
			'cohesion_growth':{'val':lambda x,y,z:x.getValue('cohesion_growth',default='0'),},
			'category':{'val':lambda x,y,z:x.getCaller().name,'foreign_key':'federation_law_categories',},
		},
		top_level=False
	),
	'federation_law_categories':CWDatabase(
		key='federation_law_categories',
		singular='federation_law_category',
		primary_key='law_category',
		script_params={
			'law_category':{'val':lambda x,y,z:x.name,},
		},
		subunits=['federation_laws',]
	),
	'federation_types':CWDatabase(
		key='federation_types',
		primary_key='federation_type',
		script_params={
			'federation_type':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='country'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'allow',root_scope='country'),},
		},
	),
	'galactic_focuses':CWDatabase(
		key='galactic_focuses',
		singular='galactic_focus',
		primary_key='galactic_focus',
		script_params={
			'galactic_focus':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
		},
	),
	'authorities':CWDatabase(
		key='authorities',
		singular='authority',
		input_folder="common\\governments\\authorities",
		primary_key='authority',
		script_params={
			'authority':{'val':lambda x,y,z:x.name,},
			'can_reform':{'val':lambda x,y,z:x.getValue('can_reform'),},
			'has_heir':{'val':lambda x,y,z:x.getValue('has_heir'),},
			'election_term_years':{'val':lambda x,y,z:x.getValue('election_term_years',default='-1'),},
			'can_have_emergency_elections':{'val':lambda x,y,z:x.getValue('can_have_emergency_elections'),},
			'emergency_election_cost':{'val':lambda x,y,z:x.getValue('emergency_election_cost',default='-1'),},
			'has_agendas':{'val':lambda x,y,z:x.getValue('has_agendas'),},
			'uses_mandates':{'val':lambda x,y,z:x.getValue('uses_mandates'),},
			'playable_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'playable'),},
			'potential':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',government=True,output_mode='flatten'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',government=True),},
		},
	),
	'civics':CWDatabase(
		key='civics',
		input_folder="common\\governments\\civics",
		additional_templates=[('civic_sprite','utf-8'),],
		filter=lambda x:match( x.getValue('is_origin'), 'no' ),
		primary_key='civic',
		script_params={
			'civic':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue("icon",default="gfx/interface/icons/governments/civics/{}.dds".format(x.name))},
			'playable_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'playable'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',government=True,output_mode='flatten'),},
			'potential_type':{'val':getCivicPotentialType,},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',government=True),},
			'random_weight':{'val':lambda x,y,z:x.getElement("random_weight").getValue("base"),},
			'trait':{'val':lambda x,y,z:x.getElement("traits").getValue("trait"),},
			'secondary_species':{'val':lambda x,y,z:x.getElement("has_secondary_species").getValue("title"),},
			'secondary_species_trait':{'val':lambda x,y,z:x.getElement("has_secondary_species").getElement("traits").getValue("trait"),},
			'starting_colony':{'val':lambda x,y,z:x.getValue("starting_colony"),},
			'pickable_at_start':{'val':lambda x,y,z:x.getValue("pickable_at_start",default='yes'),},
			'habitability_preference':{'val':lambda x,y,z:x.getValue("habitability_preference"),},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
	),
	'origins':CWDatabase(
		key='origins',
		input_folder="common\\governments\\civics",
		additional_templates=[('origin_tooltip','utf-8-sig'),('origin_sprite','utf-8'),],
		filter=lambda x:match( x.getValue('is_origin'), 'yes' ),
		primary_key='origin',
		script_params={
			'origin':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue("icon",default="gfx/interface/icons/governments/civics/{}.dds".format(x.name))},
			'playable_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'playable'),},
			'initial':{'val':lambda x,y,z:x.getElement('potential').getValue('always',default='yes'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',government=True),},
			'random_weight':{'val':lambda x,y,z:x.getElement("random_weight").getValue("base"),},
			'trait':{'val':lambda x,y,z:x.getElement("traits").getValue("trait"),},
			'secondary_species':{'val':lambda x,y,z:x.getElement("has_secondary_species").getValue("title"),},
			'secondary_species_trait':{'val':lambda x,y,z:x.getElement("has_secondary_species").getElement("traits").getValue("trait"),},
			'starting_colony':{'val':lambda x,y,z:x.getValue("starting_colony"),},
			'habitability_preference':{'val':lambda x,y,z:x.getValue("habitability_preference"),},
			'custom_initializers':{'val':lambda x,y,z:to_yesno( x.hasAttribute('initializers') ),},
			'max_once_global':{'val':lambda x,y,z:x.getValue("max_once_global"),},
			'advanced_start':{'val':lambda x,y,z:x.getValue("advanced_start"),},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
	),
	'governments':CWDatabase(
		key='governments',
		primary_key='government',
		script_params={
			'government':{'val':lambda x,y,z:x.name,},
		},
	),
	'megastructure_types':CWDatabase(
		key='megastructure_types',
		input_folder="common\\megastructures",
		primary_key='megastructure_type',
		script_params={
			'megastructure_type':{'val':lambda x,y,z:x.name,},
			'build_time':{'val':lambda x,y,z:x.getValue("build_time",default='0'),},
			'alloys_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('alloys',default='0'),},
			'upgrade_from':{'val':lambda x,y,z:x.getArrayContentsFirst('upgrade_from'),},
			'upgrade':{'val':lambda x,y,z:z.lookup(x.name, y, attribute='upgrade_from', default='no').name,},
			'filename':{'val':lambda x,y,z:x.filename,},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'unity_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('unity',default='0'),},
			'influence_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('influence',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'country_modifier',output_mode='export_modifier'),},
		},
	),
	'observation_station_missions':CWDatabase(
		key='observation_station_missions',
		primary_key='mission',
		script_params={
			'mission':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue("icon")},
			'small_icon':{'val':lambda x,y,z:x.getValue("small_icon")},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='observer',from_scope='target'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'valid',root_scope='observer',from_scope='target'),},
		},
	),
	'personalities':CWDatabase(
		key='personalities',
		singular='personality',
		primary_key='personality',
		script_params={
			'personality':{'val':lambda x,y,z:x.name,},
			'aggressiveness:':{'val':lambda x,y,z:x.getValue("aggressiveness")},
			'trade_willingness:':{'val':lambda x,y,z:x.getValue("trade_willingness")},
			'bravery:':{'val':lambda x,y,z:x.getValue("bravery")},
			'combat_bravery:':{'val':lambda x,y,z:x.getValue("combat_bravery",default='0')},
			'military_spending:':{'val':lambda x,y,z:x.getValue("military_spending",default='0')},
			'colony_spending:':{'val':lambda x,y,z:x.getValue("colony_spending",default='0')},
			'nap_acceptance:':{'val':lambda x,y,z:x.getValue("nap_acceptance",default='0')},
			'commercial_pact_acceptance:':{'val':lambda x,y,z:x.getValue("commercial_pact_acceptance",default='0')},
			'research_agreement_acceptance:':{'val':lambda x,y,z:x.getValue("research_agreement_acceptance",default='0')},
			'defensive_pact_acceptance:':{'val':lambda x,y,z:x.getValue("defensive_pact_acceptance",default='0')},
			'migration_pact_acceptance:':{'val':lambda x,y,z:x.getValue("migration_pact_acceptance",default='0')},
			'advanced_start_chance:':{'val':lambda x,y,z:x.getValue("advanced_start_chance",default='0')},
			'armor_ratio:':{'val':lambda x,y,z:x.getValue("armor_ratio",default='0')},
			'shields_ratio:':{'val':lambda x,y,z:x.getValue("shields_ratio",default='0')},
			'hull_ratio:':{'val':lambda x,y,z:x.getValue("hull_ratio",default='0')},
			'threat_modifier:':{'val':lambda x,y,z:x.getValue("threat_modifier",default='0')},
			'threat_others_modifier:':{'val':lambda x,y,z:x.getValue("threat_others_modifier",default='0')},
			'friction_modifier:':{'val':lambda x,y,z:x.getValue("friction_modifier",default='0')},
			'claims_modifier:':{'val':lambda x,y,z:x.getValue("claims_modifier",default='0')},
		},
	),
	'planet_classes':CWDatabase(
		key='planet_classes',
		singular='planet_class',
		filter=lambda x:not match( x.name, 'random_list' ),
		primary_key='planet_class',
		script_params={
			'planet_class':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'star':{'val':lambda x,y,z:x.getValue('star'),},
			'colonizable':{'val':lambda x,y,z:x.getValue('colonizable'),},
			'climate':{'val':lambda x,y,z:x.getValue('climate'),},
			'initial':{'val':lambda x,y,z:x.getValue('initial'),},
			'artificial':{'val':lambda x,y,z:x.getValue('artificial'),},
			'spawn_odds':{'val':lambda x,y,z:x.getValue('spawn_odds'),},
			'carry_cap_per_free_district':{'val':lambda x,y,z:x.getValue('carry_cap_per_free_district'),},
		},
	),
	'habitable_planet_classes':CWDatabase(
		key='habitable_planet_classes',
		singular='habitable_planet_class',
		input_folder="common\\planet_classes",
		filter=lambda x:match( x.getValue('colonizable'), 'yes' ),
		primary_key='planet_class',
		script_params={
			'planet_class':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'star':{'val':lambda x,y,z:x.getValue('star'),},
			'colonizable':{'val':lambda x,y,z:x.getValue('colonizable'),},
			'climate':{'val':lambda x,y,z:x.getValue('climate'),'index':True,},
			'initial':{'val':lambda x,y,z:x.getValue('initial'),},
			'artificial':{'val':lambda x,y,z:x.getValue('artificial'),},
			'spawn_odds':{'val':lambda x,y,z:x.getValue('spawn_odds'),},
			'carry_cap_per_free_district':{'val':lambda x,y,z:x.getValue('carry_cap_per_free_district'),},
		},
	),
	'policies':CWDatabase(
		key='policies',
		singular='policy',
		primary_key='policy',
		subelement_name='option',
		additional_templates=[('policy_string','utf-8-sig')],
		script_params={
			'policy':{'val':lambda x,y,z:x.getValue('name'),},
			'policy_flag':{'val':lambda x,y,z:x.getArrayContentsFirst( 'policy_flags', default=x.getValue('name'), log_if_empty="policy {} in mod {} has no flags".format(x.getValue('name'),y.key) ),},
			# 'policy_potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential'),},
			# 'policy_possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible'),},
			'category':{'val':lambda x,y,z:x.parent.name,'foreign_key':'policy_categories',},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
		top_level=False
	),
	'policy_categories':CWDatabase(
		key='policy_categories',
		input_folder="common\\policies",
		singular='policy_category',
		primary_key='policy_category',
		script_params={
			'policy_category':{'val':lambda x,y,z:x.name,},
			# 'category_potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential'),},
			# 'category_possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'valid'),},
		},
		subunits=['policies',],
	),
	'demands':CWDatabase(
		key='demands',
		primary_key='title',
		subelement_name='demand',
		additional_templates=[('demand_string','utf-8-sig')],
		script_params={
			'title':{'val':lambda x,y,z:x.getValue('title'),},
			'unfulfilled_title':{'val':lambda x,y,z:x.getValue('unfulfilled_title'),},
			'desc':{'val':lambda x,y,z:x.getValue('desc'),},
			'fulfilled_effect':{'val':lambda x,y,z:x.getValue('fulfilled_effect'),},
			'unfulfilled_effect':{'val':lambda x,y,z:x.getValue('unfulfilled_effect'),},
			'demand_made_trigger':{'val':lambda x,y,z:generateDemandTrigger(x,y,z,'potential',output_key='demand_made_trigger_{}_{}_{{}}'),},
			'demand_fulfilled_trigger':{'val':lambda x,y,z:generateDemandTrigger(x,y,z,'trigger',output_key='demand_fulfilled_trigger_{}_{}_{{}}'),},
			'faction_type':{'val':lambda x,y,z:x.parent.name,'foreign_key':'pop_faction_types',},
		},
		top_level=False,
	),
	'pop_faction_types':CWDatabase(
		key='pop_faction_types',
		primary_key='faction_type',
		script_params={
			'faction_type':{'val':lambda x,y,z:x.name,},
			'guiding_ethic':{'val':lambda x,y,z:x.getValue('guiding_ethic'),'index':True},
			# 'can_join':{'val':lambda x,y,z:generateBlockString(x,y,z,'can_join_faction','pop'),},
		},
		subunits=['demands',],
	),
	'pop_jobs':CWDatabase(
		key='pop_jobs',
		primary_key='job',
		script_params={
			'job':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'economic_category':{'val':lambda x,y,z:x.getElement('resources').getValue('category'),'index':True,},
		},
	),
	'relics':CWDatabase(
		key='relics',
		additional_templates=[('relic_sprite','utf-8'),],
		primary_key='relic',
		script_params={
			'relic':{'val':lambda x,y,z:x.name,},
			'sprite_name':{'val':lambda x,y,z:x.getValue('portrait'),'foreign_key':'sprites',},
		},
	),
	'resolutions':CWDatabase(
		key='resolutions',
		primary_key='resolution',
		array_key='resolution_types',
		script_params={
			'resolution':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'target':{'val':lambda x,y,z:x.getValue('target'),},
			'harmful':{'val':lambda x,y,z:x.getValue('harmful'),},
			'sanction':{'val':lambda x,y,z:x.getValue('sanction'),},
			'fire_and_forget':{'val':lambda x,y,z:x.getValue('fire_and_forget'),},
			'level':{'val':lambda x,y,z:x.getValue('level',default='0'),},
			'target':{'val':lambda x,y,z:x.getValue('target'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='country'),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'allow',root_scope='country'),},
			'category':{'val':lambda x,y,z:x.getCaller().name,'foreign_key':'resolution_categories',},
		},
		top_level=False
	),
	'resolution_categories':CWDatabase(
		key='resolution_categories',
		singular='resolution_category',
		primary_key='resolution_category',
		script_params={
			'resolution_category':{'val':lambda x,y,z:x.name,},
			'group':{'val':lambda x,y,z:x.getValue('group'),'index':True},
			'category_icon':{'val':lambda x,y,z:x.getValue('icon'),},
		},
		subunits=['resolutions',],
	),
	'ship_sizes':CWDatabase(
		key='ship_sizes',
		primary_key='ship_size',
		reverse=True,
		script_params={
			'ship_size':{'val':lambda x,y,z:x.name,},
			'ship_class':{'val':lambda x,y,z:x.getValue('class'),'index':True},
			'icon':{'val':lambda x,y,z:x.getValue('icon')},
			'icon_frame':{'val':lambda x,y,z:x.getValue('icon_frame')},
			'fleet_slot_size':{'val':lambda x,y,z:x.getValue('fleet_slot_size')},
			'size_multiplier':{'val':lambda x,y,z:x.getValue('size_multiplier')},
			'designable':{'val':lambda x,y,z:x.getValue('is_designable')},
			'default_design':{'val':lambda x,y,z:x.getValue('enable_default_design')},
			'shipyard_construction':{'val':lambda x,y,z:to_yesno( match( x.getValue("construction_type"), "starbase_shipyard" ) )},
			'prereq_tech':{'val':lambda x,y,z:x.getArrayContentsFirst('prerequisites'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'defense_platforms':{'val':lambda x,y,z:x.getElement("modifier").getValue("starbase_defense_platform_capacity_add",default="0")},
			'modules':{'val':lambda x,y,z:x.getElement("modifier").getValue("starbase_module_capacity_add",default="0")},
			'buildings':{'val':lambda x,y,z:x.getElement("modifier").getValue("starbase_building_capacity_add",default="0")},
		},
	),
	'starbase_sizes':CWDatabase(
		key='starbase_sizes',
		input_folder="common\\starbase_levels",
		additional_templates=[('starbase_string','utf-8-sig'),],
		primary_key='ship_size',
		reverse=True,
		script_params={
			'ship_size':{'val':lambda x,y,z:x.getValue('ship_size'),'foreign_key':'ship_sizes',},
			'starbase_level':{'val':lambda x,y,z:x.name,},
			'upgrade_from':{'val':lambda x,y,z:z.lookup( x.getValue('ship_size'), y, attribute='upgrade', default='no').getValue('ship_size'),},
			'upgrade':{'val':lambda x,y,z:z.lookup( x.getValue('next_level'), y, attribute='starbase_level', default='no' ).getValue('ship_size'),'index':True},
			'show_in_outliner':{'val':lambda x,y,z:x.getValue('show_in_outliner',default='yes'),},
			'display_empire_shield':{'val':lambda x,y,z:x.getValue('display_empire_shield'),},
			'display_map_icon':{'val':lambda x,y,z:x.getValue('display_map_icon',default='yes'),},
			'level_weight':{'val':lambda x,y,z:x.getValue('level_weight',default='0'),},
			'collects_trade':{'val':lambda x,y,z:x.getValue('collects_trade',default='yes'),},
			'potential_home_base':{'val':lambda x,y,z:x.getValue('display_map_icon'),},
		},
	),
	'approaches':CWDatabase(
		key='approaches',
		singular='approach',
		primary_key='approach',
		subelement_name='approach',
		script_params={
			'approach':{'val':lambda x,y,z:x.getValue('name')},
			'icon':{'val':lambda x,y,z:x.getValue('icon')},
			# 'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential','situation'),},
			# 'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'allow','situation'),},
			'situation':{'val':lambda x,y,z:x.parent.name,'foreign_key':'situations',},
		},
		top_level=False,
	),
	'situations':CWDatabase(
		key='situations',
		primary_key='situation',
		script_params={
			'situation':{'val':lambda x,y,z:x.name,},
			'complete_icon':{'val':lambda x,y,z:x.getValue('complete_icon')},
			'fail_icon':{'val':lambda x,y,z:x.getValue('fail_icon')},
			'category':{'val':lambda x,y,z:x.getValue('category'),'index':True},
			'progress_direction':{'val':lambda x,y,z:x.getValue('progress_direction')},
		},
		subunits=['approaches',],
	),
	'special_projects':CWDatabase(
		key='special_projects',
		primary_key='project',
		script_params={
			'project':{'val':lambda x,y,z:x.getValue('key'),},
		},
	),
	'species_archetypes':CWDatabase(
		key='species_archetypes',
		primary_key='archetype',
		script_params={
			'archetype':{'val':lambda x,y,z:x.name,'index':True},
			'robotic':{'val':lambda x,y,z:x.getValue('robotic')},
		},
	),
	'portraits':CWDatabase(
		key='portraits',
		primary_key='portrait',
		get_subelements=getPortraits,
		script_params={
			'portrait':{'val':lambda x,y,z:x.name,},
			'playable_trigger':{'val':lambda x,y,z:getPortraitTrigger(x,y,z,'playable',nrp_value="always"),},
			'randomized_trigger':{'val':lambda x,y,z:getPortraitTrigger(x,y,z,'randomized',nrp_value="never"),},
			'species_class':{'val':lambda x,y,z:x.getRoot().name,'foreign_key':'species_classes',},
		},
		top_level=False
	),
	'species_classes':CWDatabase(
		key='species_classes',
		primary_key='species_class',
		singular='species_class',
		script_params={
			'species_class':{'val':lambda x,y,z:x.name,},
			'archetype':{'val':lambda x,y,z:x.getValue('archetype'),'foreign_key':'species_archetypes'},
			'randomized':{'val':lambda x,y,z:getYesNoTrigger(x,y,z,'randomized',default='yes'),},
			'graphical_culture':{'val':lambda x,y,z:x.getValue('graphical_culture')},
			'species_class_playable_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'playable',output_mode='flatten'),},
			'species_class_possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',government=True,output_mode='flatten'),},
		},
		subunits=['portraits',],
	),
	'species_rights_citizenship':CWDatabase(
		key='species_rights_citizenship',
		singular='species_right_citizenship',
		input_folder="common\\species_rights\\citizenship_types",
		inline_script_path=["right","citizenship"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"citizenship_type",},
			'right_icon':{'val':lambda x,y,z:"citizenship",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_living_standards':CWDatabase(
		key='species_rights_living_standards',
		singular='species_right_living_standards',
		input_folder="common\\species_rights\\living_standards",
		inline_script_path=["right","living_standards"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"living_standard",},
			'right_icon':{'val':lambda x,y,z:"living_standards",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_military_service':CWDatabase(
		key='species_rights_military_service',
		singular='species_right_military_service',
		input_folder="common\\species_rights\\military_service_types",
		inline_script_path=["right","military_service"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"military_service_type",},
			'right_icon':{'val':lambda x,y,z:"military_service",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_slavery':CWDatabase(
		key='species_rights_slavery',
		singular='species_right_slavery',
		input_folder="common\\species_rights\\slavery_types",
		inline_script_path=["right","slavery"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"slavery_type",},
			'right_icon':{'val':lambda x,y,z:"slavery_type",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_purge':CWDatabase(
		key='species_rights_purge',
		singular='species_right_purge',
		input_folder="common\\species_rights\\purge_types",
		inline_script_path=["right","purge"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"purge_type",},
			'right_icon':{'val':lambda x,y,z:"purge_type",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_migration':CWDatabase(
		key='species_rights_migration',
		singular='species_right_migration',
		input_folder="common\\species_rights\\migration_controls",
		inline_script_path=["right","migration"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"migration_control",},
			'right_icon':{'val':lambda x,y,z:"migration_controls",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_population':CWDatabase(
		key='species_rights_population',
		singular='species_right_population',
		input_folder="common\\species_rights\\population_controls",
		inline_script_path=["right","population"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"population_control",},
			'right_icon':{'val':lambda x,y,z:"population_controls",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'species_rights_colonization':CWDatabase(
		key='species_rights_colonization',
		singular='species_right_colonization',
		input_folder="common\\species_rights\\colonization_controls",
		inline_script_path=["right","colonization"],
		additional_templates=[('rights_string','utf-8-sig'),],
		primary_key='right',
		script_params={
			'right_category':{'val':lambda x,y,z:"colonization_control",},
			'right_icon':{'val':lambda x,y,z:"colonization_controls",},
			'right':{'val':lambda x,y,z:x.name,},
		},
	),
	'starbase_buildings':CWDatabase(
		key='starbase_buildings',
		primary_key='building',
		script_params={
			'building':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'construction_days':{'val':lambda x,y,z:x.getValue('construction_days'),},
			'alloys_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('alloys',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'prereq_tech':{'val':lambda x,y,z:x.getElement('potential').getElement('owner').getValue('has_technology'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'orbital_ring_only':{'val':lambda x,y,z:x.getElement('potential').getValue('is_orbital_ring'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='starbase',convert_cw=cleanStarbaseBuildingPotentialBlock,from_scope='country',ai_check=True),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',root_scope='starbase',from_scope='country',ai_check=True),},
		},
	),
	'starbase_modules':CWDatabase(
		key='starbase_modules',
		additional_templates=[('starbase_module_string','utf-8-sig'),],
		primary_key='module',
		script_params={
			'module':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon'),},
			'construction_days':{'val':lambda x,y,z:x.getValue('construction_days'),},
			'alloys_cost':{'val':lambda x,y,z:x.getElement('resources').getElement('cost').getValue('alloys',default='0'),},
			'energy_upkeep':{'val':lambda x,y,z:x.getElement('resources').getElement('upkeep').getValue('energy',default='0'),},
			'prereq_tech':{'val':lambda x,y,z:x.getElement('potential').getElement('owner').getValue('has_technology'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'orbital_ring_only':{'val':lambda x,y,z:x.getElement('potential').getValue('is_orbital_ring'),},
			'potential_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'potential',root_scope='starbase',from_scope='country',ai_check=True),},
			'possible_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'possible',root_scope='starbase',convert_cw=cleanStarbaseModulePotentialBlock,from_scope='country',ai_check=True),},
		},
	),
	'starbase_types':CWDatabase(
		key='starbase_types',
		primary_key='starbase_type',
		script_params={
			'starbase_type':{'val':lambda x,y,z:x.name,},
		},
	),
	'technology_categories':CWDatabase(
		key='technology_categories',
		singular='technology_category',
		input_folder="common\\technology\\category",
		primary_key='tech_cat',
		script_params={
			'tech_cat':{'val':lambda x,y,z:x.name,},
		},
	),
	'technology_physics':CWDatabase(
		key='technology_physics',
		singular='technology_physics',
		input_folder="common\\technology",
		inline_script_path=["technology","physics"],
		additional_templates=[('tech_sprite','utf-8'),('tech_string','utf-8-sig')],
		filter=lambda x:match( x.getValue('area'), 'physics' ),
		primary_key='tech',
		script_params={
			'tech':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name).replace('t_space_construction',x.name),},
			'category':{'val':lambda x,y,z:x.getArrayContentsFirst("category"),'index':True},
			'start_tech':{'val':lambda x,y,z:x.getValue('start_tech'),},
			'tier':{'val':lambda x,y,z:x.getValue('tier',default='0'),},
			'cost':{'val':lambda x,y,z:x.getValue('cost',default='0'),},
			'insight':{'val':lambda x,y,z:x.getValue('is_insight'),},
			'rare':{'val':lambda x,y,z:x.getValue('is_rare'),},
			'dangerous':{'val':lambda x,y,z:x.getValue('is_dangerous'),},
			'background':{'val':getTechBackground,},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
	),
	'technology_society':CWDatabase(
		key='technology_society',
		singular='technology_society',
		input_folder="common\\technology",
		inline_script_path=["technology","society"],
		additional_templates=[('tech_sprite','utf-8'),('tech_string','utf-8-sig')],
		filter=lambda x:match( x.getValue('area'), 'society' ),
		primary_key='tech',
		script_params={
			'tech':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'category':{'val':lambda x,y,z:x.getArrayContentsFirst("category"),'index':True},
			'start_tech':{'val':lambda x,y,z:x.getValue('start_tech'),},
			'tier':{'val':lambda x,y,z:x.getValue('tier',default='0'),},
			'cost':{'val':lambda x,y,z:x.getValue('cost',default='0'),},
			'insight':{'val':lambda x,y,z:x.getValue('is_insight'),},
			'rare':{'val':lambda x,y,z:x.getValue('is_rare'),},
			'dangerous':{'val':lambda x,y,z:x.getValue('is_dangerous'),},
			'background':{'val':getTechBackground,},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
	),
	'technology_engineering':CWDatabase(
		key='technology_engineering',
		singular='technology_engineering',
		input_folder="common\\technology",
		inline_script_path=["technology","engineering"],
		additional_templates=[('tech_sprite','utf-8'),('tech_string','utf-8-sig')],
		filter=lambda x:match( x.getValue('area'), 'engineering' ),
		primary_key='tech',
		script_params={
			'tech':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue('icon',default=x.name),},
			'category':{'val':lambda x,y,z:x.getArrayContentsFirst("category"),'index':True},
			'start_tech':{'val':lambda x,y,z:x.getValue('start_tech'),},
			'tier':{'val':lambda x,y,z:x.getValue('tier',default='0'),},
			'cost':{'val':lambda x,y,z:x.getValue('cost',default='0'),},
			'insight':{'val':lambda x,y,z:x.getValue('is_insight'),},
			'rare':{'val':lambda x,y,z:x.getValue('is_rare'),},
			'dangerous':{'val':lambda x,y,z:x.getValue('is_dangerous'),},
			'background':{'val':getTechBackground,},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
	),
	'traditions':CWDatabase(
		key='traditions',
		primary_key='tradition',
		array_key='traditions',
		get_subelements=getTraditions,
		script_params={
			'tradition':{'val':lambda x,y,z:getTraditionProperty(x,x.name,x.getValue('name')),},
			'name':{'val':lambda x,y,z:getTraditionAttribute(x,'inherit_name'),},
			'icon':{'val':lambda x,y,z:getTraditionAttribute(x,'inherit_icon'),},
			'is_swap':{'val':lambda x,y,z:getTraditionProperty(x,'no','yes'),},
			'inherits_effect':{'val':lambda x,y,z:x.getValue('inherit_effects'),},
			'base_tradition':{'val':lambda x,y,z:x.getRoot().name,},
			'adopt':{'val':lambda x,y,z:x.getRoot().metadata['adopt'],},
			'finish':{'val':lambda x,y,z:x.getRoot().metadata['finish'],},
			'swap_trigger':{'val':lambda x,y,z:getTraditionTrigger(x,y,z),},
			'category':{'val':lambda x,y,z:x.getRoot().getCaller().name,'foreign_key':'tradition_categories',},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
		},
		top_level=False
	),
	'tradition_categories':CWDatabase(
		key='tradition_categories',
		singular='tradition_category',
		additional_templates=[('tradition_cat_string','utf-8-sig'),],
		primary_key='tradition_category',
		script_params={
			'tradition_category':{'val':lambda x,y,z:x.name,},
			'start_tradition':{'val':lambda x,y,z:x.getValue('adoption_bonus'),},
			'finish_tradition':{'val':lambda x,y,z:x.getValue('finish_bonus'),},
		},
		subunits=['traditions'],
	),
	'species_traits':CWDatabase(
		key='species_traits',
		input_folder="common\\traits",
		additional_templates=[('species_trait_option_text','utf-8-sig'),('trait_sprite','utf-8')],
		filter=lambda x:x.hasAttribute('allowed_archetypes'),
		primary_key='trait',
		script_params={
			'trait':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue("icon",default="gfx/interface/icons/traits/{}.dds".format(x.name)),},
			'cost':{'val':lambda x,y,z:x.getElement("cost").getValue("base",default="0"),},
			'cost_sign':{'val':getSign,},
			'initial':{'val':lambda x,y,z:x.getValue("initial",default='yes'),},
			'randomized':{'val':lambda x,y,z:x.getValue("randomized",default='yes'),},
			'advanced_trait':{'val':lambda x,y,z:x.getValue("advanced_trait"),},
			'trait_type':{'val':getTraitType,'index':True,},
			'uplifters_can_remove':{'val':lambda x,y,z:x.getElement('species_possible_remove').getValue('can_remove_presapient_genetic_traits'),},
			'no_opposites_trigger':{'val':lambda x,y,z:x.getArrayTriggers('opposites','has_trait',mode='NOR'),},
			'allowed_archetypes_trigger':{'val':lambda x,y,z:x.getArrayTriggers('allowed_archetypes','is_archetype',mode='OR'),},
			'species_class_trigger':{'val':lambda x,y,z:x.getArrayTriggers('species_class','is_species_class',mode='OR'),},
			'allowed_planet_classes_planet_trigger':{'val':lambda x,y,z:x.getArrayTriggers('allowed_planet_classes','is_planet_class',mode='OR'),},
			'allowed_planet_classes_preference_trigger':{'val':lambda x,y,z:x.getArrayTriggers('allowed_planet_classes','ideal_planet_class',mode='OR'),},
			'allowed_origins_trigger':{'val':lambda x,y,z:x.getArrayTriggers('allowed_origins','has_origin',mode='OR'),},
			'allowed_ethics_trigger':{'val':lambda x,y,z:x.getArrayTriggers('allowed_ethics','has_ethic',mode='OR'),},
			'potential_add_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'species_potential_add',root_scope='species',from_scope='country',convert_cw=cleanTraitPotentialAddBlock),},
			'possible_remove_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'species_possible_remove',root_scope='species',from_scope='country',convert_cw=cleanTraitPossibleRemoveBlock),},
		},
	),
	'leader_traits':CWDatabase(
		key='leader_traits',
		input_folder="common\\traits",
		filter=lambda x:x.hasAttribute('leader_trait'),
		primary_key='trait',
		script_params={
			'trait':{'val':lambda x,y,z:x.name,},
			'icon':{'val':lambda x,y,z:x.getValue("icon",default="gfx/interface/icons/traits/{}.dds".format(x.name)),},
			'cost':{'val':lambda x,y,z:x.getElement("cost").getValue("base",default="0"),},
			'initial':{'val':lambda x,y,z:x.getValue("initial",default='yes'),},
			'randomized':{'val':lambda x,y,z:x.getValue("randomized",default='yes'),},
			'leader_class':{'val':getLeaderClass,'index':True,},
			'prereq_tech':{'val':lambda x,y,z:x.getElement('potential').getElement('owner').getValue('has_technology'),},
			'has_prereqs_trigger':{'val':lambda x,y,z:x.getArrayTriggers('prerequisites','has_technology',mode='AND'),},
			'potential_add_trigger':{'val':lambda x,y,z:generateBlockString(x,y,z,'leader_potential_add',root_scope='leader',from_scope='country'),},
			'no_opposites_trigger':{'val':lambda x,y,z:x.getArrayTriggers('opposites','has_trait',mode='NOR'),},
			'modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'modifier',output_mode='export_modifier'),},
			'self_modifier':{'val':lambda x,y,z:generateBlockString(x,y,z,'self_modifier',output_mode='export_modifier'),},
		},
		additional_templates=[('trait_display_text','utf-8-sig'),('trait_text_icon','utf-8')]
	),
	'war_goals':CWDatabase(
		key='war_goals',
		primary_key='wargoal',
		script_params={
			'wargoal':{'val':lambda x,y,z:x.name,},
			'total_war':{'val':lambda x,y,z:x.getValue("total_war"),},
			'defender_wargoal':{'val':lambda x,y,z:x.getValue("set_defender_wargoal"),},
			'surrender_acceptance':{'val':lambda x,y,z:x.getValue("surrender_acceptance",default='0'),},
			'war_exhaustion':{'val':lambda x,y,z:x.getValue("war_exhaustion",default='1'),},
			'can_create_country':{'val':lambda x,y,z:x.getValue("release_occupied_systems_on_status_quo",),},
			'cede_claims':{'val':lambda x,y,z:x.getValue("cede_claims",default='yes'),},
			'casus_belli':{'val':lambda x,y,z:x.getValue("casus_belli"),'foreign_key':'casus_belli',},
		},
	),
	'10':numberedEntryGenerator(10),
	'25':numberedEntryGenerator(25,[('support_governor_candidate_text','utf-8-sig')]),
	'50':numberedEntryGenerator(50),
	'100':numberedEntryGenerator(100),
	'250':numberedEntryGenerator(250,[('starbase_string','utf-8-sig'),('support_faction_leader_text','utf-8-sig')]),
	'500':numberedEntryGenerator(500),
}

saved_data = {}
indexes = {}

def fetch(db,key,inheritance_list):
	for mod in inheritance_list:
		if db in saved_data[mod] and key in saved_data[mod][db]:
			return saved_data[mod][db][key]

placeholder_scripted_effects_path = os.path.join( vanilla.scripted_effect_path, "00_rst_placeholder_effects.txt" )
placeholder_scripted_effects_file = open(placeholder_scripted_effects_path,'w')
placeholder_scripted_effects_file.write("")
placeholder_scripted_effects_file.close()

placeholder_scripted_triggers_path = os.path.join( vanilla.scripted_trigger_path, "00_rst_placeholder_triggers.txt" )
placeholder_scripted_triggers_file = open(placeholder_scripted_triggers_path,'w')
placeholder_scripted_triggers_file.write("")
placeholder_scripted_triggers_file.close()

master_scripted_effects_path = os.path.join( vanilla.scripted_effect_path, "00_rst_master_effects.txt" )
master_scripted_effects_file = open(master_scripted_effects_path,'w')
master_scripted_effects_file.write("")
master_scripted_effects_file.close()

master_scripted_triggers_path = os.path.join( vanilla.scripted_trigger_path, "00_rst_master_triggers.txt" )
master_scripted_triggers_file = open(master_scripted_triggers_path,'w')
master_scripted_triggers_file.write("")
master_scripted_triggers_file.close()


template_list = open("Templates2.txt",mode='r').read().split('\n\n<<<')
templates = { }
for template in template_list[1:]:
	template = template.split('>>>')
	templates[template[0]] = template[1]

exported_modifier_names_path = os.path.join('Autogenerated','exported_modifier_names.txt')
exported_modifier_names_file = open(exported_modifier_names_path,'w')
exported_modifier_names_file.write('')
exported_modifier_names_file.close()

for mod_key in mod_data:
	mod = mod_data[mod_key]
	if not mod.vanilla:
		placeholder_scripted_triggers_file = open(placeholder_scripted_triggers_path,'a')
		placeholder_scripted_triggers_file.write( "rst_has_{} = {{ always = no }}\n".format(mod.key) )
		placeholder_scripted_triggers_file.close()
		module_trigger_path = os.path.join( mod.scripted_trigger_path, 'z_rst_module_trigger_{}.txt'.format(mod.key) )
		module_trigger_file = open(module_trigger_path,'w')
		module_trigger_file.write( "rst_has_{} = {{ always = yes }}".format(mod.key) )
		module_trigger_file.close()
	for db_key in databases:
		db = databases[db_key]
		db.readFiles(mod)

for mod_key in mod_data:
	mod = mod_data[mod_key]
	for db_key in databases:
		db = databases[db_key]
		if db.top_level:
			db.processCW(
				mod_data[mod_key],
				db.getContents(mod),
				mod_key,
			)
	for db_key in databases:
		databases[db_key].checkWritten(mod)

master_scripted_effects_file = open(master_scripted_effects_path,'a')
master_scripted_triggers_file = open(master_scripted_triggers_path,'a')

for db_key in databases:
	print("generating master scripts for database {}".format(db_key))
	db = databases[db_key]
	if db.can_write:
		if db.reverse:
			db.master_inline_script_units.reverse()
			db.master_scripted_effect_units.reverse()
			db.master_scripted_trigger_units.reverse()
		master_inline_script_path = db.vanilla_inline_script_path+".txt"
		master_inline_script_file = open(master_inline_script_path,'w')
		master_inline_script_file.write(''.join(db.master_inline_script_units))
		master_inline_script_file.close()

		master_scripted_effects_file.write( master_scripted_effect_template.format(  db.singular, ''.join(db.master_scripted_effect_units ) ) )
		master_scripted_triggers_file.write( master_scripted_trigger_template.format( db.singular, ''.join(db.master_scripted_trigger_units) ) )

master_scripted_effects_file.close()
master_scripted_triggers_file.close()


	

	

logfile.close()