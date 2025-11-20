"""Rename all category images from generic names to proper descriptive names"""
import os
import shutil

# Define mappings for each category
categories = {
    "superheroes": [
        "superman","batman","spider_man","iron_man","captain_america","wonder_woman","thor","hulk","black_widow","aquaman",
        "flash","green_lantern","black_panther","ant_man","doctor_strange","hawkeye","scarlet_witch","vision","deadpool","wolverine",
        "storm","cyclops","jean_grey","shaktimaan","captain_marvel","loki","star_lord","groot","rocket_raccoon","gamora",
        "drax","winter_soldier","falcon","war_machine","thanos"
    ],
    "cartoons": [
        "mickey_mouse","donald_duck","tom","jerry","doraemon","nobita","shinchan","chhota_bheem","chutki","motu",
        "patlu","oggy","popeye","bugs_bunny","tweety","scooby_doo","shaggy","spongebob","patrick_star","ben_10",
        "pikachu","ash_ketchum","naruto","goku","elsa","anna","olaf","simba","nala","aladdin",
        "jasmine","genie","moana","maui","woody","buzz_lightyear","minions","shrek","dora","peppa_pig"
    ],
    "vegetables": [
        "tomato","potato","onion","carrot","cabbage","cauliflower","broccoli","spinach","lettuce","cucumber",
        "eggplant","pumpkin","bitter_gourd","bottle_gourd","ridge_gourd","okra","bell_pepper","green_chili","radish","beetroot",
        "turnip","sweet_potato","ginger","garlic","corn","green_beans","peas","mushroom","zucchini","celery",
        "asparagus","artichoke","brussels_sprouts","leek","parsley","coriander","mint","fenugreek","spring_onion","kale"
    ],
    "birds": [
        "peacock","parrot","eagle","crow","sparrow","pigeon","owl","kingfisher","woodpecker","hummingbird",
        "swan","duck","goose","flamingo","pelican","stork","crane","heron","penguin","ostrich",
        "emu","kiwi","chicken","rooster","turkey","hawk","falcon","vulture","kite","cuckoo",
        "mynah","bulbul","robin","canary","finch","swallow","magpie","jay","raven","seagull"
    ],
    "flowers": [
        "rose","lotus","sunflower","jasmine","marigold","tulip","lily","orchid","daisy","daffodil",
        "hibiscus","peony","carnation","chrysanthemum","lavender","magnolia","poppy","pansy","violet","petunia",
        "zinnia","aster","dahlia","geranium","azalea","camellia","gardenia","hyacinth","iris","snapdragon",
        "gladiolus","freesia","begonia","bougainvillea","plumeria","calendula","cosmos","amaryllis","anemone","water_lily"
    ]
}

def rename_category_images(category, names):
    """Rename images for a specific category"""
    folder = f"images/{category}"
    print(f"\nRenaming {category} images...")
    renamed_count = 0
    
    # Map category names to their file prefixes
    prefix_map = {
        "superheroes": "superhero",
        "cartoons": "cartoon",
        "vegetables": "vegetable",
        "birds": "bird",
        "flowers": "flower"
    }
    prefix = prefix_map.get(category, category[:-1])
    
    for i, new_name in enumerate(names, 1):
        old_file = os.path.join(folder, f"{prefix}_{i}.jpg")
        new_file = os.path.join(folder, f"{new_name}.jpg")
        
        if os.path.exists(old_file):
            try:
                shutil.move(old_file, new_file)
                print(f"  + {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"  X Error renaming {old_file}: {e}")
        else:
            # Check if already renamed
            if os.path.exists(new_file):
                print(f"  > {new_name} (already renamed)")
            else:
                print(f"  - {old_file} not found")
    
    print(f"Renamed {renamed_count}/{len(names)} images in {category}")
    return renamed_count

# Run renaming for all categories
print("=" * 60)
print("RENAMING ALL CATEGORY IMAGES")
print("=" * 60)

total_renamed = 0
for category, names in categories.items():
    renamed = rename_category_images(category, names)
    total_renamed += renamed

print("\n" + "=" * 60)
print(f"TOTAL: {total_renamed} images renamed successfully!")
print("=" * 60)
