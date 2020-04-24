# parser
import js2py
import re
import itertools


header = 'function $() {'
footer = 'return [{0}];}}'

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

                    prestige = product[0]

                    # process model
                    name = 'Prestige'
                    fabric_price = product[1]
                    opt1_price = product[2]
                    opt2_price = product[3]
                    opt3_price = product[4]

                    # SKU = name-widthxproj-motor-lights

                    # base sets in inch
                    #projections = [132, 144, 168]
                    #widths = [132, 144, 168, 192]

                    widths = [132, 144, 168]
                    projections = [132, 144, 168, 192]
                    add_fabric = [0, 1]
                    add_opt1 = [0, 1]
                    add_opt2 = [0, 1]
                    add_opt3 = [0, 1]
                    #add_shipping = [0,1,2]

                    count = 0
                    for i in itertools.product(projections, widths, add_fabric, add_opt1, add_opt2, add_opt3):

                        # get variables
                        projection = i[0]
                        width = i[1]
                        fabric = i[2]
                        opt1 = i[3]
                        opt2 = i[4]
                        opt3 = i[5]
                        #shipping = i[6]

                        # rules
                        #if (projection <= width):
                        if (width <= projection):

                                # print i
                                count += 1

                                # create id
                                id = '{name}-{width}x{proj}-{fabric}-{opt1}-{opt2}-{opt3}'.format(name=name, width=width,
                                                                                  proj=projection,
                                                                                  fabric=fabric, opt1=opt1,
                                                                                  opt2=opt2, opt3=opt3)

                                # get base price
                                price = 0.0
                                base_key = '{0}-{1}x{2}'.format(name, width, projection)
                                for element in prestige['sku']:
                                    if prestige['sku'][element]['skucode'] == base_key:
                                        price = prestige['sku'][element]['skuprice']
                                        break

                                else:
                                    print 'WARNING: base key {0} not found'.format(base_key)
                                    # sys.exit(1)

                                # check for options and add to price
                                # motor
                                if fabric == 1:
                                    price += fabric_price

                                if opt1 == 1:
                                    price += opt1_price

                                if opt2 == 1:
                                    price += opt2_price

                                if opt3 == 1:
                                    price += opt3_price

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


