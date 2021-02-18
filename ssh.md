
# Using the departmental machines remotely


This document is a guide for using the departmental machines remotely.
You can access the machines with a secure connection through SSH. This
connection can be used for executing commands on the remote machine,
tunneling through a firewall, and transfering files to and from a remote
machine.

## Installing the SSH client

### Unix

Unix system usually have a SSH client pre-installed.

### Windows

We advise you to use PuTTY, a free SSH client for Windows that can be
downloaded on
<http://www.chiark.greenend.org.uk/sgtatham/putty/download.html>. The
PuTTY package consists of several binaries. We will use PuTTY: the SSH
client, PuTTYgen: the key generator/reformatter, Pageant: the key
manager, Plink: the command line interface to the PuTTY back ends, and
PSCP: the scp client for copying files remotely. You can download all
the binaries seperately or get the zip with everything. Put all the
binaries together in a folder. You can invoke all the binaries in this
folder from terminal as long as either you are in the folder or the
folder is in your `$PATH`.

## Obtaining a SSH key pair

To connect to a remote computer, you can use an SSH key pair. The pair
consists of a private key and a public key. The private key is kept on
your computer and should stay secret. The computer that you want to
connect to has a list of authorized public keys. The remote computer
will allow you to connect if it has your public key. You can generate an
SSH key pair through the website
<https://www.cs.kuleuven.be/restricted/ssh/>. Public keys that are
generated this way are automatically distributed on the departmental
machines, allowing you to access them remotely.

PuTTY needs the private key to be in `.ppk` format. PuTTYgen can
transform your key to the right format by first loading the existing key
and then saving it.

## Configuring SSH and running remote commands

### A simple connection

SSH is usually ran through a terminal. You can open a terminal on
Windows with `<Windows>-r`    Open: *cmd*. We can make a connection to a
remote machine by opening a terminal and running:

-   on Unix:

         % ssh <username>@<remoteMachine> -i <pathToPrivateKey>
         % ssh r0123456@st.cs.kuleuven.be -i path/to/id_rsa

-   on Windows:

         % plink <username>@<remoteMachine> -i <pathToPrivateKey.pkk>
         % plink r0123456@st.cs.kuleuven.be -i path/to/id_rsa.pkk

### Configuration

To avoid typing the key location every time, you can make sure that the
ssh client finds it automatically. On Unix systems, you do this by
placing the public key in the `\sim/.ssh` directory. To avoid having to
type the passphrase every time, you can add it to your key agent:

     % ssh-agent bash
     % ssh-add ~/.ssh/id_rsa

On Windows, you run:

     % pageant d:path/to/id_rsa.pkk

You can avoid typing the whole command all together by making a
configuration. On Unix systems, this is the file `.ssh/config` with the
following text:

    Host pcroom
    User        r0123456
    HostName    st.cs.kuleuven.be

You can now connect with

     % ssh pcroom

On Windows, you use the graphical interface of PuTTY. You first complete
the configuration by setting:

- Session → Host Name (or IP address) = st.cs.kuleuven.be
- Session → Port = 22
- Connection → Data → Auto-login username = r0123456

Then you save it in the *Session* tab by writing *pcroom* in *Saved
Sessions* and hitting *Save*.

You can now connect with

     % plink pcroom

### Getting passed the login node

The `st.cs.kuleuven.be` server is a login node, it is not meant to run
experiments. The machines that you can run experiments on have the
addres `<pcname>.cs.kotnet.kuleuven.be`. The next section points to a
list of available machines. These machines are not immediately reachable
outside the KU Leuven network, you need to go through the login node
first. From the login node, you can reach any other machine again
through ssh. For example:

     % ssh aalst.cs.kotnet.kuleuven.be

This is possible because your private keys were stored automatically in
`\sim/.ssh/` on the departmental machines. You can configure the key
agent and configuration file here the same way as on your personal
computer.

#### Proxy

You can immediately get to a departmental machine by setting up a proxy.
On Unix systems, this can be done by adding

     ProxyCommand ssh -e none <user>@<login> nc %h %p -w 120 2> /dev/null

to the configuration file. Here is a complete example:

    Host aalst
            User            r0123456
            HostName        aalst.cs.kotnet.kuleuven.be
            ProxyCommand ssh -e none r0123456@st.cs.kuleuven.be nc %h %p -w 120 2> /dev/null

In Windows a proxy can be setup through PuTTY as follows:

-   Session → Host Name (or IP address) = aalst.cs.kotnet.kuleuven.be
-   Session → Port = 22
-   Connection → Data → Auto-login username = r0123456
-   Connection → Proxy → Proxy type = local
-   Connection → Proxy → Proxy hostname = st.cs.kuleuven.be
-   Connection → Proxy → Port = 22
-   Connection → Proxy → Username = r0123456
-   Connection → Proxy → Telnet command, or local
    proxy command = plink %user@%proxyhost nc %host %port

Then you save it in the *Session* tab by writing *aalst* in *Saved
Sessions* and hitting *Save*.

You can now connect with

     % plink aalst

## List of available machines

The page <http://mysql.cs.kotnet.kuleuven.be/> gives an overview of the
available departmental machines and their current load.

This website is not always reachable because of firewall and network
configurations. You can always reach it by making an ssh tunnel. The
website is available on the server `mysql.cs.kotnet.kuleuven.be` at port
80. You can make a tunnel from your local port 10080 to that port.

Set up the tunnel by entering:

-   on Unix:

         % ssh -L 10080:mysql.cs.kotnet.kuleuven.be:80 pcroom

-   on Windows:

         % plink -L 10080:mysql.cs.kotnet.kuleuven.be:80 pcroom

Now you can reach the website at <http://localhost:10080/>

## Remote copying

Making a remote copy is similar to making a local copy in the unix
terminal. The command for a local copy is:

     % cp [-r] <source> <destination>

where source and destination are paths. The `-r` is an optional flag to
indicate that you also want to copy directories. A remote copy uses
"secure copy" (scp) and needs the ssh configuration of the remote
computer. For copying to the remote machine we use

-   on Unix:

         % scp [-r] <source> pcroom:<destination>

-   on Windows:

         % pscp [-r] <source> pcroom:<destination>

For copying from the remote machine we use

-   on Unix:

         % scp [-r] pcroom:<source> <destination>

-   on Windows:

         % pscp [-r] pcroom:<source> <destination>

If you have a proxy configured, you can directly copy to and from the
departmental machines. If not, you need to make an intermediate copy on
the login node.

On unix machines, you can also use `rsync` instead of `scp`. The usage
is the same, but this command will analyze the difference between the
source and destination and only copy what is necessary, thus being more
efficient.

## Safely running experiments with "screen"

Screen is a useful application for running experiments remotely because
it allows you to:

-   Use multiple shell windows from a single SSH session.

-   Keep a shell active even through network disruptions.

-   Disconnect and re-connect to a shell sessions from multiple
    locations.

-   Run a long running process without maintaining an active shell
    session.

Starting screen is done by typing:

     % screen

This opens a new screen terminal. After hitting Enter, you can start
working like you would in a normal terminal.

There are two ways to leave a screen terminal: terminating and
detaching. The former kills the screen, including processes that it is
running. The latter lets the screen run in the background while you
leave, it can be recovered later. A session can be terminated with
`<Ctrl>-d` or writing `exit`. It becomes detached with `<Ctrl>-a d` or
by disrupting the connection, for example a network failure or shutting
down the computer. Your experiments will thus keep on running, even when
you lose your internet connection.

All the screen commands start with `<Ctrl>-a` and are followed by
another key. These are the most common ones:

-   `d` : detach the screen

-   `c` : create a new terminal within screen

-   `n` : go to the next terminal

-   `p` : go to the previous terminal

-   `?` : help page about screen commands

You can reattach to a detached screen by running `screen -r`

## Useful directories

### Home directory

`/home/r0123456/`

In your home directory you can store your personal files. The home
directory is accessible from all the departmental machines but not from
the login node. There is an upperlimit on the space that you can use. To
know the limit and your current usage run:

     % quota

### Local space

`/tmp/`

Every machine has local space that you can use. This folder is cleaned
regularly, so do not store anything important here. It is the perfect
place for heavy output of experiments, just make sure to copy it to a
safe place if you need to keep it.

### Course directory

`/cw/lvs/NoCsBack/vakken/ac2021/H0T25A/ml-project/r0123456`

This folder is your personal space for submitting your implementation. The folder is accessible from
all the departmental machines but not from the login node. There is an upperlimit of 50MB.
