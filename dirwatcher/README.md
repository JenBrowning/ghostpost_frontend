This program searches a directory for a specific string within a given file type.

To initiate search follow the following command line scheme:

"python dirwatcher.py magictext extention directory pollinginterval"

An example I have been using is searching directories created in this folder: "python dirwatcher.py "string" '.txt' searchhere 2"

The arguments are positional, and, the polling interval is optional and defaults to 1.

After files with that given extension are added or deleted, they are logged as info.

If a file is detected there is info. If a file is deleted there is a info. If a directory is deleted/does not exist there is a warning.

There is a running message to assure the program is searching for changes, this can be removed, the instructions do not mention whether or not to log this, but this gives the appearance it is constantly working.

There is a generic state held on the global level.