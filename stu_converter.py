import os
import re
from typing import Optional as Opt

triggers = {
	'has_ethic':{
		'ethic_gestalt_consciousness':'is_gestalt',
	},
	'is_country_type':{
		'default':'is_playable',
		True:None,
	},
	'has_authority':{
		'auth_machine_intelligence':'is_machine_empire',
		'auth_hive_mind':'is_hive_empire',
		'auth_corporate':'is_megacorp',
		'auth_democratic':'has_authority_democratic',
		'auth_oligarchic':'has_authority_oligarchic',
		'auth_dictatorial':'has_authority_dictatorial',
		'auth_imperial':'has_authority_imperial',
		True:None,
	},
	'has_origin':{
		'origin_default_pre_ftl':'has_default_pre_ftl_origin',
		'origin_default':'gets_prosperous_unification_bonus',
		'origin_subterranean':'is_subterranean_empire',
		'origin_lithoid':'is_calamitous_birth_empire',
		'origin_machine':'is_resource_consolidator_empire',
		'origin_necrophage':'is_current_or_former_necrophage_empire',
		'origin_hegemon':'is_hegemon_origin_empire',
		'origin_common_ground':'is_common_ground_empire',
		'origin_imperial_vassal_overlord':'is_vassal_origin_overlord',
		'origin_imperial_vassal':'has_imperial_vassal_origin',
		'origin_separatists':'is_separatist_empire',
		'origin_mechanists':'is_mechanist_empire',
		'origin_syncretic_evolution':'is_syncretic_evolution_empire',
		'origin_life_seeded':'is_life_seeded_empire',
		'origin_post_apocalyptic':'is_post_apocalyptic_empire',
		'origin_remnants':'is_remnants_empire',
		'origin_shattered_ring':'is_shattered_ring_empire',
		'origin_void_dwellers':'has_void_dweller_origin',
		'origin_scion':'is_scion_empire',
		'origin_galactic_doorstep':'is_galactic_doorstep_empire',
		'origin_tree_of_life':'is_tree_of_life_empire',
		'origin_shoulders_of_giants':'is_shoulders_of_giants_empire',
		'origin_doomsday':'is_doomsday_empire',
		'origin_lost_colony':'is_lost_colony_empire',
		'origin_clone_army':'is_clone_army_empire',
		'origin_here_be_dragons':'is_here_be_dragons_empire',
		'origin_ocean_paradise':'is_ocean_paradise_empire',
		'origin_progenitor_hive':'is_progenitor_hive_empire',
		'origin_star_slingshot':'is_star_slingshot_empire',
		'origin_shroudwalker_apprentice':'is_shroudwalker_apprentice_empire',
		'origin_overtuned':'is_overtuned_empire',
		'origin_toxic_knights':'is_toxic_knights_empire',
		'origin_fear_of_the_dark':'is_fear_of_the_dark_empire',
		'origin_payback':'is_payback_empire',
		'origin_broken_shackles':'is_broken_shackles_empire',
		'origin_fruitful':'is_fruitful_empire',
		'origin_riftworld':'is_riftworld_empire',
		'origin_enlightened':'is_enlightened_empire',
		'origin_slavers':'is_minamar',
		True:None,
	},
	'has_civic':{
		'civic_reanimated_armies':'has_reanimated_armies',
		'civic_permanent_employment':'has_permanent_employment',
		'civic_inwards_perfection':'is_inwards_perfection_empire',
		'civic_barbaric_despoilers':'is_despoiler_empire',
		'civic_agrarian_idyll':'is_agrarian_empire',
		'civic_aristocratic_elite':'is_aristocratic_empire',
		'civic_shared_burden':'is_shared_burden_empire',
		'civic_environmentalist':'is_environmentalist_empire',
		'civic_gospel_of_the_masses':'is_megachurch_empire',
		'civic_machine_assimilator':'is_machine_assimilator',
		'civic_citizen_service':'has_citizen_service',
		'civic_franchising':'is_franchise',
		'civic_hive_cordyceptic_drones':'is_cordyceptic_empire',
		'civic_pompous_purists':'is_pompous_empire',
		'civic_feudal_realm':'is_feudal_empire',
		'civic_technocracy':'is_technocracy',
		'civic_exalted_priesthood':'has_exalted_priesthood',
		'civic_warrior_culture':'has_warrior_culture',
		'civic_hive_natural_neural_network':'has_natural_neural_network',
		'civic_efficient_bureaucracy':'has_efficient_bureaucracy',
		'civic_byzantine_bureaucracy':'has_byzantine_bureaucracy',
		'civic_machine_maintenance_protocols':'has_maintenance_protocols',
		'civic_dystopian_society':'has_dystopian_society',
		'civic_private_healthcare_corporate':'is_private_healthcare_empire',
		'civic_crusader_spirit_corporate':'is_privateer_empire',
		'civic_crusader_spirit':'has_crusader_spirit',
		'civic_parliamentary_system':'has_parliamentary_system',
		'civic_heroic_tales':'has_heroic_tales',
		'civic_philosopher_king':'has_philosopher_king',
		'civic_machine_servitor':'is_servitor_empire',
		'civic_void_hive':'is_void_hive_empire',
		'civic_selective_kinship':'is_selective_kinship_empire',
		True:None,
	},
	'has_valid_civic':{
		'civic_reanimated_armies':'has_reanimated_armies',
		'civic_permanent_employment':'has_permanent_employment',
		'civic_inwards_perfection':'is_inwards_perfection_empire',
		'civic_barbaric_despoilers':'is_despoiler_empire',
		'civic_agrarian_idyll':'is_agrarian_empire',
		'civic_aristocratic_elite':'is_aristocratic_empire',
		'civic_shared_burden':'is_shared_burden_empire',
		'civic_environmentalist':'is_environmentalist_empire',
		'civic_gospel_of_the_masses':'is_megachurch_empire',
		'civic_machine_assimilator':'is_machine_assimilator',
		'civic_citizen_service':'has_citizen_service',
		'civic_franchising':'is_franchise',
		'civic_hive_cordyceptic_drones':'is_cordyceptic_empire',
		'civic_pompous_purists':'is_pompous_empire',
		'civic_feudal_realm':'is_feudal_empire',
		'civic_technocracy':'is_technocracy',
		'civic_exalted_priesthood':'has_exalted_priesthood',
		'civic_warrior_culture':'has_warrior_culture',
		'civic_hive_natural_neural_network':'has_natural_neural_network',
		'civic_efficient_bureaucracy':'has_efficient_bureaucracy',
		'civic_byzantine_bureaucracy':'has_byzantine_bureaucracy',
		'civic_machine_maintenance_protocols':'has_maintenance_protocols',
		'civic_dystopian_society':'has_dystopian_society',
		'civic_private_healthcare_corporate':'is_private_healthcare_empire',
		'civic_crusader_spirit_corporate':'is_privateer_empire',
		'civic_crusader_spirit':'has_crusader_spirit',
		'civic_parliamentary_system':'has_parliamentary_system',
		'civic_heroic_tales':'has_heroic_tales',
		'civic_philosopher_king':'has_philosopher_king',
		'civic_machine_servitor':'is_servitor_empire',
		'civic_void_hive':'is_void_hive_empire',
		'civic_selective_kinship':'is_selective_kinship_empire',
		True:None,
	},
	'is_planet_class':{
		'pc_city':'is_city_world',
		'pc_habitat':'is_habitat',
		'pc_shattered_ring_habitable':'is_shattered_ring_habitable',
		'pc_ringworld_habitable_damaged':'is_damaged_ring_segment',
		'pc_ringworld_habitable':'is_unshattered_ring_habitable_segment',
		'pc_gaia':'is_gaia_world',
		'pc_hive':'is_hive_world',
		'pc_machine':'is_machine_world',
		'pc_nuked':'is_nuked_world',
		'pc_relic':'is_relic_world',
		'pc_continental':'is_continental_world',
		'pc_tropical':'is_tropical_world',
		'pc_ocean':'is_ocean_world',
		'pc_desert':'is_desert_world',
		'pc_arid':'is_arid_world',
		'pc_savannah':'is_savannah_world',
		'pc_arctic':'is_arctic_world',
		'pc_tundra':'is_tundra_world',
		'pc_alpine':'is_alpine_world',
		'pc_gas_giant':'is_gas_giant',
		'pc_toxic':'is_toxic_world',
		'pc_frozen':'is_frozen_world',
		'pc_barren_cold':'is_barren_cold_world',
		'pc_barren':'is_barren_dry_world',
		'pc_molten':'is_molten_world',
		'pc_ice_asteroid':'is_ice_asteroid',
		'pc_rare_crystal_asteroid':'is_rare_crystal_asteroid',
		'pc_asteroid':'is_rocky_asteroid',
		'pc_broken':'is_broken_world',
		'pc_shattered':'is_shattered_world',
		'pc_gray_goo':'is_gray_goo_world',
		'pc_infested':'is_infested_world',
		'pc_shrouded':'is_shrouded_world',
		'pc_black_hole':'planet_is_black_hole',
		True:None,
	},
}
substitution_patterns = {
	'NOT = {{ {} = {} }}':'{} = no',
	'NOT = {{ {} = "{}" }}':'{} = no',
	'{} = {}':'{} = yes',
	'{} = "{}"':'{} = yes',
}
substitution_patterns_allow_invalid = {
	'{} = {}':'{} = {{ allow_invalid = yes }}',
	'{} = "{}"':'{} = {{ allow_invalid = yes }}',
}
inline_substituation_patterns = {
	"""ethics = { NOT = { value = ethic_gestalt_consciousness } }
		authority = { NOT = { value = auth_corporate } }""":"governments/conditions/is_regular",
	"""authority = { value = auth_hive_mind }""":"governments/conditions/is_hive",
	"""authority = { value = auth_machine_intelligence }""":"governments/conditions/is_machine",
	"""OR = {
			authority = { value = auth_corporate }
			civics = { value = civic_galactic_sovereign_megacorp }
		}""":"governments/conditions/is_corporate",
}
flag_patterns = [
	'damage_vs_player_crisis_mult',
	'construction_type = starbase_defenses',
	'job_[^ \n]*_add',
	'pc_[^ \n]*_habitability',
	'has_modifier = flooded_habitat',
	'spawn_planet',
]

class stu_path():
	def __init__( self, parent=None, name:Opt[str]=None, vanilla_path:Opt[str]=None, stu_path:Opt[str]=None ) -> None:
		self.name=name
		self.parent=parent
		if self.parent is not None:
			self.vanilla_path = os.path.join( self.parent.vanilla_path, self.name )
			self.stu_path = os.path.join( self.parent.stu_path, self.name )
		else:
			self.vanilla_path = vanilla_path
			self.stu_path = stu_path
	
	def process(self):
		if os.path.isdir(self.vanilla_path):
			self.is_dir=True
			for entry in os.listdir(self.vanilla_path):
				entry_stup = stu_path(self,entry)
				entry_stup.process()
		elif self.name.endswith('.txt') and not self.name.endswith('ThirdPartyLicenses.txt'):
			self.is_dir=False
			# print(self.vanilla_path)
			file = open(self.vanilla_path,'r',encoding='UTF-8')
			self.text = file.read()
			file.close()
			self.process_text()

	def write(self):
		if self.parent is not None:
			self.parent.write()
		if self.is_dir:
			if not os.path.exists(self.stu_path):
				os.mkdir(self.stu_path)
		else:
			file = open(self.stu_path,'w',encoding='UTF-8')
			file.write(self.text)
			file.close()

	
	def process_text(self):
		should_write = False
		for trigger in triggers:
			for value in triggers[trigger]:
				if value is True:
					if trigger in self.text:
						print( f"found pattern {trigger} in file {self.vanilla_path}" )
						should_write = True
				elif trigger == 'has_civic' and self.parent.name == 'events':
					substitute_trigger = triggers[trigger][value]
					for pattern in substitution_patterns_allow_invalid:
						f = pattern.format( trigger, value )
						r = substitution_patterns_allow_invalid[pattern].format( substitute_trigger )
						if f in self.text:
							print( f"found pattern {f} in file {self.vanilla_path}" )
							should_write = True
							self.text = self.text.replace(f,r)
				else:
					substitute_trigger = triggers[trigger][value]
					for pattern in substitution_patterns:
						f = pattern.format( trigger, value )
						r = substitution_patterns[pattern].format( substitute_trigger )
						if f in self.text:
							print( f"found pattern {f} in file {self.vanilla_path}" )
							should_write = True
							self.text = self.text.replace(f,r)
		for f in inline_substituation_patterns:
			if f in self.text:
				print( f"found pattern {f} in file {self.vanilla_path}" )
				should_write = True
				r = 'inline_script = "{}"'.format( inline_substituation_patterns[f] )
				self.text = self.text.replace(f,r)
		for pattern in flag_patterns:
			if re.match( pattern, self.text ):
				print( f"found pattern {pattern} in file {self.vanilla_path}" )
				should_write=True
		if should_write:
			self.write()
		

root = stu_path(
	vanilla_path="C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stellaris",
	stu_path="C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod\\scripted_trigger_undercoat"
	# stu_path="C:\\Users\\kuyan\\OneDrive\\Desktop\\mod stuff\\stu_test_output"
)
root.process()