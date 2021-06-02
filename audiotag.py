#!/usr/bin/python3

# Standard library imports
from sys import argv, stderr

# Third-party imports
try:
	import mutagen
except ModuleNotFoundError:
	print("Error loading Mutagen - ensure that Mutagen is installed and try again", file=stderr)
	exit(1)

if len(argv) < 2:
	print(f"Usage: {argv[0]} FILE", file=stderr)
	exit(1)

supportedTypes = ["flac"]
filetype = argv[1].split(".")[-1].casefold()

if filetype == "flac":
	from mutagen.flac import FLAC
	song = FLAC(argv[1])
else:
	print("Error: unsupported filetype. Supported types are: {supportedTypes}", file=stderr, sep=" ")
	exit(1)


helpstrs = {"help": "help [COMMAND]: display help for COMMAND, or a list of " \
		"accepted commands if none is given", "addTag": "addTag TAG "\
		"[VALUE]: set new tag TAG to VALUE. If no VALUE is supplied, "\
		"the user will be prompted for one.", "save": "save: save "\
		"changes made to the audio file", "quit": "quit: terminate "\
		"the program", "listTags": "listTags: list the song's tags as "\
		"key-value pairs", "deleteTag": "deleteTag TAG VALUE: remove "\
		"the occurence of TAG with value VALUE from the song's "\
		"metadata. VALUE is case-sensitive, while TAG is not."}

def printHelp(*args):

	if (len(args) == 0):
		print(*helpstrs.keys(), sep="    ")
		return 0
	
	for arg in args:
		print(helpstrs[arg])
		
	return 0


# Forward declaration
song = None

def saveSong(*args):

	song.save()
	return 0

def addTag(*args):

	if (len(args) < 1 or len(args) > 2):
		print("Usage: addTag TAG [VALUE]")
		return 1
	
	if (len(args) == 1):
		val = input("Value: ")
	else:
		val = args[1]
	
	song.tags.append((args[0], val))

def listTags(*args):

	for pair in song.tags:
		print(f"{pair[0]}: {pair[1]}")
	return 0

def deleteTag(*args):

	if (len(args) != 2):
		print("Usage: deleteTag TAG VALUE")
		return 1
	
	key = args[0].upper()
	value = args[1]
	try:
		song.tags.remove((key, value))
		return 0
	
	except ValueError:
		print("Tag not found", file=stderr)
		return 1
	

# Keys are accepted commands, values are the internal functions that we call
commands = {"save": saveSong, "help": printHelp, "addTag": addTag, "listTags":
		listTags, "deleteTag": deleteTag}

# Input loop
while (True):

	# Get command string
	raw = input(": ")

	# Split args at spaces
	args = raw.split(" ")

	# First arg is command entered
	cmd = args.pop(0)

	if (cmd == "quit"):
		break

	# If invalid command entered, print help message and return to start of
	# loop
	if (cmd not in commands.keys()):
		print(f"Error: {cmd}: invalid command. Run `help` for help.",
		file=stderr)
		continue
	
	# If we have a valid command, pass args to the command associated with
	# it.
	commands[cmd](*args)
