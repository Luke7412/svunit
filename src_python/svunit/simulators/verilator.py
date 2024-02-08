

def generate_commands(args):
    commands = []

    # add the vdhl switches if necessary
    cmd = ['verilator', '--binary', '--top-module' 'testrunner']
    commands.append(cmd)




