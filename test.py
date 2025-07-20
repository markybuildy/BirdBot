class BirdCount:
    def __init__(self):
        self.birds = {}
        self.commands = ['add','done','help','print','remove','rename', 'set']
        self.cmdhelp = {
            "add": "Add birds.",
            "done": "Complete session.",
            "help": "Show this help menu.",
            "print": "Print current checklist.",
            "remove": "Remove birds.",
            "rename": "Rename a bird to something else.",
            "set": "Set a bird's quantity."
        }
        self.formats = {
            "add": '"add <bird_name> <count>" or "<bird_name> <count>"',
            "help": 'help <command>',
            "remove": 'remove <bird_name> <count>',
            "rename": 'rename <old_name> <new_name>',
            "done": 'done',
            "print": 'print',
            "set": 'set <bird_name> <count>'
        }


    def add_bird(self, bird_name, count):
        if bird_name in self.birds:
            self.birds[bird_name] += count
            print("Added " + str(count) + "x " + bird_name + ". " + str(self.birds[bird_name]) + " seen total.")
        else:
            self.birds[bird_name] = count
            print("Added " + str(count) + "x " + bird_name + ".")

    def remove_bird(self, bird_name, count):
        if bird_name in self.birds:
            if count > self.birds[bird_name]:
                print("Not enough birds to remove.")
            else:
                self.birds[bird_name] -= count
                print("Removed " + str(count) + "x " + bird_name + ". " + str(self.birds[bird_name]) + " remain.")
                if self.birds[bird_name] == 0:
                    self.birds.pop(bird_name)
        else:
            print('"' + bird_name + '" does not exist.')

    def print_results(self):
        if len(self.birds) != 0:
            for bird in self.birds:
                print(bird + " x" + str(self.birds.get(bird)))
        else:
            print("No birds seen.")

    def rename(self, old_name, new_name):
        if old_name in self.birds:
            if new_name not in self.birds:
                self.birds[new_name] = self.birds[old_name]
                self.birds.pop(old_name)
                print("Renamed " + old_name + " to " + new_name + ".")
            else:
                print('"' + new_name + '" already exists.')
        else:
            print('"' + old_name + '" does not exist.')

    def set(self, bird_name, count):
        if bird_name in self.birds:
            self.birds[bird_name] = count
            print('Set "' + bird_name + '" to ' + str(count) + '.')
        else:
            print('"' + bird_name + '" does not exist.')

    def run(self):
        while True:
            userinput = input()
            segments = userinput.split()

            if len(segments) == 2 and segments[0].lower() not in self.commands:
                if segments[0].isdigit():
                    print("Please enter a valid bird name.")
                else:
                    if segments[1].isdigit():
                        self.add_bird(segments[0], int(segments[1]))
                    else:
                        print("Please use an integer for quantity.")

            elif len(segments) == 2 and segments[0].lower() == "remove":
                if segments[1].lower() in self.birds.keys():
                    self.birds.pop(segments[1].lower())
                    print('Removed ' + segments[1].lower() + '.')
                else:
                    print('"' + segments[1] + '" does not exist.')

            elif len(segments) == 3:
                if segments[0].lower() not in self.commands:
                    print("Please enter a valid command.")

                elif segments[0] != "rename" and not segments[2].isdigit():
                    print("Please use an integer for quantity.")

                elif segments[0].lower() == "add":
                    self.add_bird(segments[1].lower(), int(segments[2]))

                elif segments[0].lower() == "remove":
                    self.remove_bird(segments[1].lower(), int(segments[2]))

                elif segments[0].lower() == "rename":
                    self.rename(segments[1].lower(), segments[2].lower())

                elif segments[0].lower() == "set":
                    self.set(segments[1].lower(), int(segments[2]))

            elif segments[0].lower() == "print":
                self.print_results()

            elif segments[0].lower() == "done":
                self.print_results()
                break

            elif segments[0].lower() == "help":
                if len(segments) == 1:
                    print("List of available commands:")
                    for command in self.cmdhelp:
                        print(command + ": " + self.cmdhelp[command])
                    print('Enter "help <command>" for the format of that specific command.')
                elif len(segments) == 2:
                    if segments[1].lower() in self.formats:
                        print(self.formats[segments[1]])
                    else:
                        print('"' + segments[1] + '" is not a valid command.')





            elif segments[0].lower() not in self.commands:
                print('"' + segments[0] + '" is not a valid command.')
            else:
                print('Please use command in the correct format.')





birdcount_test = BirdCount()
birdcount_test.run()
