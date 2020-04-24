# parser
import js2py
import re
import itertools


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
                    name = 'SolarShade'

                    # SKU = name-widthxproj-motor-lights

                    # base sets in inch
                    widths = [x for x in range(36, 186, 6)]
                    types = [0, 1, 2]

                    count = 0
                    for i in itertools.product(widths, types):

                        # get variables
                        width = i[0]
                        type = i[1]

                        count += 1

                        # create id
                        id = '{name}-{width}-{type}'.format(name=name, width=width, type=type)

                        # get base price
                        price = 0.0
                        base_key = '{0}-{1}'.format(name, width)
                        motor_price = 0.0
                        solar_price = 0.0
                        for element in product['sku']:
                            if product['sku'][element]['skucode'] == base_key:
                                price = product['sku'][element]['skuprice']
                                motor_price = product['sku'][element]['motor']
                                solar_price = product['sku'][element]['solar']
                                break

                        else:
                            print 'WARNING: base key {0} not found'.format(base_key)
                            # sys.exit(1)

                        # check for options and add to price
                        # motor
                        if type == 1:
                            price += motor_price

                        # add a door
                        if type == 2:
                            price += solar_price

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


