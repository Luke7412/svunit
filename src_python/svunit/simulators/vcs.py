

def generate_commands(args):
    commands = []

    cmd = [args.simulator, '-R', '-sverilog', '-l', f'{args.logfile}']
    
    # Add (System)Verilog sources
    for file in args.filelists:
        cmd.extend(['-f', f'{file}'])

    # Add VHDL sources
    if args.vhdl_file:
        cmd.extend(['-f', args.vhdl_file])

    # Add SVUnit sources
    cmd.extend(['-f', '.svunit.f'])

    # add the uvm switches
    if args.uvm:
        cmd.append('-ntb_opts uvm')
        args.defines.append('RUN_SVUNIT_WITH_UVM')

    # Add defines
    for define in args.defines:
        cmd.append(f'+define+{define}')

    cmd.extend([*args.compileargs, *args.simargs, '-top', 'testrunner'])

    cmd.append(f"+SVUNIT_FILTER={args.filter}")
    commands.append(cmd)
    
    return commands