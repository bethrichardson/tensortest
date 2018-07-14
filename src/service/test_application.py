# "Name": int(request.args.get('name')),
#         "Environment": int(request.args.get('environment')),
#         "Type": int(request.args.get('type')),
#         "Code": int(request.args.get('code'))

def run(name, env, type, code):
    print "Running test application!"
    if name == 2:
        return 0
    else:
        return 1

