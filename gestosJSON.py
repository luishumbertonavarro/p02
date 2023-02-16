<<<<<<< HEAD


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
=======
import json

person_dict = {"Gesto": "SPIDERMAN",
                "Thumb": "DEDOSENUM.THUMB.value",
                "Index": "DEDOSENUM.INDEX.value",
                "Middle": None,
                "Ring": None,
                "Pinky": "DEDOSENUM.PINKY.value",
                "Image": "./recursos/SPIDERMAN.png"
            }

with open('person.txt', 'a') as json_file:
  json.dump(person_dict, json_file)
  json_file.write('\n')
>>>>>>> ce4e38be6700f1848b2b6e077a5dcd3d3a0a7b55
