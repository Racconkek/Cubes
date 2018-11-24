from argparse import ArgumentParser

class ArgParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self, prog="Cubes Game", description="Play in cubes: click on part of field "
                                                                    "and highlighted part will disappear "
                                                                    "and you will get points. "
                                                                    "You can see how many points you"
                                                                    " can get and how many you already have.")
        self.add_argument("-s", "--size", action="store", nargs="?", default="small",
                            choices=['small', 'middle', 'large'], help="Sets field's size")
        self.add_argument("-c", "--colors", action="store", nargs="?", default="2",
                            choices=['2', '3', '4'], help="Sets amount of colors")
        self.add_argument("-r", "--records", action="store_true", help="Shows record's table")
        self.add_argument("-n", "--name", action="store", nargs=1, default="DefaultName", help="Write here you name")

    def parse_arguments(self):
        arg = self.parse_args()
        return self.get_settings(arg)

    def get_settings(self, arg):
        board_size = 200
        colors_count = 2
        show_records = arg.records
        name = arg.name[0]
        if arg.size == 'small':
            board_size = 200
        elif arg.size == 'middle':
            board_size = 400
        elif arg.size == 'large':
            board_size = 600
        if arg.colors == '2':
            colors_count = 2
        elif arg.colors == '3':
            colors_count = 3
        elif arg.colors == '4':
            colors_count = 4
        return board_size, colors_count, show_records, name