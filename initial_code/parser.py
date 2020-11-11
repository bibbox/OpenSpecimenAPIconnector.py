from generic_parser import entrypoint, EntryPointParameters


def get_arguments():

    args = EntryPointParameters()
    args.add_parameter(name="file",
                       flags=["-f", "--file"],
                       help="First Parameter, the filename of the xml to parse",
                       type=str,
                       required= True,
                       )
    args.add_parameter(name="gen",
                       flags=["-g", "--generate"],
                       help="Generate random participants",
                       type=str,
                       default="default",
                       required=False,
                       )
    return args