# parser
import js2py
import re


header = 'function $() {'
footer = 'return {0};}}'

def parse_file(page, mod_name, url):
    model = ''
    found_model = False
    count = 0
    sku_list = []
    with open(page, 'r') as file:
        for line in file:
            # add line if token is found
            if found_model:
                # look for end token
                search_obj = re.search(r'FUNCTION TOKEN \((.+)\)', line)
                if search_obj:
                    found_model = False
                    model_id = search_obj.group(1)
                    model += footer.format(model_id)

                    f = js2py.eval_js(model)
                    product = f()

                    # process model
                    name = 'nsCover'

                    # SKU = name-widthxproj-motor-lights

                    # base sets in inch
                    widths = [120, 132, 144, 156, 168, 180, 192, 204, 216, 228, 240]

                    count = 0
                    for width in widths:

                        # print i
                        count += 1

                        # create id
                        id = '{name}-{width}'.format(name=name, width=width)

                        # get base price
                        price = 0.0
                        base_key = '{0}-{1}'.format(name, width)
                        for element in product['sku']:
                            if product['sku'][element]['skucode'] == base_key:
                                price = product['sku'][element]['skuprice']
                                break

                        else:
                            print 'WARNING: base key {0} not found'.format(base_key)
                            # sys.exit(1)

                        # create sku
                        sku = {}
                        sku['id'] = id
                        sku['price'] = float('{:.2f}'.format(price))
                        sku['url'] = url.format(mod_name)

                        sku_list.append(sku)

                    return sku_list

                # add line
                model += line

            else:
                # look for start token
                search_obj = re.search(r'FUNCTION TOKEN \((.+)\)', line)
                if search_obj:
                    found_model = True
                    model_id = search_obj.group(1)
                    print 'Found function: model {0}'.format(model_id)
                    model = header #.format(model_id)

            count += 1

    return sku_list


