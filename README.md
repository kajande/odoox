# Documentation for the Odoox Project

## Overview

Odoox is a command-line tool designed to streamline Odoo development workflows. The project contains utilities for managing Odoo modules, configurations, and related development tasks. This document provides an overview of the codebase and detailed explanations of the available features.

---

## Table of Contents

- [Documentation for the Odoox Project](#documentation-for-the-odoox-project)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
- [Tutorial: Getting Started with Odoox](#tutorial-getting-started-with-odoox)
  - [Prerequisites](#prerequisites)
  - [Step 1: Initialize a New Odoo Project](#step-1-initialize-a-new-odoo-project)
  - [Step 2: Build the Project](#step-2-build-the-project)
  - [Step 3: Run the Project](#step-3-run-the-project)
  - [Additional Commands](#additional-commands)
  - [Conclusion](#conclusion)
  - [Module Development](#module-development)
    - [Overview](#overview-1)
    - [Available Options](#available-options)
    - [Notes:](#notes)
    - [Terminology:](#terminology)
  - [Database Management](#database-management)
    - [Overview](#overview-2)
    - [Available Options](#available-options-1)
    - [Notes:](#notes-1)
- [Contribute.](#contribute)
  - [Project Structure](#project-structure)
    - [Key Files](#key-files)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Modules Overview](#modules-overview)
    - [`config.py`](#configpy)
    - [`db.py`](#dbpy)
    - [`dockerx.py`](#dockerxpy)
    - [`gitx.py`](#gitxpy)
    - [`module.py`](#modulepy)
    - [`module_init.py`](#module_initpy)
    - [`odoo_conf.py`](#odoo_confpy)
    - [`project.py`](#projectpy)
  - [Future Enhancements](#future-enhancements)

---

# Tutorial: Getting Started with Odoox

This guide provides a step-by-step tutorial to help you get started with **odoox**, a command-line tool designed to simplify and accelerate the Odoo development workflow. Follow these instructions to set up, build, and run an Odoo project effortlessly.

---

## Prerequisites

Before you begin, ensure that you have the following installed:

- Python (3.8 or higher recommended)
- Pipenv (optional, for creating isolated Python environments)
- Docker

---

## Step 1: Initialize a New Odoo Project

1. Open a terminal and create a new directory for your project:
   ```bash
   mkdir test_project
   cd test_project
   ```

2. Set up a Python environment (optional):
   ```bash
   pipenv install
   ```

3. Install **odoox** within the environment:
   - Head to the [odoox GitHub repository](https://github.com/kajande/odoox).
   - Copy the installation command provided in the repository: `pip install git+https://github.com/kajande/odoox.git`.
   - Paste and execute the command in your terminal.

4. Once installed, initialize the project structure using:

   **N.B**: Make sure that the directory is empty before running the following command. (Remove any file then put them back later)
   ```bash
   odoox p --init
   ```

   This command generates all the necessary files and folders for your project, including:
   - A `Dockerfile` for building the project.
   - An `odoo.conf` file for configuring the Odoo instance.
   - A pre-populated Odoo module folder named after your project.

---

## Step 2: Build the Project

1. Build the project with a single command:
   ```bash
   odoox build
   ```

2. During the build process, observe the logs. You’ll notice that the **odoox** tool is installed inside the Docker image, enabling you to use it directly within the container.

3. Verify that the build was successful by listing all related images:
   ```bash
   odoox im
   ```

   The output will display the project’s image, named after your project and tagged as `latest`.

---

## Step 3: Run the Project

1. Run the project using:
   ```bash
   odoox run
   ```

   This command:
   - Starts a PostgreSQL container.
   - Starts an Odoo container connected to the PostgreSQL container.

2. Watch the logs to confirm the base modules are being installed.

3. Access the Odoo application:
   - Use the command:
     ```bash
     odoox url
     ```
     This outputs the URL for accessing the Odoo interface. The port includes the Odoo version for easy identification.
   - Open the URL in your browser.

4. Log in to the Odoo interface with the default credentials:
   - **Username:** `admin`
   - **Password:** `admin`

5. Activate **debug mode** in the Odoo interface to view additional details, such as the current database and default module.

---

## Additional Commands

- **Manage containers:**
  
  ```bash
  odoox ps
  ```
   Prints the two containers (_odoo_ and _postgres_) within this project.
   The two containers are named `{project_name}_odoo` and `{project_name}_pg` respectively.

   This means that you cannot recreate new containers because you'll get name conflicts. To do that you'll have to remove the existing ones with `odoox rm -og`.

  ```bash
  odoox restart -o
  odoox restart -g
  odoox restart -og
  odoox start -o|-g|-og
  odoox stop -o|-g|-og
  odoox rm -o|-g|-og

  odoox in -o # gets you inside the odoo container
  odoox in -g # gets you inside the postgres container
  ```
  - *-o* targets the _odoo container_
  - *-g* targets the _postgres container_
  - *-og* or *-go* targets both the _odoo container_ and the _postgres container_

- **Get the access URL:**
  ```bash
  odoox url
  ```
  Prints the URL for accessing the Odoo application.

- **List all images:**
  ```bash
  odoox im
  ```
  Displays all images built for the project.

   ```bash
  odoox im --rm
  ```
  Removes current image (tagged `latest`).

- **Tag an image:**
  ```bash
  odoox tag <tag>
  ```
  Tags the current `latest` image with a new name, preserving its state.

- **Switch to a specific image:**
  ```bash
  odoox workon <tag>
  ```
  Assigns the `latest` tag to a specified image, ensuring that `odoox run` uses it.

---

## Conclusion

With just a few commands, **odoox** streamlines the process of setting up, building, and running Odoo projects. Explore the tool further to discover more features that simplify your Odoo development workflow.

For additional details, check out the [documentation](https://github.com/kajande/odoox) or contribute to the project by submitting issues and pull requests.


## Module Development

### Overview

Odoox simplifies module development with the base command:

```bash
odoox m <module> --option
```

- **`m`**: Denotes the subcommand for module-related operations.
- **`<module>`**: The name of the target module.
- **`--option`**: Specifies the operation to perform.

### Available Options

1. **Create a Module (Scaffold Base Code):**
   ```bash
   odoox m my_module --init
   ```
   Initializes the structure for a new module named `my_module`.

2. **Install a Module:**
   ```bash
   odoox m my_module -i
   ```
   Installs the specified module in the active Odoo database.

3. **Uninstall a Module:**
   ```bash
   odoox m my_module --i
   ```
   Uninstalls the module from the active Odoo database.

4. **Activate a Module:**
   ```bash
   odoox m my_module -a
   ```
   Activates the module by installing its data and making it ready for use.

5. **Deactivate a Module:**
   ```bash
   odoox m my_module --a
   ```
   Deactivates the module, effectively disabling it.

6. **Update a Module:**
   ```bash
   odoox m my_module -u
   ```
   Updates the module's data by reloading XML or other configurations.

### Notes:

- **Restart After Code Changes:**
  If you modify `.py` files, restart the server with:
  ```bash
  odoox restart -o
  ```

- **Update After XML Changes:**
  If you modify `.xml` files, update the module with:
  ```bash
  odoox m my_module -u
  ```

### Terminology:

- **Install vs. Activate:**
  - `Install`: Makes the module available in the database and ready for activation.
  - `Activate`: Performs the traditional "installation" by loading the module's data and making it usable.

---

## Database Management

### Overview

Odoox provides a set of commands to simplify interaction with PostgreSQL databases. The base command is:

```bash
odoox db <dbname> --options
```

- **`db`**: Denotes the subcommand for database-related operations.
- **`<dbname>`**: The name of the database to interact with.
- **`--options`**: Specifies the operation to perform.

### Available Options

1. **Create a Database:**
   ```bash
   odoox db <db_name> -c
   ```
   Creates a new database named `<project_name>_<db_name>`.

2. **Select a Database:**
   ```bash
   odoox db <db_name> -s
   ```
   Selects an existing database for further operations. This sets the current database for module commands.

3. **Delete a Database:**
   ```bash
   odoox db <db_name> -d
   ```
   Deletes a specific database, useful in cases of severe database inconsistencies.

4. **List All Databases:**
   ```bash
   odoox db <db_name> -l
   ```
   Lists all databases created under the current project. **(TODO)**

   Do you want additional database operations ?
   Run the command `odoox in -g` to get straight away inside the database and start `list`ing or `delet`ing databases.

### Notes:

- **Database Name Prefix:**
  Running any `odoox db` command appends the current project name as a prefix to the database name. For example, executing:
  ```bash
  odoox db test -c
  ```
  under a project named `proj` will create a database named `proj_test`.

---

# Contribute.

## Project Structure

```
odoox/
├── odoox/
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── db.py
│   ├── dockerx.py
│   ├── gitx.py
│   ├── module.py
│   ├── module_init.py
│   ├── odoo_conf.py
│   ├── project.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
```

### Key Files

- **`odoox/`**: Contains the main logic of the project.
- **`setup.py`**: Installation script for packaging and distribution.
- **`requirements.txt`**: Python dependencies required for the project.
- **`README.md`**: High-level description and instructions for the tool.

---

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd odoox
   ```

2. Install the project and dependencies:

   ```bash
   pip install -e .
   ```

3. Verify installation:

   ```bash
   odoox --help
   ```

---

## Usage

The tool provides various commands to interact with Odoo modules, configurations, and workflows. Below are some example usages:

- **Initialize a module:**

  ```bash
  odoox m <module_name> --init
  ```

- **Manage Docker containers:**

  ```bash
  odoox restart -o
  ```

More detailed command options will be documented in the respective modules.

---

## Modules Overview

### `config.py`

**Purpose:** Handles configuration settings for the project.

- **Key Features:**
  - Load Odoo configurations from files.
  - Provide methods for accessing database and Docker settings.

### `db.py`

**Purpose:** Provides database utilities for interacting with Odoo databases.

- **Key Features:**
  - Connect to the PostgreSQL database.
  - Execute queries securely.

### `dockerx.py`

**Purpose:** Manages Docker containers running Odoo instances.

- **Key Features:**
  - Restart Docker containers.
  - Fetch container details (e.g., IP address).

### `gitx.py`

**Purpose:** Facilitates Git operations for Odoo projects.

- **Key Features:**
  - Clone repositories.
  - Manage Git workflows.

### `module.py`

**Purpose:** Contains logic for managing Odoo modules.

- **Key Features:**
  - Copy and rename Odoo modules.
  - Update module configurations.

### `module_init.py`

**Purpose:** Handles initialization of Odoo modules within the development environment.

- **Key Features:**
  - Automates the creation of Odoo module scaffolding.

### `odoo_conf.py`

**Purpose:** Manages the `odoo.conf` configuration file.

- **Key Features:**
  - Read and write Odoo configuration files.
  - Update database and path settings.

### `project.py`

**Purpose:** Manages high-level project settings and operations.

- **Key Features:**
  - Set up new Odoo projects.
  - Organize project files and directories.

---

## Future Enhancements

- Add more Docker container management features.
- Integrate module testing capabilities.
- Support for multi-environment configurations.

---

**Documentation Last Updated:** 2024-12-15
