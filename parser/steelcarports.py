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
                    name = 'ArrowCarport'

                    # SKU = name-widthxproj-opt1

                    # base sets in inch
                    lengths = [180, 240, 288, 348]
                    widths = [120, 144]
                    add_opt1= [0, 1]

                    count = 0
                    for i in itertools.product(lengths, widths, add_opt1):

                        # get variables
                        length = i[0]
                        width = i[1]
                        opt1 = i[2]

                        # rules
                        if (length == 180 and width == 144):
                            continue

                        count += 1

                        # create id
                        id = '{name}-{width}x{len}-{opt1}'.format(name=name, width=width,
                                                                          len=length, opt1=opt1)

                        # get base price
                        price = 0.0
                        base_key = '{0}-{1}x{2}'.format(name, width, length)
                        opt1_price = 0.0
                        for element in product['sku']:
                            if product['sku'][element]['skucode'] == base_key:
                                price = product['sku'][element]['skuprice']
                                opt1_price = product['sku'][element]['winterKit']
                                break

                        else:
                            print 'WARNING: base key {0} not found'.format(base_key)
                            # sys.exit(1)

                        # check for options and add to price
                        if opt1 == 1:
                            if opt1_price == 0:
                                continue
                            else:
                                price += opt1_price

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


