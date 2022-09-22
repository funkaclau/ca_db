from peewee import * 

db = SqliteDatabase('user.db')


class User(Model): 
    name = CharField() 
    tg_id = IntegerField() 
    wallet = CharField() 
    food_bank = IntegerField() 
    coins = IntegerField()
    coins_earned = IntegerField() 
    coins_spent = IntegerField() 
    items_sold = IntegerField() 
    items_bought = IntegerField() 
    belt_tick = IntegerField() 
    clover_tick = IntegerField()
    explore = IntegerField() 
    home = IntegerField() 
    search = IntegerField() 
    home = IntegerField() 
    mine = IntegerField() 
    chop = IntegerField() 
    crafted = IntegerField() 
    collected = IntegerField() 
    eat = IntegerField()
    class Meta: 
        database = db 


class Log(Model):
    command = CharField()
    user = CharField() 
    type = CharField() 
    subtype = CharField() 
    status = CharField() 
    time = IntegerField() 
    
		
class Collector(Model): 
	owner = ForeignKeyField(User, backref='collectors') 
	asset_id = CharField() 
	number = IntegerField() 
    daring = BooleanField()
    tired = BooleanField()
    hungry = BooleanField()
    max_inv = IntegerField() 
    actions = IntegerField() 
    actions_max = IntegerField() 
    location = CharField()
    distance = IntegerField()
	class Meta: 
		database = db 

class Equipment(Model): 
    owner = ForeignKeyField(Collector, backref='equipment') 
    teleportal = CharField() 
    teleportal_id = IntegerField() 
    axe = CharField() 
    axe_id = IntegerField() 
    pick = CharField() 
    pick_id = IntegerField() 
    clover = CharField() 
    clover_id = IntegerField() 
    belt = CharField() 
    belt_id = IntegerField() 
    bag = CharField() 
    bag_id = IntegerField() 
    boots = CharField() 
    boots_id = IntegerField() 
    class Meta: 
		database = db 

class Stash(Model):
    owner = ForeignKeyField(User, backref='stash')
    stash_id = IntegerField() 
    location = CharField() 
    space = IntegerField() 
    level = IntegerField() 
    wood = IntegerField() 
    stone = IntegerField() 
    clay = IntegerField() 
    nail = IntegerField()
    class Meta: 
		database = db 

class Tool(Model):
    owner = oreignKeyField(User, backref='tools')
    knife = BooleanField()
    frame = BooleanField()
    fpan = BooleanField()
    pan = BooleanField()
    bowl = BooleanField()
    dish = BooleanField()
    jar = BooleanField()
    wood_spoon = BooleanField()
    wood_spatula = BooleanField()
    bamboo_cup = BooleanField()
    class Meta: 
		database = db 

class Inventory(Model):
    owner = owner = oreignKeyField(User, backref='inventory')
    holder = Charfield()
    name = Charfield()
    template_id = IntegerField() 
    schema = IntegerField() 
    class Meta: 
		database = db 
    