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

                    #model
                    navi = product[0]

                    # process model
                    name = 'Navigloo'
                    kit_price = product[1]

                    # SKU = name-widthxlength-tarp-kit

                    # base sets in inch
                    sizes = [(8,14),  (14,17), (18,24), (25,30), (31,35), (36,40)]
                    add_tarp = [0, 1]
                    add_kit = [0, 1]

                    count = 0
                    for i in itertools.product(sizes, add_tarp, add_kit):

                        # get variables
                        width = i[0][0]
                        length = i[0][1]
                        tarp = i[1]
                        kit = i[2]

                        count += 1

                        # create id
                        id = '{name}-{width}-{length}-{tarp}-{kit}'.format(name=name, width=width,
                                                                          length=length,
                                                                          tarp=tarp, kit=kit)

                        # get base price
                        price = 0.0
                        base_key = '{0}-{1}-{2}'.format(name, width, length)
                        tarp_price = 0.0
                        for element in navi['sku']:
                            if navi['sku'][element]['skucode'] == base_key:
                                price = navi['sku'][element]['skuprice']
                                tarp_price = navi['sku'][element]['tarp']
                                break

                        else:
                            print 'WARNING: base key {0} not found'.format(base_key)
                            # sys.exit(1)

                        # check for options and add to price
                        if tarp == 1:
                            price += tarp_price

                        # add a door
                        if kit == 1:
                            price += kit_price

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


