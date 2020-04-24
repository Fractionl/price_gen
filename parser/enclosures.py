# parser
import re

def parse_file(page, mod_name, url):

    # get sku_name
    if mod_name == 'insulatedcovers':
        sku_name = 'Insulated'
    elif mod_name == 'flatpancovers':
        sku_name = 'FlatPan'
    elif mod_name == 'wpancovers':
        sku_name = 'WPan'
    else:
        sku_name = 'Enclosure'

    found_sku = False
    count = 0
    sku_list = []
    with open(page, 'r') as file:
        for line in file:
            # remove any ',' as they are in some pricing
            line = line.replace(',', '')

            # add line if token is found
            if found_sku:
                # look for price
                search_obj = re.search(r'\$\("#price"\)\.html\("\$(\d+\.\d+)"\)', line)
                if search_obj:
                    found_sku = False
                    price = search_obj.group(1)

                    # create sku
                    sku = {}
                    sku['id'] = '{0}-{1}'.format(sku_name, sku_id)
                    sku['price'] = float(price)
                    sku['url'] = url.format(mod_name)

                    sku_list.append(sku)


            else:
                # look for sku_id
                search_obj = re.search(r'if \(coverWidth == "(.+)"\)', line)
                if search_obj:
                    found_sku = True
                    sku_id = search_obj.group(1)

            count += 1

    return sku_list
