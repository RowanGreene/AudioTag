#!/usr/bin/python3

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
		print("Tag not found", file=sys.stderr)
		return 1
	
# Import system functionality
import sys

# Import mutagen flac functionality, or fail gracefully.
try:
	from mutagen.flac import FLAC, Picture
except:
	print("Error loading required library - run `pip3 install mutagen` and try again", file=sys.stderr)
	exit(1)

# Because there is no argc
argc = len(sys.argv)

# For consistency with argc
argv = sys.argv

if (argc < 2):
	print(f"Usage: {argv[0]} FILE", file=sys.stderr)
	exit(1)

# If we aren't given a flac file, print an error message and exit
if (argv[1].split(".")[-1].casefold() != "flac"):
	print("Error: unsupported file type.", file=sys.stderr)
	exit(1)

# Load song
song = FLAC(argv[1])

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
		file=sys.stderr)
		continue
	
	# If we have a valid command, pass args to the command associated with
	# it.
	commands[cmd](*args)
