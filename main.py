import fields
from utils import *
from csv import DictWriter
from argparse import ArgumentParser




def main(max_row):

    url = 'https://www.courtlistener.com/api/rest/v3/financial-disclosures'

    count = 1
    row_num = 1
    with open('data/output.csv', 'w', newline = '', encoding = 'utf-8') as f:
        writer = DictWriter(f, fields.all_field_names)
        writer.writeheader()
        
        while count:
            
            data = req(url)
            people = data.get('results')
            
            #rate limited
            while not people:
                
                #wait 15 mins
                print('sleeping...')
                sleep_progress(60 * 15)
                data = req(url)
                people = data.get('results')


            for person in people:
                print(f'starting on {person["resource_uri"]}')
                
                #compute here and save so not recomputing unnecesarily
                non_disc_fields = get_person_fields(person) | get_common_fields(person)
                
                for disc_type in fields.disc_types:
                    print(f'\tGrabbing {disc_type}')

                    #each individual disclosure per type per person
                    for disc in person[disc_type]:
                        try:
                            row = get_disclosure_fields(disc, disc_type) | non_disc_fields | {'Disclosure Type': disc_type}
                            writer.writerow(row)
                        except:
                            ...
                            
                        print(f'row: {row_num}')
                        if row_num >= max_row:
                            print('\n\nFINISHED')
                            quit()
                        
                        row_num += 1
            
            url = data.get('next')
            #reached end
            if not url:
                break
            
            count += len(people)
            print(f'On person {count}')
            
        print('\n\nFINISHED')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-max', type = float, default = float('inf'))
    args = parser.parse_args()
    main(args.max)