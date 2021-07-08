# Laboratory 2 - Shell and Processes
In this lab we extend the implementation of a simple shell, exercising the flow
of process creation, execution, control, and elimination, in the way we learn 
in the classroom.

The required tasks were:
- Modify the code in xeu.cpp to execute any program that exists on the folders with binaries.
- Only one program can be executed at a time, which means we need to use a syscall for *wait* the finish of the execution.
- On the final of the execution of a program, another program can be executed.
- The output of the programs should be on the console.

## Indicated Strategy
An intuitive set of actions is using the Linux syscalls to control the flow of execution of the programs. In fact, for each program, a one (or more) new process should be created (e.g. with a fork), executed (the right exec only require the program name), while the shell must wait for the finish of the execution and an exit() call should be done. In case that we decide to implement the extra tasks [not described here], a syscall like pipe() or another would be called.

## How compile and execute 
```bash
make # Compilation.
./xeu # Run the binary.

# In one line:
make && ./xeu
```

```bash
make test  # Run tests on whenever modification.
```
