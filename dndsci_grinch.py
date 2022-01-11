import random
import math
 
def roll_die(n):
    return math.ceil(random.random()* n )
 
def blum_blooper_noise(child):
    return(6)
 
def fum_foozler_noise(child):
    return( 8 if child.gender == 'F' else 4)
 
def gah_ginka_noise(child):
    return( 11 - math.floor(child.age / 2) )
 
def sloo_slonker_noise(child):
    return( 5 + math.floor(child.age / 2) )
 
def trum_troopa_noise(child):
    if len([s for s in child.get_siblings() if 'Trum-Troopa' in [ t['name'] for t in s.toys ]]):
        return(10)
    else:
        return(5)
 
def who_whonker_noise(child):
    return( 9 if child.gender == 'M' else 5)
 
names = [
    { 'name' : 'Andy', 'Gender' : 'M' },
    { 'name' : 'Betty', 'Gender' : 'F' },
    { 'name' : 'Cindy', 'Gender' : 'F' },
    { 'name' : 'Danny', 'Gender' : 'M' },
    { 'name' : 'Eddie', 'Gender' : 'M' },
    { 'name' : 'Freddie', 'Gender' : 'M' },
    { 'name' : 'Georgie', 'Gender' : 'M' },
    { 'name' : 'Harry', 'Gender' : 'M' },
    { 'name' : 'Johnny', 'Gender' : 'M' },
    { 'name' : 'Lucy', 'Gender' : 'F' },
    { 'name' : 'Mary', 'Gender' : 'F' },
    { 'name' : 'Phoebe', 'Gender' : 'F' },
    { 'name' : 'Naomi', 'Gender' : 'F' },
    { 'name' : 'Ollie', 'Gender' : 'M' },
    { 'name' : 'Ruby', 'Gender' : 'F' },
    { 'name' : 'Sally', 'Gender' : 'F' },
]
 
class Child():
    def __init__(self, child_id, family, world):
        self.child_id = child_id
        self.age = 1
        self.favorite_toy = random.choice(world.toy_names)
        self.family = family
        self.world = world
        self.toys = []
        self.assign_name()
 
    def assign_name(self):
        self.name = None
        while self.name == None:
            name_data = random.choice(names)
            raw_name = name_data['name']
            if len([c for c in self.world.children if c.name == raw_name]) == 0:
                self.name = raw_name
                self.gender = name_data['Gender']
 
    def get_siblings(self):
        return([c for c in self.world.children if c.family == self.family and c != self])
 
    def get_full_name(self):
        return(self.name + ' ' + self.family + ' Who')

    def print_self(self):
        print('{} (ID{}, {}{}, likes {})'.format(self.get_full_name(), self.child_id, self.age, self.gender, self.favorite_toy))

    def increment_age(self):
        self.age = self.age + 1
   
class World():
    def __init__(self):
        self.year = -100 # to allow time for child ages to settle
        self.initialize_families()
        self.initialize_toys()
        self.setup_logs()
 
    def initialize_families(self):
        self.families = [ 'Drew', 'Lou', 'Sue' ]
        self.children = []
        self.current_child_id = 1432
 
    def initialize_toys(self):
        self.toys = [
            {'name' : 'Blum-Blooper', 'noise_func' : blum_blooper_noise},
            {'name' : 'Fum-Foozler', 'noise_func' : fum_foozler_noise},
            {'name' : 'Gah-Ginka', 'noise_func' : gah_ginka_noise},
            {'name' : 'Sloo-Slonker', 'noise_func' : sloo_slonker_noise},
            {'name' : 'Trum-Troopa', 'noise_func' : trum_troopa_noise},
            {'name' : 'Who-Whonker', 'noise_func' : who_whonker_noise},
        ]
        self.toy_names = [t['name'] for t in self.toys]
 
    def children_age(self):
        for c in self.children:
            c.increment_age()
        self.children = [ c for c in self.children if c.age <= 12 ]
 
    def new_children(self):
        for f in self.families:
            f_children = len([c for c in self.children if c.family == f])
            new_child_roll = roll_die(4)
            if new_child_roll > f_children:
                self.children.append(Child(self.current_child_id, f, self))
                self.current_child_id = self.current_child_id + 1
 
    def allocate_toys(self):
        for c in self.children:
            c.toys = random.sample(self.toys, 2)
 
    def log(self, log_row, mode='a'):
        log_string = ','.join([str(e) for e in log_row])+'\n'
        f = open('grinch_output.csv', mode)
        f.write(log_string)
 
    def setup_logs(self):
        log_row = ['Year', 'Who Child ID', 'Who Child Name', 'Who Child Age', 'Who Child Gender', 'Toy 1', 'Toy 2', 'Noise Made']
        for t in self.toys:
            log_row.append(t['name'] + ' Received?')
        self.log(log_row, mode='w')
 
    def log_noise(self):
        for c in self.children:
            noise_made = 0
            for t in c.toys:
                toy_noise = t['noise_func'](c)
                if t['name'] == c.favorite_toy:
                    toy_noise = toy_noise * 2
                noise_made = noise_made + toy_noise
 
            log_row = [self.year, c.child_id, c.get_full_name(), c.age, c.gender, c.toys[0]['name'], c.toys[1]['name'], noise_made]
            for t in self.toys:
                log_row.append(1 if t in c.toys else 0)
            self.log(log_row)
 
    def time_passes(self, partial_year = False):
        self.year = self.year + 1
        self.children_age()
        self.new_children()
        if partial_year == False:
            self.allocate_toys()
            if self.year >= 1:
                self.log_noise()

    def print_children(self):
        for c in self.children:
            c.print_self()
 
random.seed('Grinch')
 
my_world = World()
while my_world.year <= 53:
    my_world.time_passes()
my_world.time_passes(partial_year=True)
my_world.print_children()

