# parser
import re


def parse_file(page, mod_name, url):
    found_sku = False
    found_price = False
    count = 0
    sku_list = []
    with open(page, 'r') as file:
        for line in file:
            # remove any ',' as they are in some pricing
            line = line.replace(',', '')

            # add line if token is found
            if found_price:
                # look for price
                # $('#buy-button').attr('data-item-id', 'PatioPlus-GP-3300-07');
                #search_obj = re.search(r'\$\(\'#buy-button\'\)\.attr\(\'data-item-id\', \'(.+)\'\)', line)
                search_obj = re.search(r'\$\(\'#buy-button\'\)\.attr\(\'data-item-id\' \'(.+)\'\)', line.replace(',', ''))
                if search_obj:
                    found_price = False
                    sku_name = search_obj.group(1)

                    # create sku
                    sku = {}
                    sku['id'] = '{0}'.format(sku_name)
                    sku['price'] = float(sku_price)
                    sku['url'] = url.format(mod_name)

                    sku_list.append(sku)

            elif found_sku:
                # look for price
                # $("#result_price").html("$2,326.00");
                search_obj = re.search(r'\$\("#result_price"\)\.html\("\$(\d+\.\d+)"\)', line)
                if search_obj:
                    found_price = True
                    sku_price = search_obj.group(1)

            else:
                # look for sku_id
                search_obj = re.search(r'if \(ifWidth == "(.+)"\)', line)
                if search_obj:
                    found_sku = True
                    sku_id = search_obj.group(1)

            count += 1

    return sku_list
