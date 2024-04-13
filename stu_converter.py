import os
import re
from typing import Optional as Opt
from shutil import rmtree

### DATA FOR REGULAR SUBSTITUTIONS ###

triggers = [
	('has_ethic',[
		('ethic_gestalt_consciousness','is_gestalt'),
	]),
	('is_country_type',[
		(['default','fallen_empire','awakened_fallen_empire'],'is_empire'),
		(['default','awakened_fallen_empire','fallen_empire'],'is_empire'),
		(['fallen_empire','awakened_fallen_empire'],'is_fallen_empire'),
		(['awakened_fallen_empire','fallen_empire'],'is_fallen_empire'),
		(['extradimensional','extradimensional_2','extradimensional_3','swarm','ai_empire'],'is_endgame_crisis'),
		(['swarm','extradimensional','extradimensional_2','extradimensional_3','ai_empire'],'is_endgame_crisis'),
		('default','is_playable'),
		(True,None),
	]),
	('is_species_class',[
		(['FUN','PLANT'],'is_flora_species'),
		(['PLANT','FUN'],'is_flora_species'),
		(True,None),
	]),
	('has_authority',[
		('auth_machine_intelligence','is_machine_empire'),
		('auth_hive_mind','is_hive_empire'),
		('auth_corporate','is_megacorp'),
		('auth_democratic','has_authority_democratic'),
		('auth_oligarchic','has_authority_oligarchic'),
		('auth_dictatorial','has_authority_dictatorial'),
		('auth_imperial','has_authority_imperial'),
		(True,None),
	]),
	('has_origin',[
		(['origin_common_ground','origin_hegemon'],'has_federation_origin'),
		('origin_default_pre_ftl','has_default_pre_ftl_origin'),
		('origin_default','gets_prosperous_unification_bonus'),
		('origin_subterranean','is_subterranean_empire'),
		('origin_lithoid','is_calamitous_birth_empire'),
		('origin_machine','is_resource_consolidator_empire'),
		('origin_necrophage','is_current_or_former_necrophage_empire'),
		('origin_hegemon','is_hegemon_origin_empire'),
		('origin_common_ground','is_common_ground_empire'),
		('origin_imperial_vassal_overlord','is_vassal_origin_overlord'),
		('origin_imperial_vassal','has_imperial_vassal_origin'),
		('origin_separatists','is_separatist_empire'),
		('origin_mechanists','is_mechanist_empire'),
		('origin_syncretic_evolution','is_syncretic_evolution_empire'),
		('origin_life_seeded','is_life_seeded_empire'),
		('origin_post_apocalyptic','is_post_apocalyptic_empire'),
		('origin_remnants','is_remnants_empire'),
		('origin_shattered_ring','is_shattered_ring_empire'),
		('origin_void_dwellers','has_void_dweller_origin'),
		('origin_scion','is_scion_empire'),
		('origin_galactic_doorstep','is_galactic_doorstep_empire'),
		('origin_tree_of_life','is_tree_of_life_empire'),
		('origin_shoulders_of_giants','is_shoulders_of_giants_empire'),
		('origin_doomsday','is_doomsday_empire'),
		('origin_lost_colony','is_lost_colony_empire'),
		('origin_clone_army','is_clone_army_empire'),
		('origin_here_be_dragons','is_here_be_dragons_empire'),
		('origin_ocean_paradise','is_ocean_paradise_empire'),
		('origin_progenitor_hive','is_progenitor_hive_empire'),
		('origin_star_slingshot','is_star_slingshot_empire'),
		('origin_shroudwalker_apprentice','is_shroudwalker_apprentice_empire'),
		('origin_overtuned','is_overtuned_empire'),
		('origin_toxic_knights','is_toxic_knights_empire'),
		('origin_fear_of_the_dark','is_fear_of_the_dark_empire'),
		('origin_payback','is_payback_empire'),
		('origin_broken_shackles','is_broken_shackles_empire'),
		('origin_fruitful','is_fruitful_empire'),
		('origin_riftworld','is_riftworld_empire'),
		('origin_enlightened','is_enlightened_empire'),
		('origin_slavers','is_minamar'),
		(True,None),
	]),
	(['has_civic','has_valid_civic'],[
		(['civic_fanatic_purifiers','civic_machine_terminator','civic_hive_devouring_swarm'],'is_homicidal'),
		(['civic_fanatic_purifiers','civic_hive_devouring_swarm','civic_machine_terminator'],'is_homicidal'),
		(['civic_hive_devouring_swarm','civic_fanatic_purifiers','civic_machine_terminator'],'is_homicidal'),
		(['civic_machine_terminator','civic_hive_devouring_swarm','civic_fanatic_purifiers'],'is_homicidal'),
		(['civic_eager_explorers','civic_privatized_exploration','civic_hive_stargazers','civic_machine_exploration_protocol'],'is_eager_explorer_empire'),
		(['civic_pleasure_seekers','civic_corporate_hedonism'],'is_pleasure_seeker'),
		(['civic_crafters','civic_corporate_crafters'],'is_crafter_empire'),
		(['civic_corporate_crafters','civic_crafters'],'is_crafter_empire'),
		(['civic_anglers','civic_corporate_anglers'],'is_anglers_empire'),
		(['civic_catalytic_processing','civic_corporate_catalytic_processing','civic_hive_catalytic_processing','civic_machine_catalytic_processing'],'is_catalytic_empire'),
		(['civic_catalytic_processing','civic_hive_catalytic_processing','civic_machine_catalytic_processing','civic_corporate_catalytic_processing'],'is_catalytic_empire'),
		(['civic_idyllic_bloom','civic_hive_idyllic_bloom','civic_life_seeded'],'is_idyllic_bloom_empire'),
		(['civic_idyllic_bloom','civic_hive_idyllic_bloom'],'is_idyllic_bloom_empire'),
		(['civic_death_cult','civic_death_cult_corporate'],'is_death_cult_empire'),
		(['civic_memorialist','civic_hive_memorialist','civic_machine_memorialist'],'is_memorialist_empire'),
		(['civic_memorialist','civic_machine_memorialist','civic_hive_memorialist'],'is_memorialist_empire'),
		(['civic_relentless_industrialists','civic_corporate_relentless_industrialists'],'is_relentless_industrialist_empire'),
		(['civic_toxic_baths','civic_corporate_toxic_baths','civic_hive_toxic_baths','civic_machine_toxic_baths'],'has_toxic_baths'),
		(['civic_scavengers','civic_corporate_scavengers'],'is_scavenger'),
		(['civic_memory_vault','civic_memory_vault_corporate','civic_memory_vault_machine','civic_memory_vault_hive'],'is_memory_vault_empire'),
		(['civic_ascensionists','civic_corporate_ascensionists','civic_hive_ascensionists','civic_machine_ascensionists'],'is_ascensionist_empire'),
		(['civic_slaver_guilds','civic_indentured_assets'],'has_slaver_civic'),
		(['civic_indentured_assets','civic_slaver_guilds'],'has_slaver_civic'),
		(['civic_dimensional_worship','civic_corporate_dimensional_worship'],'is_dimensional_worship_empire'),
		('civic_reanimated_armies','has_reanimated_armies'),
		('civic_permanent_employment','has_permanent_employment'),
		('civic_inwards_perfection','is_inwards_perfection_empire'),
		('civic_barbaric_despoilers','is_despoiler_empire'),
		('civic_agrarian_idyll','is_agrarian_empire'),
		('civic_aristocratic_elite','is_aristocratic_empire'),
		('civic_shared_burden','is_shared_burden_empire'),
		('civic_environmentalist','is_environmentalist_empire'),
		('civic_gospel_of_the_masses','is_megachurch_empire'),
		('civic_machine_assimilator','is_machine_assimilator'),
		('civic_citizen_service','has_citizen_service'),
		('civic_franchising','is_franchise'),
		('civic_hive_cordyceptic_drones','is_cordyceptic_empire'),
		('civic_pompous_purists','is_pompous_empire'),
		('civic_feudal_realm','is_feudal_empire'),
		('civic_technocracy','is_technocracy'),
		('civic_exalted_priesthood','has_exalted_priesthood'),
		('civic_warrior_culture','has_warrior_culture'),
		('civic_hive_natural_neural_network','has_natural_neural_network'),
		('civic_efficient_bureaucracy','has_efficient_bureaucracy'),
		('civic_byzantine_bureaucracy','has_byzantine_bureaucracy'),
		('civic_machine_maintenance_protocols','has_maintenance_protocols'),
		('civic_dystopian_society','has_dystopian_society'),
		('civic_private_healthcare_corporate','is_private_healthcare_empire'),
		('civic_crusader_spirit_corporate','is_privateer_empire'),
		('civic_crusader_spirit','has_crusader_spirit'),
		('civic_parliamentary_system','has_parliamentary_system'),
		('civic_heroic_tales','has_heroic_tales'),
		('civic_philosopher_king','has_philosopher_king'),
		('civic_machine_servitor','is_servitor_empire'),
		('civic_void_hive','is_void_hive_empire'),
		('civic_selective_kinship','is_selective_kinship_empire'),
		(True,None),
	]),
	('is_planet_class',[
		(['pc_desert','pc_tropical','pc_arid','pc_continental','pc_ocean','pc_tundra','pc_arctic','pc_alpine','pc_savannah'],'is_starting_planet_type'),
		(['pc_desert','pc_tropical','pc_continental','pc_ocean','pc_arctic','pc_tundra','pc_arid','pc_alpine','pc_savannah'],'is_starting_planet_type'),
		(['pc_molten','pc_barren','pc_barren_cold','pc_toxic','pc_frozen'],'uninhabitable_regular_planet'),
		(['pc_shielded','pc_ringworld_shielded','pc_habitat_shielded'],'is_shielded'),
		(['pc_shattered','pc_shattered_2'],'is_shattered_world'),
		(['pc_neutron_star','pc_pulsar','pc_black_hole'],'planet_is_nonstandard_star'),
		(['pc_neutron_star','pc_pulsar'],'planet_is_neutron_star_including_pulsar'),
		(['pc_pulsar','pc_neutron_star'],'planet_is_neutron_star_including_pulsar'),
		('pc_city','is_city_world'),
		('pc_habitat','is_habitat'),
		('pc_shattered_ring_habitable','is_shattered_ring_habitable'),
		('pc_ringworld_habitable_damaged','is_damaged_ring_segment'),
		('pc_ringworld_habitable','is_unshattered_ring_habitable_segment'),
		('pc_gaia','is_gaia_world'),
		('pc_hive','is_hive_world'),
		('pc_machine','is_machine_world'),
		('pc_nuked','is_nuked_world'),
		('pc_relic','is_relic_world'),
		('pc_continental','is_continental_world'),
		('pc_tropical','is_tropical_world'),
		('pc_ocean','is_ocean_world'),
		('pc_desert','is_desert_world'),
		('pc_arid','is_arid_world'),
		('pc_savannah','is_savannah_world'),
		('pc_arctic','is_arctic_world'),
		('pc_tundra','is_tundra_world'),
		('pc_alpine','is_alpine_world'),
		('pc_gas_giant','is_gas_giant'),
		('pc_toxic','is_toxic_world'),
		('pc_frozen','is_frozen_world'),
		('pc_barren_cold','is_barren_cold_world'),
		('pc_barren','is_barren_dry_world'),
		('pc_molten','is_molten_world'),
		('pc_ice_asteroid','is_ice_asteroid'),
		('pc_rare_crystal_asteroid','is_rare_crystal_asteroid'),
		('pc_asteroid','is_rocky_asteroid'),
		('pc_broken','is_broken_world'),
		('pc_gray_goo','is_gray_goo_world'),
		('pc_infested','is_infested_world'),
		('pc_shrouded','is_shrouded_world'),
		('pc_black_hole','planet_is_black_hole'),
		(True,None),
	]),
]
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
	r'job_[^ \n]*_add',
	r'pc_[^ \n]*_habitability',
	'has_modifier = flooded_habitat',
	'spawn_planet',
]

ethic_opposites = {
	'authoritarian':'egalitarian',
	'xenophobe':'xenophile',
	'militarist':'pacifist',
	'spiritualist':'materialist',
	'egalitarian':'authoritarian',
	'xenophile':'xenophobe',
	'pacifist':'militarist',
	'materialist':'spiritualist',
}

### SUBSTITUTION-GENERATING SCRIPT ###

class substitution():
	def __init__( self, f, r=None, tag=None, folder=None, preserve_whitespace=False ) -> None:
		if not preserve_whitespace:
			# allow arbitrary whitespace
			f = f.replace('{',r'\{').replace('}',r'\}').replace(' ',r'[\s\n]+').replace('\n',r'[\s\n]+').replace('\t','')
		self.f = f
		self.r = r
		self.folder = folder
		self.tag = tag

substitutions = []

def add_substitution( f, r=None, tag=None, folder=None, preserve_whitespace=False ):
	print("adding substitution:")
	print(f)
	substitutions.append( substitution( f=f, r=r, tag=tag, folder=folder, preserve_whitespace=preserve_whitespace ) )

def apply_substitution_pattern( triggers, values, substitute_trigger, substitute_trigger_value, unit_pattern="{} = \"?{}\"?", master_pattern = "{}", interspersed=False, tag=None, folder=None ):
	units = []
	for i in range( len(values) ):
		value = values[i]
		if type(triggers) == list:
			trigger = triggers[i]
		else:
			trigger = triggers
		units.append( unit_pattern.format( trigger, value ) )
	if interspersed:
		join_str = r"([\s\n](?:[^{}]|\n)*[\s\n])" # capture separating clauses
	else:
		join_str = ' '
	inner = join_str.join( units )
	f = master_pattern.format(inner)
	r = f"{substitute_trigger} = {substitute_trigger_value}#!stu_tag!#" # tag for later comment-adding
	capture_groups = 1
	if interspersed:
		while capture_groups < len(values):
			r += "\\"+str(capture_groups)
			capture_groups += 1
	add_substitution( f=f, r=r, tag=tag, folder=folder )

def add_or_context_substitution_patterns( triggers, values, substitute_trigger, tag ):
	apply_substitution_pattern( triggers, values, substitute_trigger, 'no', unit_pattern="{} = \"?{}\"?", master_pattern="NOR = {{ {} }}" , tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'yes', unit_pattern="{} = \"?{}\"?", master_pattern="OR = {{ {} }}" , tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'no', unit_pattern="NOT = {{ {} = \"?{}\"? }}", interspersed=True, tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'yes', unit_pattern="{} = \"?{}\"?", interspersed=True, tag=tag )

def add_and_context_substitution_patterns( triggers, values, substitute_trigger, tag ):
	apply_substitution_pattern( triggers, values, substitute_trigger, 'no', unit_pattern="{} = \"?{}\"?", master_pattern="NAND = {{ {} }}" , tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'yes', unit_pattern="{} = \"?{}\"?", master_pattern="AND = {{ {} }}" , tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'no', unit_pattern="NOT = {{ {} = \"?{}\"? }}", interspersed=True, tag=tag )
	apply_substitution_pattern( triggers, values, substitute_trigger, 'yes', unit_pattern="{} = \"?{}\"?", interspersed=True, tag=tag )




### ADD SUBSTITUTIONS ###

# is_necrophage_empire
add_and_context_substitution_patterns(
	triggers=['has_origin','has_trait'],
	values=['origin_necrophage','trait_necrophage'],
	substitute_trigger='is_necrophage_empire',
	tag="undercoat: moved to scripted trigger"
)
# is_necrophage_empire
add_and_context_substitution_patterns(
	triggers=['has_trait','has_origin'],
	values=['trait_necrophage','origin_necrophage'],
	substitute_trigger='is_necrophage_empire',
	tag="undercoat: moved to scripted trigger"
)
# $|from$
add_substitution(
	f = "from",
	r = "$country|from$",
	file = 'scripted_triggers'
)
# $|from$
add_substitution(
	f = "root",
	r = "$country|root$",
	file = 'scripted_triggers'
)
# damage_vs_crisis_mult
add_substitution(
	f = """damage_vs_country_type_swarm_mult = ([\\d\\.]+)
		damage_vs_country_type_extradimensional_mult = \\1
		damage_vs_country_type_extradimensional_2_mult = \\1
		damage_vs_country_type_extradimensional_3_mult = \\1
		damage_vs_country_type_ai_empire_mult = \\1
		damage_vs_country_type_gray_goo_mult = \\1
		damage_vs_player_crisis_mult = \\1""",
	r = "damage_vs_crisis_mult = \\1#!stu_tag!#",
	tag = "undercoat: moved to static modifier"
)
# jobs/triggered/researcher_add
add_substitution(
	f = """triggered_planet_modifier = {
			potential = {
				exists = owner
				owner = { is_regular_empire = yes }
			}
			modifier = {
				job_researcher_add = (\\d+)
			}
		}
		triggered_planet_modifier = {
			potential = {
				exists = owner
				owner = { is_hive_empire = yes }
			}
			modifier = {
				job_brain_drone_add = \\1
			}
		}
		triggered_planet_modifier = {
			potential = {
				exists = owner
				owner = { is_machine_empire = yes }
			}
			modifier = {
				job_calculator_add = \\1
			}
		}""",
	r = """# undercoat: moved to inline script
	inline_script = {
		script = jobs/triggered/researchers_add
		AMOUNT = \\1
		desc = 0
		trigger = " "
		mult_line = " "
	}""",
	folder = 'deposits'
)
# homicidal_diplomacy_restrictions = { mirror = yes }
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				NOT = { has_valid_civic = civic_fanatic_purifiers }
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				from = { NOT = { has_valid_civic = civic_fanatic_purifiers } }
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_devouring_swarm"
			NOT = { has_valid_civic = civic_hive_devouring_swarm }
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_devouring_swarm"
			from = { NOT = { has_valid_civic = civic_hive_devouring_swarm } }
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_machine_terminator"
			OR = {
				is_same_species = from
				NOT = { has_civic = civic_machine_terminator }
				AND = {
					has_civic = civic_machine_terminator
					from = {
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_machine_terminator"
			OR = {
				is_same_species = from
				from = { NOT = { has_civic = civic_machine_terminator } }
				AND = {
					from = { has_civic = civic_machine_terminator }
					OR = {
						has_country_flag = synthetic_empire
						has_authority = auth_machine_intelligence
					}
				}
			}
		}""",
	r = "homicidal_diplomacy_restrictions = { mirror = yes } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# homicidal_diplomacy_restrictions_no_exception = { mirror = yes }
add_substitution(
	f = """possible = {
		custom_tooltip = {
			fail_text = "requires_actor_not_fanatic_purifiers"
			NOT = { has_valid_civic = civic_fanatic_purifiers	}
		}
		custom_tooltip = {
			fail_text = "requires_recipient_not_fanatic_purifiers"
			from = { NOT = { has_valid_civic = civic_fanatic_purifiers } }
		}
		custom_tooltip = {
			fail_text = "requires_actor_not_devouring_swarm"
			NOT = { has_valid_civic = civic_hive_devouring_swarm }
		}
		custom_tooltip = {
			fail_text = "requires_recipient_not_devouring_swarm"
			from = { NOT = { has_valid_civic = civic_hive_devouring_swarm } }
		}
		custom_tooltip = {
			fail_text = "requires_actor_not_machine_terminator"
			OR = {
				is_same_species = from
				NOT = { has_civic = civic_machine_terminator }
				AND = {
					has_civic = civic_machine_terminator
					from = {
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		}
		custom_tooltip = {
			fail_text = "requires_recipient_not_machine_terminator"
			OR = {
				is_same_species = from
				from = { NOT = { has_civic = civic_machine_terminator } }
				AND = {
					from = { has_civic = civic_machine_terminator }
					OR = {
						has_country_flag = synthetic_empire
						has_authority = auth_machine_intelligence
					}
				}
			}
		}""",
	r = "homicidal_diplomacy_restrictions_no_exception = { mirror = yes } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# homicidal_diplomacy_restrictions = { mirror_with_intel = yes }
add_substitution(
	f = """if = {
			limit = { from = { has_valid_civic = civic_fanatic_purifiers } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_fanatic_purifiers
					OR = {
						is_same_species = from
						from = { NOT = { has_valid_civic = civic_fanatic_purifiers } }
					}
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					OR = {
						is_same_species = from
						NOT = { has_valid_civic = civic_fanatic_purifiers }
					}
				}
			}
		}

		if = {
			limit = { from = { has_valid_civic = civic_hive_devouring_swarm } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_devouring_swarm
					always = no
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					always = no
				}
			}
		}

		if = {
			limit = { from = { has_valid_civic = civic_machine_terminator } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_machine_terminator
					AND = {
						from = { has_civic = civic_machine_terminator }
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					AND = {
						from = { has_civic = civic_machine_terminator }
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		}

		custom_tooltip = {
			fail_text = "requires_actor_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				NOT = { has_valid_civic = civic_fanatic_purifiers }
			}
		}

		custom_tooltip = {
			fail_text = "requires_actor_not_devouring_swarm"
			NOT = { has_valid_civic = civic_hive_devouring_swarm }
		}

		custom_tooltip = {
			fail_text = "requires_actor_not_machine_terminator"
			OR = {
				is_same_species = from
				NOT = { has_civic = civic_machine_terminator }
				AND = {
					has_civic = civic_machine_terminator
					from = {
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		}""",
	r = "homicidal_diplomacy_restrictions = { mirror_with_intel = yes } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# homicidal_diplomacy_restrictions = { mirror = no }
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				NOT = { has_valid_civic = civic_fanatic_purifiers }
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_devouring_swarm"
			NOT = { has_valid_civic = civic_hive_devouring_swarm }
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_machine_terminator"
			OR = {
				is_same_species = from
				NOT = { has_civic = civic_machine_terminator }
				AND = {
					has_civic = civic_machine_terminator
					from = {
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		}""",
	r = "homicidal_diplomacy_restrictions = { mirror = no } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# interspersed homicidal/purifier restrictions
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				NOT = { has_valid_civic = civic_fanatic_purifiers }
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_fanatic_purifiers"
			OR = {
				is_same_species = from
				from = { NOT = { has_valid_civic = civic_fanatic_purifiers } }
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_devouring_swarm"
			NOT = { has_valid_civic = civic_hive_devouring_swarm }
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_devouring_swarm"
			from = { NOT = { has_valid_civic = civic_hive_devouring_swarm } }
		} (#.*)?
		if = {
			limit = { from = { has_valid_civic = civic_inwards_perfection } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_inward_perfection
					always = no
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					always = no
				}
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_inward_perfection"
			NOT = { has_valid_civic = civic_inwards_perfection }
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_actor_not_machine_terminator"
			OR = {
				is_same_species = from
				NOT = { has_civic = civic_machine_terminator }
				AND = {
					has_civic = civic_machine_terminator
					from = {
						OR = {
							has_country_flag = synthetic_empire
							has_authority = auth_machine_intelligence
						}
					}
				}
			}
		} (#.*)?
		custom_tooltip = {
			fail_text = "requires_recipient_not_machine_terminator"
			OR = {
				is_same_species = from
				from = { NOT = { has_civic = civic_machine_terminator } }
				AND = {
					from = { has_civic = civic_machine_terminator }
					OR = {
						has_country_flag = synthetic_empire
						has_authority = auth_machine_intelligence
					}
				}
			}
		}""",
	r = """homicidal_diplomacy_restrictions = { mirror = yes } # Undercoat scripted trigger
		inwards_perfection_diplomacy_restrictions = { mirror_with_intel = yes } # Undercoat scripted trigger""",
	folder = 'diplomatic_actions'
)
# machine_assimilator_diplomacy_restrictions = { mirror = no }
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_machine_assimilator"
			NOT = { has_valid_civic = civic_machine_assimilator }
		}""",
	r = "machine_assimilator_diplomacy_restrictions = { mirror = no } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# inwards_perfection_diplomacy_restrictions = { mirror_with_intel = yes }
add_substitution(
	f = """if = {
			limit = { from = { has_valid_civic = civic_inwards_perfection } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_inward_perfection
					always = no
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					always = no
				}
			}
		}
		custom_tooltip = {
			fail_text = "requires_actor_not_inward_perfection"
			NOT = { has_valid_civic = civic_inwards_perfection }
		}""",
	r = "inwards_perfection_diplomacy_restrictions = { mirror_with_intel = yes } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# inwards_perfection_diplomacy_restrictions = { mirror = no }
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_inward_perfection"
			NOT = { has_valid_civic = civic_inwards_perfection }
		}""",
	r = "inwards_perfection_diplomacy_restrictions = { mirror = no } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# pompous_diplomacy_restrictions
add_substitution(
	f = """if = {
			limit = {
				from = { has_valid_civic = civic_pompous_purists }
				NOT = { root = { is_overlord_to = from } }
			}
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_pompous
					always = no
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					always = no
				}
			}
		}""",
	r = "pompous_diplomacy_restrictions = yes # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# pompous_sender_diplomacy_restrictions
add_substitution(
	f = """custom_tooltip = {
			fail_text = "requires_actor_not_pompous"
			NOT = { has_valid_civic = civic_pompous_purists }
		}""",
	r = "pompous_sender_diplomacy_restrictions = yes # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# barbaric_despoilers_diplomacy_restrictions = { mirror_with_intel = yes }
add_substitution(
	f = """if = {
			limit = { from = { has_valid_civic = civic_barbaric_despoilers } }
			if = {
				limit = {
					has_intel = {
						who = from
						intel = civics
					}
				}
				custom_tooltip = {
					fail_text = requires_recipient_not_barbaric_despoilers
					always = no
				}
			}
			else = {
				custom_tooltip = {
					fail_text = diplo_action_no_low_intel
					always = no
				}
			}
		}
		custom_tooltip = {
			fail_text = "requires_actor_not_barbaric_despoilers"
			NOT = { has_valid_civic = civic_barbaric_despoilers }
		}""",
	r = "barbaric_despoilers_diplomacy_restrictions = { mirror_with_intel = yes } # Undercoat scripted trigger",
	folder = 'diplomatic_actions'
)
# barbaric_despoilers_diplomacy_restrictions = { mirror = no }
add_substitution(
	f = """custom_tooltip = {
			fail_text = requires_actor_not_barbaric_despoilers
			NOT = { has_valid_civic = civic_barbaric_despoilers }
		}""",
	r = "barbaric_despoilers_diplomacy_restrictions = { mirror = no } # Undercoat scripted trigger",
	folder = 'federation_types'
)
# standard faction actions
add_substitution(
	f = """embrace_faction = {
			title = "EMBRACE_FACTION"
			description = "EMBRACE_FACTION_DESC"

			cost = {
				unity = 5000
			}

			potential = {
				exists = owner
				owner = {
					OR = {
						is_subject = no
						NOT = { any_agreement = { agreement_preset = preset_dominion } }
					}
				}
			}

			valid = {
				custom_tooltip = {
					fail_text = EMBRACE_FACTION_COOLDOWN
					parameter:empire = {
						NOT = { has_modifier = embraced_faction_timer }
					}
				}
				support > 0.20
				parameter:empire = {
					NOT = { has_ethic = "ethic_fanatic_([^ \\t]+)" }
				}
			}

			effect = {
				add_modifier = { modifier = embraced_faction days = 3600 }
				parameter:empire = {
					shift_ethic = ethic_\\1
					hidden_effect = {
						add_modifier = { modifier = embraced_faction_timer days = 3600 }
						every_pop_faction = {
							limit = { NOT = { is_same_value = root } }
							add_modifier = { modifier = embraced_another_faction days = 3600 }
						}
					}
				}
				hidden_effect = {
					save_event_target_as = TargetFaction
					parameter:empire = {
						every_relation = {
							limit = {
								is_ai = no
								is_country_type = default
								has_communications = prev
								has_intel_level = {
									who = prev
									category = government
									level >= 1
								}
							}
							country_event = { id = factions.2000 }
						}
					}
				}
			}

			ai_weight = {
				base = 1
				modifier = {
					factor = 0
					support < 0.50
					owner = {
						has_ethic = ethic_\\1
					}
				}
				modifier = {
					factor = 0
					owner = { has_valid_civic = civic_fanatic_purifiers }
				}
				modifier = {
					factor = 0
					owner = {
						count_pop_faction = {
							count < 4
						}
					}
				}
			}
		}
		promote_faction = {
			title = "PROMOTE_FACTION"
			description = "PROMOTE_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					NOR = {
						has_modifier = suppressed_\\1
						has_modifier = promoted_\\1
					}
				}
			}

			effect = {
				parameter:empire = {
					add_modifier = { modifier = promoted_\\1 days = -1 }
				}
			}

			ai_weight = {
				base = 0
			}
		}
		cancel_promote_faction = {
			title = "CANCEL_PROMOTE_FACTION"
			description = "CANCEL_PROMOTE_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = { has_modifier = promoted_\\1 }
			}

			effect = {
				parameter:empire = {
					remove_modifier = promoted_\\1
				}
			}

			ai_weight = {
				base = 0
			}
		}
		suppress_faction = {
			title = "SUPPRESS_FACTION"
			description = "SUPPRESS_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					NOR = {
						has_modifier = suppressed_\\1
						has_modifier = promoted_\\1
					}
				}
			}

			effect = {
				add_modifier = { modifier = suppressed_faction days = -1 }
				parameter:empire = {
					add_modifier = { modifier = suppressed_\\1 days = -1 }
				}
			}

			ai_weight = {
				base = 0
			}
		}
		cancel_suppress_faction = {
			title = "CANCEL_SUPPRESS_FACTION"
			description = "CANCEL_SUPPRESS_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = { has_modifier = suppressed_\\1 }
			}

			effect = {
				remove_modifier = suppressed_faction
				parameter:empire = {
					remove_modifier = suppressed_\\1
				}
			}

			ai_weight = {
				base = 0
			}
		}""",
	r = """inline_script = {
			script = pop_faction_types/standard_actions
			faction = __objectname
			ethic = \\1
			opposite = __opposite_\\1
			apply_to_other_factions = "always = no"
		} # Undercoat scripted trigger""",
	folder = 'federation_types'
)
# standard faction actions (multi-faction ethic)
add_substitution(
	f = """embrace_faction = {
			title = "EMBRACE_FACTION"
			description = "EMBRACE_FACTION_DESC"

			cost = {
				unity = 5000
			}

			potential = {
				exists = owner
				owner = {
					OR = {
						is_subject = no
						NOT = { any_agreement = { agreement_preset = preset_dominion } }
					}
				}
			}

			valid = {
				custom_tooltip = {
					fail_text = EMBRACE_FACTION_COOLDOWN
					parameter:empire = {
						NOT = { has_modifier = embraced_faction_timer }
					}
				}
				support > 0.20
				parameter:empire = {
					NOT = { has_ethic = "ethic_fanatic_([^ \\t]+)" }
				}
			}

			effect = {
				add_modifier = { modifier = embraced_faction days = 3600 }
				parameter:empire = {
					shift_ethic = ethic_\\1
					hidden_effect = {
						every_pop_faction = { # embraces \\1 ethos
							limit = { (.*) }
							add_modifier = { modifier = embraced_faction days = 3600 }
						}
						add_modifier = { modifier = embraced_faction_timer days = 3600 }
						every_pop_faction = {
							limit = { NOT = { is_same_value = root } }
							add_modifier = { modifier = embraced_another_faction days = 3600 }
						}
					}
				}
				hidden_effect = {
					save_event_target_as = TargetFaction
					parameter:empire = {
						every_relation = {
							limit = {
								is_ai = no
								is_country_type = default
								has_communications = prev
								has_intel_level = {
									who = prev
									category = government
									level >= 1
								}
							}
							country_event = { id = factions.2000 }
						}
					}
				}
			}

			ai_weight = {
				base = 1
				modifier = {
					factor = 0
					support < 0.50
					owner = {
						has_ethic = ethic_\\1
					}
				}
				modifier = {
					factor = 0
					owner = { has_valid_civic = civic_fanatic_purifiers }
				}
				modifier = {
					factor = 0
					owner = {
						count_pop_faction = {
							count < 4
						}
					}
				}
			}
		}
		promote_faction = {
			title = "PROMOTE_FACTION"
			description = "PROMOTE_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					NOR = {
						has_modifier = suppressed_\\1
						has_modifier = promoted_\\1
					}
				}
			}

			effect = {
				parameter:empire = {
					add_modifier = { modifier = promoted_\\1 days = -1 }
				}
			}

			ai_weight = {
				base = 0
			}
		}
		cancel_promote_faction = {
			title = "CANCEL_PROMOTE_FACTION"
			description = "CANCEL_PROMOTE_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					has_modifier = promoted_\\1
				}
			}

			effect = {
				parameter:empire = {
					remove_modifier = promoted_\\1
				}
			}

			ai_weight = {
				base = 0
			}
		}
		suppress_faction = {
			title = "SUPPRESS_FACTION"
			description = "SUPPRESS_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					NOR = {
						has_modifier = suppressed_\\1
						has_modifier = promoted_\\1
					}
				}
			}

			effect = {
				add_modifier = { modifier = suppressed_faction days = -1 }
				parameter:empire = {
					hidden_effect = {
						every_pop_faction = {
							limit = { \\2 }
							add_modifier = { modifier = suppressed_faction days = -1 }
						}
					}
					add_modifier = { modifier = suppressed_\\1 days = -1 }
				}
			}

			ai_weight = {
				base = 0
			}
		}
		cancel_suppress_faction = {
			title = "CANCEL_SUPPRESS_FACTION"
			description = "CANCEL_SUPPRESS_FACTION_DESC"

			potential = {
				exists = owner
				parameter:empire = {
					has_modifier = suppressed_\\1
				}
			}

			effect = {
				remove_modifier = suppressed_faction
				parameter:empire = {
					remove_modifier = suppressed_\\1
					hidden_effect = {
						every_pop_faction = {
							limit = { \\2 }
							remove_modifier = suppressed_faction
						}
					}
				}
			}

			ai_weight = {
				base = 0
			}
		}""",
	r = """inline_script = {
			script = pop_faction_types/standard_actions
			faction = __objectname
			ethic = \\1
			opposite = __opposite_\\1
			apply_to_other_factions = "\\2"
		} # Undercoat scripted trigger""",
	folder = 'pop_faction_types'
)

# events/homicidal_option_2
add_substitution(
	f = """option = {
		exclusive_trigger = {
			(\\w+) = { has_valid_civic = civic_machine_terminator }
		}
		name = EXTERMINATE
	}
	option = {
		exclusive_trigger = {
			\\1 = { has_valid_civic = civic_hive_devouring_swarm }
		}
		name = PREY
	}
	option = {
		exclusive_trigger = {
			\\1 = { has_valid_civic = civic_fanatic_purifiers }
		}
		name = SCUM
	}""",
	r = """
	# undercoat inline script
	inline_script = {
		script = events/homicidal_option_2
		who = \\1
	}""",
	folder = 'events'
)
# events/homicidal_option_2
add_substitution(
	f = """option = {
		exclusive_trigger = {
			has_valid_civic = civic_machine_terminator
		}
		name = EXTERMINATE
	}
	option = {
		exclusive_trigger = {
			has_valid_civic = civic_hive_devouring_swarm
		}
		name = PREY
	}
	option = {
		exclusive_trigger = {
			has_valid_civic = civic_fanatic_purifiers
		}
		name = SCUM
	}""",
	r = """inline_script = {
		script = events/homicidal_option_2
		who = this
	}""",
	folder = 'events'
)
# events/homicidal_option_2
add_substitution(
	f = """name = {
		trigger = { (\\w+) = { has_valid_civic = civic_hive_devouring_swarm } }
		text = PREY
	}
	name = {
		trigger = { \\1 = { has_valid_civic = civic_fanatic_purifiers } }
		text = SCUM
	}
	name = {
		trigger = { \\1 = { has_valid_civic = civic_machine_terminator } }
		text = EXTERMINATE
	}""",
	r = """
	# undercoat inline script
	inline_script = {
		script = events/homicidal_option_text_2
		who = \\1
	}""",
	folder = 'events'
)
# events/homicidal_option
add_substitution(
	f = """option = {
		name = SCUM
		trigger = {
			has_valid_civic = civic_fanatic_purifiers
		}
	}
	option = {
		name = TASTY
		trigger = {
			has_valid_civic = civic_hive_devouring_swarm
		}
	}
	option = {
		name = EXTERMINATE
		trigger = {
			has_valid_civic = civic_machine_terminator
		}
	}""",
	r = """inline_script = {
		script = events/homicidal_option
		who = this
	}""",
	folder = 'events'
)
# events/homicidal_option
add_substitution(
	f = """option = {
		name = SCUM
		trigger = {
			(\\w+) = { has_valid_civic = civic_fanatic_purifiers }
		}
	}
	option = {
		name = TASTY
		trigger = {
			\\1 = { has_valid_civic = civic_hive_devouring_swarm }
		}
	}
	option = {
		name = EXTERMINATE
		trigger = {
			\\1 = { has_valid_civic = civic_machine_terminator }
		}
	}""",
	r = """inline_script = {
		script = events/homicidal_option
		who = \\1
	}""",
	folder = 'events'
)
# events/homicidal_option_text
add_substitution(
	f = """name = {
			trigger = { has_valid_civic = civic_fanatic_purifiers }
			text = SCUM
		}
		name = {
			trigger = { has_valid_civic = civic_hive_devouring_swarm }
			text = TASTY
		}
		name = {
			trigger = { has_valid_civic = civic_machine_terminator }
			text = EXTERMINATE
		}""",
	r = """inline_script = {
			script = events/homicidal_option_text
			who = this
		}""",
	folder = 'events'
)


for trigger_group in triggers:
	trigger_list = trigger_group[0]
	if type(trigger_list)==str:
		trigger_list = [trigger_list]
	for trigger in trigger_list:
		for case in trigger_group[1]:
			values = case[0]
			if values is True:
				add_substitution(f=trigger)
			else:
				substitute_trigger = case[1]
				if type(values) == str:
					values = [values]
				add_or_context_substitution_patterns( trigger, values, substitute_trigger, tag="undercoat: moved to scripted trigger" )



for f in inline_substituation_patterns:
	r = 'inline_script = "{}"#!stu_tag!#'.format( inline_substituation_patterns[f] )
	add_substitution( f=f, r=r, tag="undercoat: moved to inline script"  )

for f in flag_patterns:
	add_substitution( f=f, preserve_whitespace=True )

add_substitution(
	f = '\n}',
	r = """
	init_effect = { # undercoat
		every_system_planet = { fire_on_action = { on_action = on_planet_spawned } }
		fire_on_action = { on_action = on_system_spawned }
	}
}""",
	folder = "solar_system_initializers",
	preserve_whitespace = True,
)
add_substitution(
	f = 'num_tradition_categories < 7',
	r = "num_tradition_categories < @TRADITION_CATEGORIES_MAX",
	tag = "undercoat: added script variable",
)


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
			print(self.vanilla_path)
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

	def find( self, pattern ):
		if ( pattern.folder is None ) or ( pattern.folder == self.parent.name ):
			if re.search( pattern.f, self.text ):
				print( f"found pattern {pattern.f} in file {self.vanilla_path}" )
				self.should_write = True
				if pattern.r is not None:
					self.text = re.sub( pattern.f, pattern.r, self.text)
				# add comments
				if pattern.tag is not None:
					self.text = re.sub( r'#!stu_tag!#(.*)\n', f'\\1 # {pattern.tag}\\n', self.text )
					self.text = re.sub( r'#!stu_tag!#(.*)$', f'\\1 # {pattern.tag}', self.text )


	def process_text(self):
		self.should_write = False
		for substitution in substitutions:
			self.find( substitution )
		if self.parent.name == "pop_faction_types":
			objectname = self.name.replace('00_','')
			self.text = self.text.replace( '__objectname', objectname )
			for ethic in ethic_opposites:
				self.text = self.text.replace( f"__opposite_{ethic}", ethic_opposites[ethic] )
		if self.should_write:
			self.write()
		
	def clear(self,dir):
		dir = os.path.join(self.stu_path,dir)
		if os.path.exists(dir):
			rmtree(dir)
		

root = stu_path(
	vanilla_path="C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stellaris",
	# stu_path="C:\\Users\\kuyan\\OneDrive\\Documents\\Paradox Interactive\\Stellaris\\mod\\scripted_trigger_undercoat"
	stu_path="C:\\Users\\kuyan\\OneDrive\\Desktop\\mod stuff\\stu_test_output"
)
root.clear('common')
root.clear('events')
root.clear('gfx')
root.clear('sound')
root.process()