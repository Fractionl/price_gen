# parser
import sys
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
                    vjPatioPlus = product[0]
                    windows = product[1]
                    panels = product[2]

                    # upgrade cost
                    frame_cost = product[3]
                    front_cost = product[4]
                    back_cost = product[5]
                    door_cost = product[6]

                    # SKU = VJP - width - proj - type - upgradeFrame - changeBack - changeFront - addDoor

                    # base sets in inch
                    types = [0, 1, 2]
                    projections = [90, 120, 135]
                    widths = [120, 135, 180, 225, 270, 315, 360, 405, 444]
                    upgrade_frame = [0, 1]
                    upgrade_back = [0, 1]
                    upgrade_front = [0, 1]
                    add_door = [0, 1]

                    count = 0
                    sku_list = []
                    for i in itertools.product(types, projections, widths, upgrade_frame, upgrade_back, upgrade_front,
                                               add_door):

                        # get variables
                        type = i[0]
                        projection = i[1]
                        width = i[2]
                        frame = i[3]
                        back = i[4]
                        front = i[5]
                        door = i[6]

                        # print i
                        count += 1

                        # Get panel count for upgrades
                        # base count for the projections
                        num_panels = 0
                        if projection == 90:
                            num_panels = 4
                        elif projection == 120 or projection == 135:
                            num_panels = 6
                        else:
                            print 'invalid projection'.format(projection)
                            sys.exit(1)

                        # add panels for the width
                        if width == 120:
                            num_panels += 3
                        elif width == 135:
                            num_panels += 3
                        elif width == 180:
                            num_panels += 4
                        elif width == 225:
                            num_panels += 5
                        elif width == 270:
                            num_panels += 6
                        elif width == 315:
                            num_panels += 7
                        elif width == 360:
                            num_panels += 8
                        elif width == 405:
                            num_panels += 9
                        elif width == 444:
                            num_panels += 10
                        else:
                            print 'invalid width'.format(width)
                            sys.exit(1)

                        # create id
                        id = 'VJP-{width}x{proj}-{type}-{frame}-{back}-{front}-{door}'.format(width=width,
                                                                                              proj=projection,
                                                                                              type=type,
                                                                                              frame=frame,
                                                                                              back=back,
                                                                                              front=front,
                                                                                              door=door)

                        # get base price
                        price = 0.0
                        base_key = 'vjPatioPlus-{0}x{1}'.format(projection, width)
                        for element in vjPatioPlus['sku']:
                            if vjPatioPlus['sku'][element]['skucode'] == base_key:
                                price = vjPatioPlus['sku'][element]['skuprice']
                                break

                        else:
                            print 'WARNING: base key {0} not found'.format(base_key)
                            # sys.exit(1)

                        # check for options and add to price
                        # windows
                        if type == 1:
                            win_key = 'objWindows-{0}x{1}'.format(projection, width)
                            for element in windows['sku']:
                                if windows['sku'][element]['skucode'] == win_key:
                                    price += windows['sku'][element]['skuprice']
                                    break

                            else:
                                print 'WARNING: window key {0} not found'.format(win_key)
                                # sys.exit(1)

                        # panels
                        if type == 2:
                            panel_key = 'objPanels-{0}x{1}'.format(projection, width)
                            for element in panels['sku']:
                                if panels['sku'][element]['skucode'] == panel_key:
                                    price += panels['sku'][element]['skuprice']
                                    break

                            else:
                                print 'WARNING: panel key {0} not found'.format(panel_key)
                                # sys.exit(1)

                        # frame upgrade
                        if frame == 1:
                            price += (num_panels * frame_cost)

                        # front height upgrade
                        if front == 1:
                            price += (num_panels * front_cost)

                        # back upgrade (one time cost)
                        if back == 1:
                            price += back_cost

                        # add a door
                        if door == 1:
                            price += door_cost

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


