# Where to Start

## Account Creation and Verification
The client has a built-in utilities CLI, you can use it to create an account and receive your cloud API token
### New User Registration
```bash
pysync reg <EMAIL>
```
The command should return something along the lines of
```bash
Welcome to PySync, Your Token is "FooBar"
```

## Client Project Bootloader
Use the CLI again to initialize and new project, or inject into an existing one. This can be accomplished using one of the following commands.
#### New Project Initialization
```bash
pysync init <PATH>
```
#### Existing Project Injection
```bash
pysync inject <PATH>
```
This will otherwise add the PySync project monitor to the project directory, from here you can modify `setup.yaml` for environment configuration and settings\
As a side note, the CLI also supports default modification, for instance `pysync deaults -w user-email helloworld@pysync.pyi` will write `helloworld@pysync.pyi` as the value for `user-email` for all project initializations going forward\

#### Server Start
To start the server, you can continue to use the CLI, with the `pysync run start` while you are in the project directory, alternatively you can also import the `Sync` function from the PySync module and the syncing will start upon file run start.\
Another side note, you can also configure the project specific setup.yaml file with the `**quark` values in the sync function call
##### Example (Project-side Server Init)
```Python
from pysync import Sync
Sync(projectTitle="FooBar")
```

<seealso>
    <category ref="lnks">
        <a href="https://github.com/definiteconfusion">My Github</a>
        <a href="https://www.linkedin.com/in/jake-rase-9a28a926a/">My LinkedIn</a>
        <a href="https://www.python.org/downloads/">Python Download</a>
    </category>
</seealso>