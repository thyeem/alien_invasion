# Note: here assumed that ONLY VALID DATA will be given as a map file.
# In order to focus on the algorithm itself, I skipped all validations of
# input files and command-line arguments.

import random 

def parse_world_map(mapfile):
    world_map = {}      # {key: city, value: dict(direction=vicinity)}
    with open(mapfile, 'r') as f:
        lines = [ line.strip() for line in f if line.strip() ]
    for line in lines:
        token = [ l.split('=') for l in line.split() ]
        key = token.pop(0).pop()
        world_map[key] = token and dict(token) or dict()
    return world_map

def dump_world_map(world_map):
    print("\n----- THE REMAINING WORLD ----------")
    if not world_map: print("All cities are destroyed.")
    for city, road in world_map.items():
        print(city, ' '.join('='.join(item) for item in road.items()))

def init_alien_invasion(num_aliens, world_map):
    city_aliens = {}     # {key: invaded city, value: set(alien_ids)}
    if not world_map: return city_aliens
    for alien_id in map(str, range(1, num_aliens+1)):
        invaded = random.choice(list(world_map))
        move_alien_into_city(alien_id, invaded, city_aliens)
    return city_aliens

def move_alien_from_city(alien_id, city, city_aliens):
    city_aliens[city].remove(alien_id)
    if not city_aliens[city]: del city_aliens[city]

def move_alien_into_city(alien_id, city, city_aliens):
    if city in city_aliens:
        city_aliens[city].add(alien_id)
    else:
        city_aliens[city] = set([alien_id])

def wander_randomly(world_map, city_aliens):
    for from_city, alien_ids in city_aliens.copy().items():
        if not world_map[from_city]: continue
        for alien_id in alien_ids.copy():
            into_city = random.choice(list(world_map[from_city].values()))
            move_alien_from_city(alien_id, from_city, city_aliens)
            move_alien_into_city(alien_id, into_city, city_aliens)

def destroy_and_kill(world_map, city_aliens):
    for city, alien_ids in city_aliens.copy().items():
        if len(alien_ids) < 2: continue
        for _, vicinity in world_map[city].items():
            for direction, c in world_map[vicinity].copy().items():
                if c == city: del world_map[vicinity][direction]
        del world_map[city]
        del city_aliens[city]
        ids = [ f'alien {i}' for i in alien_ids ]
        print(f'{city} has been destroyed by {", ".join(ids[:-1])} and {ids[-1]}!')

def run(num_aliens, FILE_MAP, MAX_MOVES_ALIEN):
    world_map = parse_world_map(FILE_MAP)
    city_aliens = init_alien_invasion(num_aliens, world_map)
    destroy_and_kill(world_map, city_aliens)
    
    moves = 0
    while True:
        if moves > MAX_MOVES_ALIEN: break
        if not world_map: break
        if not city_aliens: break
        wander_randomly(world_map, city_aliens)
        destroy_and_kill(world_map, city_aliens)
        moves += 1
    dump_world_map(world_map)


if __name__ == '__main__':
    import sys 
    FILE_MAP = '../worldmap/coin_world.txt'
    MAX_MOVES_ALIEN = 10000

    if len(sys.argv) != 2: sys.exit(f'Usage: {sys.argv[0]} <num of aliens>')
    run(int(sys.argv[1]), FILE_MAP, MAX_MOVES_ALIEN)

