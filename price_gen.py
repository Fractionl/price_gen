import js2py
import json
import re
import importlib
import os
import shutil
import time
from zipfile import ZipFile

outputs = ['sh', 'pc']
dirs = ['../sh-bootstrap/assets/js/', '../patioconcepts/assets/js/']
urls = ['https://screen-house.com/buy/{0}.json', 'https://patioconcepts.ca/buy/{0}.json']
pages = [
    ['buy-replacementtops.js',
     ('screen.html', '../sh-bootstrap/screen-porch-kits/'),
    # 'buy-1100.js',
    # 'buy-1500.js',
    # 'buy-2700.js',
    # 'buy-3100.js',
    # 'buy-3300.js',
    # 'buy-3500.js',
    # 'buy-3700.js',
    # 'buy-4100.js',
    # 'buy-4300.js',
    # 'buy-4500.js',
    # 'buy-4700.js',
    # 'buy-5500.js',
    # 'buy-5700.js',
    # 'buy-athena.js',
    # 'buy-europa.js',
    # 'buy-slim.js',
    # 'buy-nushade.js',
    # 'buy-azul.js',
    'buy-prestige.js',
    'buy-steelcarports.js',
    'buy-polaria.js',
    'buy-hoodcover.js',
    'buy-softcover.js',
    'buy-solarshade.js',
    'buy-softtops.js',
    'buy-enclosures-trailers.js',
    'buy-navigloo.js',
    'buy-enclosures.js',
    'buy-flatpancovers.js',
    'buy-insulatedcovers.js',
    'buy-wpancovers.js'
    ],

    ['buy-athena.js',
     'buy-europa.js',
     'buy-slim.js',
     'buy-prestige.js',
     'buy-solarshade.js',
     'buy-softtops.js',
     'buy-enclosures-trailers.js']
]

def logging(message):
    # print
    print message

    # log
    log.write(message + '\n')

now = time.strftime('%Y%m%d-%H%M%S')

# process
for i, output in enumerate(outputs):
    # check for output directory, delete adn recreate
    if os.path.exists(output):
        print 'Output directory detected, deleting...'
        shutil.rmtree(output)

    if not os.path.exists(output):
        print 'Creating output directory'
        os.mkdir(output)

    # open log file
    log_file = '{0}/log.txt'.format(output)
    log = open(log_file, 'w')

    url = urls[i]
    dir = dirs[i]

    logging('----------------------------------------------------------------------------------')
    logging('Processing output "{0}"'.format(output))
    logging('----------------------------------------------------------------------------------')

    # open page
    for page in pages[i]:
        logging('----------------------------------------------------------------------------------')
        # detect
        try:
            path = dir + page

            logging('Processing page {0}'.format(path))
            search_obj = re.search(r'buy-(.+)\.js', page)
            if not search_obj:
                logging('No parser name can be extracted from the page name. Must be in buy-[parser].js format')
                exit(1)

        except:
            path = page[1] + page[0]
            logging('Path override detected. Using page {0} and path {1}'.format(page[0], page[1]))

            logging('Processing page {0}'.format(path))
            search_obj = re.search(r'(.+)\..+', page[0])
            if not search_obj:
                logging('No parser name can be extracted from the page name {0}'.format(page[0]))
                exit(1)

        mod_name = search_obj.group(1)

        # module substitution
        if mod_name == '1100' or mod_name == '1500' or mod_name == '2700' or mod_name == '3100' or \
           mod_name == '3300' or mod_name == '3500' or mod_name == '3700' or mod_name == '4100' or \
           mod_name == '4300' or mod_name == '4500' or mod_name == '4700' or mod_name == '5500' or \
           mod_name == '5700':
            import_mod_name = 'model_x'
            logging('Switching import module to {0}'.format(import_mod_name))
        elif mod_name == 'insulatedcovers' or mod_name == 'flatpancovers' or mod_name == 'wpancovers':
            import_mod_name = 'enclosures'
            logging('Switching import module to {0}'.format(import_mod_name))
        else:
            import_mod_name = mod_name

        try:
            module = importlib.import_module('parser.{0}'.format(import_mod_name))
            parser = getattr(module, 'parse_file')

        except:
            logging('No parse module can be found with the name {0}'.format(import_mod_name))
            exit(1)

        logging('Importing module {0}'.format(import_mod_name))

        sku_list = parser(path, mod_name, url)

        # check for duplicates
        logging('Checking for SKU duplicates...')
        check = []
        for sku in sku_list:
            id = sku['id']
            if id in check:
                logging('ERROR: duplicate SKU "{0}" found in file {1}'.format(id, page))
            else:
                check.append(id)

        # create JSON
        if sku_list:
            with open('{0}/{1}.json'.format(output, mod_name), 'w') as json_file:
                json.dump(sku_list, json_file, indent=4, sort_keys=True)

            # print total variant count
            logging('Total number of SKU variants = {0}'.format(len(sku_list)))
            logging('Exporting SKU list to {0}.json'.format(mod_name))

        else:
            logging('WARNING: No SKUs were found in file {0}'.format(path))

        logging('----------------------------------------------------------------------------------')

    log.close()

    zip_name = '{0}_{1}.zip'.format(output, now)
    print 'Creating Zip file {0}'.format(zip_name)
    with ZipFile(zip_name, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(output):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)

    shutil.move(zip_name, '{0}/{1}'.format(output, zip_name))