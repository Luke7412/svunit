

def generate_commands(args):
    commands = []

    # add the vdhl switches if necessary
    cmd = [args.simulator, '-l', f'{args.logfile}']
    if args.vhdlfile:
        cmd.extend(['-f', f'{args.vhdlfile}'])


    # add the uvm switches
    if args.uvm:
        cmd.append('-uvm')
        args.defines.append('RUN_SVUNIT_WITH_UVM')


    # add the filelists and defines
    for file in args.filelists:
        cmd.extend(['-f', f'{file}'])
    cmd.extend(['-f', '.svunit.f'])


    # defines
    for define in args.defines:
        cmd.append(f'+define+{define}')


    cmd.extend([*args.compileargs, *args.elabargs, *args.simargs, '-top', 'testrunner'])


    # add filter
    if args.filter:
        cmd.append(f"+SVUNIT_FILTER={args.filter}")
    
    commands.append(cmd)
    return commands