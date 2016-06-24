def args_to_dict(args):

    args = str(args).split('(')[1][:-1]
    args_list = args.split(", ")
    args_dict = {}
    for arg in args_list:
        arg_param = arg.split("=")
        try:
            args_dict[arg_param[0]] = int(arg_param[1])
        except:
            args_dict[arg_param[0]] = arg_param[1][1:-1]
    return args_dict
