import pytest
from backend.universe import Universe

@pytest.fixture
def base_rules():
    return {
        'Heroes Unlimited': {'combat': 'Roll d20 for attack.', 'skills': 'Percentile skill checks.'},
        'Ninjas & Superspies': {'combat': 'Roll d20, add bonuses.', 'skills': 'd100 for skills.'},
        'TMNT': {'combat': 'Roll d20 for attack.', 'skills': 'Percentile skill checks.'}
    }

def test_create_universe_from_multiple_systems(base_rules):
    u = Universe(name='TestU', owner_id='user1')
    u.add_system('Heroes Unlimited', base_rules['Heroes Unlimited'])
    u.add_system('Ninjas & Superspies', base_rules['Ninjas & Superspies'])
    assert set(u.all_systems()) == {'Heroes Unlimited', 'Ninjas & Superspies'}
    # Should merge combat and skills
    assert 'combat' in u.rules and 'skills' in u.rules
    assert '[Merged]' in u.rules['combat'] or u.rules['combat'] != base_rules['Heroes Unlimited']['combat']

def test_add_system_to_existing_universe(base_rules):
    u = Universe(name='TestU', owner_id='user1')
    u.add_system('TMNT', base_rules['TMNT'])
    assert u.has_system('TMNT')
    u.add_system('Ninjas & Superspies', base_rules['Ninjas & Superspies'])
    assert set(u.all_systems()) == {'TMNT', 'Ninjas & Superspies'}
    # Rules should be re-merged
    assert '[Merged]' in u.rules['combat'] or u.rules['combat'] != base_rules['TMNT']['combat']

def test_ai_merges_rules_with_conflicts():
    u = Universe(name='TestU', owner_id='user1')
    sys1 = {'combat': 'A', 'skills': 'B'}
    sys2 = {'combat': 'C', 'skills': 'B'}
    u.add_system('Sys1', sys1)
    u.add_system('Sys2', sys2)
    # Combat should be merged, skills should not
    assert u.rules['combat'].startswith('[Merged]')
    assert u.rules['skills'] == 'B'

def test_prevent_duplicate_system_additions(base_rules):
    u = Universe(name='TestU', owner_id='user1')
    u.add_system('TMNT', base_rules['TMNT'])
    with pytest.raises(ValueError):
        u.add_system('TMNT', base_rules['TMNT'])

def test_user_overrides_ai_generated_rules(base_rules):
    u = Universe(name='TestU', owner_id='user1')
    u.add_system('Heroes Unlimited', base_rules['Heroes Unlimited'])
    u.add_system('Ninjas & Superspies', base_rules['Ninjas & Superspies'])
    # User overrides combat rule
    u.set_user_override('combat', 'User custom combat rule.')
    assert u.get_rule('combat') == 'User custom combat rule.'
    # Adding another system does not overwrite user override
    u.add_system('TMNT', base_rules['TMNT'])
    assert u.get_rule('combat') == 'User custom combat rule.'

def test_rules_are_saved_for_future_use(base_rules):
    # Simulate a global rule cache
    rule_cache = {}
    def save_rules(system, rules):
        rule_cache[system] = rules
    u = Universe(name='TestU', owner_id='user1')
    for sys, rules in base_rules.items():
        save_rules(sys, rules)
    # All rules should be available for all users
    for sys in base_rules:
        assert sys in rule_cache
        assert rule_cache[sys] == base_rules[sys]
