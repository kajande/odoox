# Odoox: Getting started

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

