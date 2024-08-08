from random import *
from math import *
#Whenever you type a word, it creates a new spell, and, the more mutagen given to the spell, the more powerful it is. 
spell_types={
    "Fire":{},
    "Frost":{},
    "Arcana":{},
    "Holy":{},
    "Shadow":{},
    "Nature":{},
    "Fel":{}
}
All_Requirements=[
    "C","G","Lb","D","Ab","B"
]
damage_types=["force","radiant","acid","poison","psychic","lightning","cold","fire"]
net_libram=[]
def get_net_libram(X):
    if len(net_libram)==0:
        with open("Effects.txt","r") as f:
            for i in f.read().split("\n"):
                net_libram.append(i)
    return net_libram[min(9999,max(0,X))]
colors=["black","crimson","red","orange","yellow","dark green","light green","light blue","dark blue","purple","pink","white","light gray","dark gray","brown"]
effects=["spikes","spheres","wave","weapon","water","fire","bolts","projectiles","auras","runes"]
def create_new_effect(new_seed,mutagen):
    smutagen=mutagen
    seed(new_seed)
    output=""
    mode=randint(1,1)
    #Random Ranged Damage spell
    requirements=[]
    for i in range(6):
        roll=random()
        if roll<0.3**(1+0.4*i):
            requirements.append("n-"+All_Requirements[i])
            mutagen*=1.05+0.25*i
        elif roll>1-0.2**(1+0.4*i):
            requirements.append(All_Requirements[i])
            mutagen*=1.1+0.5*i
    
    mutagen=int(mutagen)
    smutagen2=mutagen/smutagen
    if mode==1:
        
        discharge_roll=random()
        #Sphere, Cone, Multi Target, Normal
        for i in enumerate([0.025,0.05,0.1,1]):
            discharge_roll-=i[1]
            if discharge_roll<=0:
                discharge=i[0]
                break
        if discharge==0:
            if random()<0.1:
                d2=1
                #2 in every direction
                mutagen=int(mutagen/7)
            else:
                d2=0
                mutagen=int(mutagen/3)
        elif discharge==1:
            if random()<0.04:
                d2=1
                #30ft in one direction
                mutagen=int(mutagen/10)
            else:
                d2=0
                mutagen=int(mutagen/3)
        elif discharge==2:
            d2=2-int(log(random(),2))
            mutagen=int(mutagen/(d2+1))
        type_of_spell=choice(list(spell_types.keys()))
        mutagen_raw_damage=random()*mutagen
        mutagen-=ceil(mutagen_raw_damage)
        used_dice=randint(0,4)*2+4
        used_dice_reduction=(used_dice+1)/2
        while mutagen_raw_damage<used_dice_reduction and used_dice>4:
            used_dice_reduction-=1
            used_dice-=2
        used_dice_count=max(1,int(mutagen_raw_damage/used_dice_reduction*random()**0.5))
        extra_to_hit=-int(log(random(),3))
        if mutagen>extra_to_hit*5: mutagen-=extra_to_hit*5
        else: extra_to_hit=0
        damage_type_roll=random()
        # fire, cold, poison, acid, radiant, force, lightning, psychic
        # force, radiant, acid, poison, psychic, lightning, cold, fire
        for i in enumerate([0.01,0.02,0.04,0.08,0.14,0.2,0.3,1]):
            damage_type_roll-=i[1]
            if damage_type_roll<=0:
                damage_type=i[0]
                break
        output+=f"Ranged spell attack, Type: {type_of_spell}. Discharge: {['Sphere','Cone','Multi Target','Single Target'][discharge]}, "
        if discharge==0: output+=f"Range: self, Radius: {d2+2} sq,"
        if discharge==1: output+=f"Range: self, Radius: {d2*2} sq,"
        if discharge==2: output+=f"Target count: {d2},"
        if extra_to_hit>0: output+=f" +{extra_to_hit} to hit,"
        output+=f" {used_dice_count}d{used_dice} {damage_types[damage_type]}. \n"
        other_effects=randint(0,1)
        if other_effects==1:
            if random()<0.8 or mutagen<50:
                mutagen_on_DC=random()**2*mutagen+0.01
                mutagen-=mutagen_on_DC
                mutagen=int(mutagen)
                output+=f"On a succesful hit, the target must succeed on a DC {10-int(log(random(),1+1/mutagen_on_DC))} {['STR','DEX','CON','INT','WIS','CHA'][randint(0,5)]} saving throw, and they may choose to evade the effects of the following effect. "
            else:
                mutagen=int(mutagen/2)
                output+="On a succesful hit the following effect triggers: "
            new_effect=get_net_libram(randint(0,10000))[5:].replace("Caster","Target").replace("caster","target")
            output+="\n"+new_effect
        
        if len(requirements)>0:
            output+="\n"+f"Requirements for the spell:"
            for i in requirements:
                output+=" "+i
        if smutagen>smutagen-int(mutagen/smutagen2):
            output+=f"\nThe Cost of this spell has been reduced to {smutagen-int(mutagen/smutagen2)} Mirtons."
    output+="\nThe spells visual appearance consists of "
    for i in range(int(log(smutagen,10)+1)):
        output+=choice(colors)+" "+choice(effects)+","
    return output
while True:
    try:
        print(create_new_effect(sum(["abcdefghijklmnopqrstuvwxyz".index(i[1])*26**i[0] for i in enumerate(input("Trigger: "))]),int(input("Mutagen: "))))
    except Exception as e:
        print(e)
for i in range(20):
    print(create_new_effect(i+100,110))
    print()