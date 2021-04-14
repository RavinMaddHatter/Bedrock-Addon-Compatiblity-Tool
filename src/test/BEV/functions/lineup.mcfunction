setblock ~ ~2 ~ monster_egg 
fill ~ ~2 ~ ~ ~2 ~ air 0 destroy 
tag @e[type=minecraft:silverfish,r=3] add centerer 
execute @e[tag=centerer] ~ ~ ~ tp @e[type=hatchibombotar:grave,r=3] ~0.7 ~-2 ~0.5 
kill @e[tag=centerer] 
tp @s ~ ~ ~ facing ~1 ~ ~ 