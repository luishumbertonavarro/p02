import json

with open("person.txt", "r") as arquivo:
  texto = arquivo.readlines()

#print(texto)

for busca in texto:
  if "SPIDERMAN_SIGN" in busca:
    print(busca)