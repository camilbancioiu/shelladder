# Shelladder
`shelladder` enables you to call Python functions as if they were Bash
functions or normal commands.


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
`addertest.py` in your current folder. Now run this command:

```
python3 /some/where/shelladder/shelladder.py addertest.py
```

What `shelladder` does is that it creates a new folder in your `$HOME` called
`.shelladder`, where it will deploy your `addertest.py` module (with minor
modifications!), and it will create a companion Bash script, called
`addertest.sh`. By sourcing `addertest.sh` into your shell, you gain access to
all the `# export`-ed functions in `addertest.py`. Neat, right?

Try it:

```
source ~/.shelladder/addertest.sh
```

Observe that `shelladder` will print the location of this companion Bash
script, which allows you to do everything in one command:

```
source $(python3 /some/where/shelladder/shelladder.py addertest.py)
```

Just make sure you run the above command everytime you edit `addertest.py`.

_You need to specify the path to `shelladder.py`, because it's just a Python
script, not an executable._ Or add an alias to `~/.bashrc`:

```
alias adder="python3 /some/where/shelladder/shelladder.py"
```

Now you can do `adder addertest.py` anytime, from anywhere.
