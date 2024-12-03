# odoox
Docker scripts for managing odoo project developpement lifecycle from developpement to testing and deployment to cloud.

## Installation

```
pip install git+https://github.com/kajande/odoox.git
```

## Usage
There are basically two types of commands:
- `docker`-like commands for handling docker images and containers related to odoo
- `odoo`-like commands for automating odoo workflows: install/update module, etc.

As for the `docker` commands, there are also two categories:
- commands that run before container creations: build - run - tag - ...
- commands that run when containers are Up: stop - start - restart - remove

As we can see, the names of the commands reflect their counterparts in `docker` and `odoo` but their intent is to be used only in the context of **odoo**. For example:
```shell
odoox ps
```
will return only the containers related to odoo for the current project:
```
CONTAINER ID   IMAGE              COMMAND                          ...              NAMES
f5232e593c1b   user/demo:latest   "/entrypoint.sh odoo"            ...              demo_odoo

d0f45f75de7a   postgres:15        "docker-entrypoint.s…"           ...              demo_pg
```

This output tells a lot:

We can see that the containers are named **demo_odoo** and **demo_pg**. The prefix **demo** actually refers to the project name (project folder) from where these containers are run. The same way the image that is created is named **user/demo:latest** where *demo* again refers to the project name and folder. The **user** comes from the configuration file of the project (see later in this tutorial), and **latest** refers to the fact that this is the image that is currently being run.

Also note that we cannot have more than these two containers per project. Whereas we can have multiple built images in the same project, that are defferentiated only by their **tag** (which in this case is *latest*). We will see later how we can tag images and select which one to work with.

This means that if you want to run a different image you will have to stop and remove completely (see later) the ones that are currently running to avoid conflicts because their names would be exactly the same.

Now that we get the idea, let's start a project and then revisit the available commands for managing it.

### The `init` command: