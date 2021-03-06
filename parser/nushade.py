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

                    # process model
                    name = 'NuShade'
                    opt1_name = 'nsWgWithAwning'
                    opt2_name = 'nsRMK'

                    # SKU = name-widthxproj-motor-lights

                    # base sets in inch
                    projections = [96, 120, 144]
                    widths = [132, 144, 156, 168, 180, 192, 204, 216, 228, 240]
                    add_motor = [0, 1]
                    add_opt1 = [0, 1]
                    add_opt2 = [0, 1]
                    add_opt3 = [0, 1]

                    count = 0
                    for i in itertools.product(projections, widths, add_motor, add_opt1, add_opt2, add_opt3):

                        # get variables
                        projection = i[0]
                        width = i[1]
                        motor = i[2]
                        opt1 = i[3]
                        opt2 = i[4]
                        opt3 = i[5]

                        # rules
                        if ((projection == 96 and width >= 132) or (projection == 120 and width >= 144) or (
                                projection == 144 and width >= 168)):

                                # print i
                                count += 1

                                # create id
                                id = '{name}-{width}x{proj}-{motor}-{opt1}-{opt2}-{opt3}'.format(name=name, width=width,
                                                                                  proj=projection,
                                                                                  motor=motor, opt1=opt1,
                                                                                  opt2=opt2, opt3=opt3)

                                # get base price
                                price = 0.0
                                base_key = '{0}-{1}x{2}'.format(name, width, projection)
                                motor_price = 0.0
                                for element in product[0]['sku']:
                                    if product[0]['sku'][element]['skucode'] == base_key:
                                        price = product[0]['sku'][element]['skuprice']
                                        motor_price = product[0]['sku'][element]['motor']
                                        break

                                else:
                                    print 'WARNING: base key {0} not found'.format(base_key)
                                    # sys.exit(1)

                                # check for options and add to price
                                # motor
                                if motor == 1:
                                    price += motor_price

                                if opt1 == 1:
                                    opt1_price = 0.0
                                    opt_id = '{name}-{width}'.format(name=opt1_name, width=width)
                                    for element in product[1]['sku']:
                                        if product[1]['sku'][element]['skucode'] == opt_id:
                                            opt1_price = product[1]['sku'][element]['skuprice']
                                            break

                                    else:
                                        print 'WARNING: base key {0} not found'.format(opt_id)

                                    price += opt1_price

                                if opt2 == 1:
                                    opt2_price = 0.0
                                    opt_id = '{name}-{width}'.format(name=opt2_name, width=width)
                                    for element in product[2]['sku']:
                                        if product[2]['sku'][element]['skucode'] == opt_id:
                                            opt2_price = product[2]['sku'][element]['skuprice']
                                            break

                                    else:
                                        print 'WARNING: base key {0} not found'.format(opt_id)

                                    price += opt2_price

                                if opt2 == 1:
                                    price += product[3]

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


