# "Name": int(request.args.get('name')),
#         "Environment": int(request.args.get('environment')),
#         "Type": int(request.args.get('type')),
#         "Code": int(request.args.get('code'))


def run(name, env, typ, code):
    print "Running test application!"
    total = name + env + typ + code
    path = 0
    if total > 2:
        path += 1
        if env >= 0:
            path += 1
            if typ == 0:
                path += 1
                if code == 0:
                    path += 1
        if env == 1:
            path += 1
            if typ == 0:
                path += 1
                if code >= 1:  # name = 5, env = 1, typ = 0, code = 1
                    path += 1
                else:
                    return calculate_input_status(path) # name = 5, env = 1, typ = 0, code = 0
        if typ == 1:
            path += 1
            return calculate_input_status(path)
    if total > 3:
        path += 1
        if env >= 1:
            path += 1
            if typ == 0:
                path += 1
                if code == 0:
                    path += 1
        if env == 1:
            path += 1
            if typ == 0:
                path += 1
                if code == 1:   # name = 5, env = 1, typ = 0, code = 1
                    path += 1
                else:
                    return calculate_input_status(path)  # name = 5, env = 1, typ = 0, code = 2
        if typ == 1:
            path += 1
            return calculate_input_status(path)

    if total > 4:
        path += 1
        if env > 1:
            path += 1
            if typ == 0:
                path += 1
                if code == 0:
                    path += 1
        if env == 1:
            path += 1
            if typ == 0:
                path += 1
                if code == 0:
                    path += 1
                    return calculate_input_status(path)
        if typ == 1:
            path += 1
            return calculate_input_status(path)

    if total > 5:
        path += 1
        return calculate_input_status(path)
    return calculate_input_status(path)


def calculate_input_status(path):
    print "PATH IS:" + str(path)
    if path < 3:
        return 0
    if path < 10:
        return 1
    return 2
