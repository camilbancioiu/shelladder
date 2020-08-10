# Shell adder
`shelladder` enables you to call Python functions as if they were Bash
functions or commands.

Calling `print()` in your Python function is directly sent to `stdout`. You can
pipe input into your functions, which can read it using `sys.stdin`.

Also, all the arguments are available in `sys.argv`, so you can use
`argparse.ArgumentParser` objects directly.

Named after the common European adders, which have a zigzag pattern on their
backs - just like what `shelladder` does, moving you from Bash into Python then
back into Bash, back and forth.


# How it works
You begin by writing your Python functions in a module, e.g. `myfunctions.py`.
This module _must not_ contain the usual construct `if __name__ == "__main__"`.
Just write the functions, because `shelladder` will handle their calling.

Let's say you would like a Python function called `printdir()` to be accessible
to you in the terminal, as if it were a normal command. You would write a file
containing this:

```python
import os

# export
def printdir():
    print(os.getcwd())
```

Note the `# export` line just above the line `def printdir():`. Adding `#
export` before defining a function marks it for export into Bash, so
`shelladdder` knows you want to call it. Function definitions that don't have
the `# export` mark will remain "private" to the module, i.e. they can be
called by other exported functions, but not from Bash.

Once you're happy with your Python functions, save your file. For example,
`myfunctions.py` in your current folder. Now run this command:

```
python3 /some/where/shelladder/shelladder.py myfunctions.py
```

Now `shelladder` has created a new dot-folder in your `$HOME` called
`.shelladder`, where it will deploy your `myfunctions.py` module (with minor
modifications!), and it will create a companion Bash script, called
`myfunctions.sh`.

And by sourcing `myfunctions.sh` into your shell, you gain access to
all the `# export`-ed functions in `myfunctions.py`. Neat, right? Take a look at
these two generated files, to see what happened.

Now try sourcing:

```
source ~/.shelladder/myfunctions.sh
```

Try calling `printdir` now!

```
printdir
/what/ever/your/dir/is
```


# A shortcut
Observe that `shelladder` will print the location of this companion Bash
script, which allows you to do everything in one command:

```
source $(python3 /some/where/shelladder/shelladder.py myfunctions.py)
```

Just make sure you run the above command everytime you edit `myfunctions.py`.

_You need to specify the path to `shelladder.py`, because it's just a Python
script, not an executable._ Or add an alias to `~/.bashrc`:

```
alias adder="python3 /some/where/shelladder/shelladder.py"
```

Now you can do `adder myfunctions.py` anytime, from anywhere, hassle-free:

```
source $(adder myfunctions.py)
printdir
/what/ever/your/dir/is
```
