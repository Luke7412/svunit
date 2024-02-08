

def generate_commands(args):
    commands = []

    # add the vdhl switches if necessary
    if args.vhdlfile:
        cmd = ['xvhdl', '-f', f'{args.vhdlfile}']
        commands.append(cmd)

    cmd = ['xvlog', '--sv', '--log', 'compile.log']


    # add the uvm switches if necessary
    if args.uvm:
        cmd.extend(['--lib', 'uvm'])
        args.defines.append('RUN_SVUNIT_WITH_UVM')


    # add the filelists and defines
    for file in args.filelists:
        cmd.extend(['-f', f'{file}'])
    cmd.extend(['-f', '.svunit.f'])


    # defines
    for define in args.defines:
        cmd.extend(['--define', define])


    cmd.extend(args.compileargs)
    commands.append(cmd)

    cmd = ['xelab', 'testrunner', *args.elabargs]
    commands.append(cmd)

    cmd = ['xsim', *args.simargs, '--R', '--log', 'logfile.log', 'testrunner']


    # add filter
    if args.filter:
        cmd.extend(['--testplusarg', f'+SVUNIT_FILTER={args.filter}'])

    commands.append(cmd)
    return commands