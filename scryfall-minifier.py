#!/usr/bin/env python3

import sys, getopt, json

attributes_to_keep = ['name', 'set', 'collector_number']

def main(argv):
  f_in = 'not_defined'
  f_out = 'not_defined'
  opts, _ = getopt.getopt(argv,"hi:o:",["help","input=","output="])
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print ('scryfall-mignifier.py -i <input> -o <output>')
      sys.exit()
    elif opt in ("-i","--input"):
      f_in = arg
    elif opt in ("-o","--output"):
      f_out = arg
  
  with open(f_in) as json_input:
    print("read input file")
    data = json.load(json_input)
    cards = list(filter(lambda x: x['object'] == 'card', data))
    print("found {} card(s)".format(len(cards)))

    print("write output file")
    with open(f_out, 'w') as json_output:
      minified = [{key: card[key] for key in attributes_to_keep} for card in cards]
      json.dump(minified, json_output)
      print("done.")
        

if __name__ == "__main__":
  main(sys.argv[1:])