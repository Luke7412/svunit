


def generate_commands(args):
    commands = []

    ### LIBRARY COMMAND
    # Create library
    cmd = ['vlib', 'work']
    commands.append(cmd)

    ### COMPILATION COMMAND
    # Compile VHDL sources
    if args.vhdl_file:
        cmd = ['vcom', '-work', 'work', '-f', f'{args.vhdl_file}']
        commands.append(cmd)

    # Compile (System)Verilog sources
    cmd = ['vlog', '-l', 'compile.log']

    for file in args.filelists:
        cmd.extend(['-f', f'{file}'])
    cmd.extend(['-f', '.svunit.f'])

    # Add the uvm switches if necessary
    if args.uvm:
        raise Exception('Not Supported for this simulator')
        # args.defines.append('RUN_SVUNIT_WITH_UVM')

    # Add defines
    for define in args.defines:
        cmd.append(f'+define+{define}')

    if args.compileargs:
        cmd.extend(args.compileargs)
    commands.append(cmd)

    ### SIMULATION COMMAND
    # Add simulator arguments
    if not any([x in args.simargs for x in ['-gui', '-c', '-i']]):
        args.simargs.append('-c')

    cmd = ['vsim', *args.simargs, '-lib', 'work', '-do', 'run -all; quit', '-l', f'{args.logfile}', 'testrunner']

    # Add SVUnit filter
    cmd.append(f"+SVUNIT_FILTER={args.filter}")
    commands.append(cmd)

    return commands
