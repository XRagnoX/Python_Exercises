OPTIONS: list[str] = ['']

def get_options():

    print('1. Scan Neighbours')
    print('2. Scan Routers')
    print('3. IPv4 Scan')
    print('4. Port Scan')

def intro():

    opt = ''

    while(True):
        if opt == 1:
            print('1. Scan Neighbours')
        elif opt == 2:
            print('2. Scan Routers')
        elif opt == 3:
            print('3. IPv4 Scan')
        elif opt == 4:
            print('4. Port Scan')
        elif opt == 5 or opt == '-h' or opt == '--help':
            get_options()
        elif opt == 6:
            print('Gracefull Exit.')
            return


