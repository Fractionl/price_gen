# parser
import re

def parse_file(page, mod_name, url):

    # get sku_name
    count = 0
    sku_list = []
    with open(page, 'r') as file:
        for line in file:
            # remove any ',' as they are in some pricing
            line = line.replace(',', '')

            # look for price
            # <option value="77.50" data-sku="Pool-Patio-18x14-24">24in Width</option>
            search_obj = re.search(r'<optionvalue="(\d+\.\d+)"data-sku="(.+)">', line.replace(' ', ''))
            if search_obj:
                price = search_obj.group(1)
                sku_name = search_obj.group(2)

                # create sku
                sku = {}
                sku['id'] = '{0}'.format(sku_name)
                sku['price'] = float(price)
                sku['url'] = url.format(mod_name)

                sku_list.append(sku)

            count += 1

    return sku_list
