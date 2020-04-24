# parser
import js2py
import re


header = 'function $({0}_width) {{\nvar thisItemId = \'\';'
footer = 'return [thisItemId, {0}_price];}}'

def process_model(mod_name, url, model, max_width=120):
    sku_list = []
    for width in range(max_width):
        f = js2py.eval_js(model)
        product = f(width)

        # create sku
        sku = {}
        sku['id'] = product[0]
        price = product[1]
        if width > 96:
            price += 120
        sku['price'] = float('{:.2f}'.format(price))
        sku['url'] = url.format(mod_name)

        if sku['price'] != 0:
            sku_list.append(sku)

    # remove duplicates
    sku_list_no_dup = [i for n, i in enumerate(sku_list) if i not in sku_list[n + 1:]]

    return sku_list_no_dup

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

                    # process model
                    sku_list.extend(process_model(mod_name, url, model))

                # add line
                model += line

            else:
                # look for start token
                search_obj = re.search(r'FUNCTION TOKEN \((.+)\)', line)
                if search_obj:
                    found_model = True
                    model_id = search_obj.group(1)
                    print 'Found function: model {0}'.format(model_id)
                    model = header.format(model_id)

            count += 1

    return sku_list