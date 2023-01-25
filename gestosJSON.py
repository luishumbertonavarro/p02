

import json

person_dict = {"Gesto": "PALMA_ABIERTA",
"Pinky": "DEDOSENUM.PINKY.value",
"Index": "DEDOSENUM.INDEX.value",
"Thumb": "DEDOSENUM.THUMB.value",
"Ring": "DEDOSENUM.RING.value",
"Middle": "DEDOSENUM.MIDDLE.value",
"Image": "./recursos/PALMA_ABIERTA.pnga"
}

with open('person.txt', 'a') as json_file:
  json.dump(person_dict, json_file)
  json_file.write('\n')
