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