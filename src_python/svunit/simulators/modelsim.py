


def generate_commands(args):
    commands = []

    # add the vdhl switches if necessary
    cmd = ['vlib', 'work']
    commands.append(cmd)
    if args.vhdlfile:
        cmd = ['vcom', '-work', 'work', '-f', f'{args.vhdlfile}']
        commands.append(cmd)
    cmd = ['vlog', '-l', 'compile.log']


    # add the uvm switches if necessary
    if args.uvm:
        raise Exception('Not Supported for this simulator')


    # add the filelists and defines
    for file in args.filelists:
        cmd.extend(['-f', f'{file}'])
    cmd.extend(['-f', '.svunit.f'])


    # defines
    for define in args.defines:
        cmd.append(f'+define+{define}')


    if args.compileargs:
        cmd.extend(args.compileargs)
    commands.append(cmd)


    vopt_elabargs = ['-voptargs'] + args.elabargs if args.elabargs else []

    # Add simulator arguments
    if not any([x in args.simargs for x in ['-gui', '-c', '-i']]):
        args.simargs.append('-c')

    cmd = ['vsim', *vopt_elabargs, *args.simargs, '-lib', 'work', '-do', 'run -all; quit', '-l', f'{args.logfile}', 'testrunner']


    # add filter
    if args.filter:
        cmd.append(f'+SVUNIT_FILTER={args.filter}')

    commands.append(cmd)
    return commands
