import subprocess
from pathlib import Path

def clone_and_checkout(repo_url, branch=None, commit_hash=None, target_dir=None):
    """
    Clone a repository and optionally check out a specific branch and/or commit.
    
    Args:
        repo_url (str): The URL of the repository.
        branch (str, optional): The branch to clone. Defaults to None (default branch).
        commit_hash (str, optional): The commit hash to check out. Defaults to None (HEAD).
        target_dir (str): The directory where the repository will be cloned.
    """
    if not target_dir:
        target_dir="."
    try:
        # Build the clone command
        clone_command = ["git", "clone"]
        if branch:
            clone_command.extend(["--branch", branch])
        clone_command.extend([repo_url, target_dir])
        
        # Clone the repository
        subprocess.run(clone_command, check=True)
        print(f"Cloned repository from {repo_url} into {target_dir}")
        if branch:
            print(f"Checked out branch '{branch}'")
        else:
            print(f"Cloned default branch")
        
        # Check out the specified commit if provided
        if commit_hash:
            subprocess.run(
                ["git", "-C", target_dir, "checkout", commit_hash],
                check=True,
            )
            print(f"Checked out commit '{commit_hash}' in {target_dir}")
        else:
            print(f"Checked out HEAD in {target_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        raise

def set_user_permission(dir_name, permission):
    # Set permissions to 777
    module_dir = Path(dir_name)
    for path in module_dir.rglob("*"):
        path.chmod(permission)
    module_dir.chmod(permission)
