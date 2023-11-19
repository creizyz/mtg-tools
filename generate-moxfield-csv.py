#!/usr/bin/env python3

import sys, getopt, json, csv

attributes_to_keep = ['name', 'set', 'collector_number']

def main(argv):
  f_in = 'not_defined'
  f_out = 'not_defined'
  scryfall_db = 'not_defined'
  opts, _ = getopt.getopt(argv,'hi:o:s:',['help','input=','output=','scryfall='])
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print ('scryfall-mignifier.py -i <input> -o <output> -s <scryfall>')
      sys.exit()
    elif opt in ('-i','--input'):
      f_in = arg
    elif opt in ('-o','--output'):
      f_out = arg
    elif opt in ('-s','--scryfall'):
      scryfall_db = arg
  
  with open(scryfall_db) as scryfall:
    print('reading scryfall db file...')
    cards = json.load(scryfall)
    print('done (found {} cards).'.format(len(cards)))
    
    with open(f_in) as json_input:
      print('reading input file...')
      inputs = json.load(json_input)
      print('done (found {} cards).'.format(len(inputs)))
      
      print('matching inputs with scryfall db file...')
      csv_cards = list()
      for i in inputs:
        card = next((x for x in cards if x['set'] == i['e'] and x['collector_number'] == i['cn']), None)
        if card == None:
          print('could not find card: e={} cn={}'.format(i['e'], i['cn']))
          continue
        row = {}
        row['Count'] = 1
        row['Condition'] = 'NM'
        row['Language'] = 'FR'
        row['Edition'] = card['set']
        row['Foil'] = 'foil' if i['foil'] == 'yes' else ''
        row['Collector Number'] = card['collector_number']
        row['Name'] = card['name']
        csv_cards.append(row)
      print('done (found {} matches).'.format(len(csv_cards)))
        
      print('writing moxfield CSV')
      with open(f_out, 'w') as csv_output:
        writer = csv.writer(csv_output, quoting=csv.QUOTE_ALL)
        writer.writerow(['Count', 'Condition', 'Language', 'Edition', 'Foil', 'Collector Number', 'Name'])
        for row in csv_cards:
            writer.writerow([row['Count'], row['Condition'], row['Language'], row['Edition'], row['Foil'], row['Collector Number'], row['Name']])
        print('done.')
        

if __name__ == '__main__':
  main(sys.argv[1:])