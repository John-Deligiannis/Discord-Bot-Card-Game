#-----------------------------------#
            #Importations#
#-----------------------------------#
#Card Index Number / Card Name / Rarity (0, 1, 2, 3, 4) / Base Stat: [HP, Atk, Def, Magic, Magic Def, Speed] / Lore Text
CardsBaseList = [
  [0, "Valkyrie", 0, [9, 7, 3, 2, 1, 3], "The generals in Xalt's army are made up of these fearless warriors. The Valkyries will charge into battle no questions asked and decimate the enemy."],
  [1, "Kotaro", 0, [7, 6, 2, 4, 2, 8],"A modern day ninja and robin hood. Kotaro enjoys playing Pokémon Go! and posting thirst trap videos on Tik Tok."],
  [2, "Glaceor", 0, [8,7,2,8,3,5],"Some say he was he was born a man, then turned to ice. Others say he was ice, turned to man. Everyone agrees on his titanic power, only mirrored by the sleeping giants, glaciers."],
  [3, "Clay Soldier", 0, [11,6,4,6,2,4],"A member of a once cerimonial army built for an ancient king. Forgotten for centuries, on reawakened by witch to follow her nefarious schemes"],
  [4, "Captain Curtis", 0, [8,7,3,5,2,6],"A fugative of the United States Millitary, Capitain Curtis was sent on the run after he discovered secret millitary documents when he was stationed at Area 51. His two dogs, A{OUEHFG and AOIEHFG0o are his best and only friends."],
  [5, "Shard Runner", 0, [8,8,2,8,2,7],"The Shard Runners were a group of vigilantes during the corporation wars. Nearly eradicated by the megacorp Azmuth Industries, only a few Shard Runners live to tell the tales of thier fight against corporate dictatorship."],
  [6, "Crypt Guard", 1, [22,17,4,12,5,19],"There was a time when every crypt had Crypt Guard. Now all that remains are the rotting corpses, still just as powerful, but very smelly."],
  [7, "Skydiving Moose", 1, [18,16,5,11,4,15],"Once built lightsabers for jedi, the mythical SkydivingMoose now enjoys retirement sipping tea next to the ocean. His days of glory firmly cemetented in galactic history."],
  [8, "Froxial", 1, [20,18,5,16,3,17],"The product of turbulant seas and toxic waste. Born in mixing pot of radiation and swirling sea foam. A right hand man to Poseidon, he has a deep love for the seas from which he was born."],
  [9, "Woud", 2, [33,35,11,34,11,33],"A stealthy forest tracker and tactical genius. Woud is determined to drive the intruders from his forest. He is not afraid to use lethal force. Traps and ambushes make entering his forest extremely risky to anyone except himself."],
  [10, "Xalt", 2, [36,34,11,28,8,30],"The son of a mighty viking warlord. His infamous reputation for being a ruthless leader in battle, taking only neccesary prisoners. Enjoys gardens and pedicures."],
  [11, "Voltaic Spartan", 2, [32,33,9,38,12,36],"Children of Zeus, the Voltaic Spartan is the first line of defence against any unseen foe foolish enough to attack Mount Olympus."],
  [12, "Ben 20", 2, [34,32,12,35,11,35],"A fallen off child prodigy, now using his powers and intelligence for crime."],
  [13, "Lunar Guardian", 3, [69,66,22,62,20,62],"A servant of the Lunar Praetorian, a Lunar Guaridan devouts its entire 450 year life to the defence of The Moonlit Temple and the untold power within."],
  [14, "Edgerunner", 3, [60,62,20,62,21,69],"In a corrput world, one must be equally corrupt. At least that's how the Edgerunners justify their actions. Raiding local buisnesses, pillaging people on the street, dealing illict drugs, the Edgerunners are a force to be reckoned with."],
  [15, "Cyblade", 3, [66,65,21,61,20,60],"Born in the year 3022, Kanye East was born. He likes technology. Thats it."],
  [16, "Anubis", 3, [66,65,21,61,20,60],"An abomination born during the age of the Black Death. When not in a special containment suit, it will infect anything it comes in contact with. Spends its days working to cure its curse. It just wants to be normal and have real friends."],
  [17, "Pyralis", 4,[96,98,32,98,33,96],"A child of the flame. Some say that when he was younger his family did't have to pay to heat their house. Everyones best friend in the winter. Banned from glacial parks. May or may not be the largest factor of global warming."],
  [18, "Kotoshi", 4, [94,93,30,93,30,100],"An ancient samurai with the ability wield the shadows through his sword who will destory anyone in his path."],
  [19, "Lunar Praetorian", 4, [100,96,33,98,31,92],"The guardian of the Interstellar Staff of Life. Waits silentily in its sanctuary, ready to thwart anything theatening its peace."]
    ]
#-----------------------------------#
            #Functions#
#-----------------------------------#
def GetCardsBaseStatList():
  return CardsBaseList
#-----------------------------------#
