import json

with open("person.txt", "r") as arquivo:
  texto = arquivo.readlines()

# print(texto)

for busca in texto:
  if "SPIDERMAN" in busca:
    print(busca)