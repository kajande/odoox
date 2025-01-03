import subprocess
import time

from .config import Config

class Dockerx:

    config = Config()
    docker = config.get_docker_client()
    
    def build(self, options):
        path = self.config.project_path
        if '-t' in options:
            t_index = options.index('-t')
            tag = self.config.project['user']['user'] + '/' + path.stem + ':' + options.pop(t_index+1)
            options.insert(t_index+1, tag)
        else:
            tag = self.config.project['user']['user'] + '/' + path.stem + ':latest'
            options.append('-t')
            options.append(tag)
        options.append(str(path))
        options.extend(["--build-arg", f"PROJECT_NAME={self.config.project_name}"])
        options.extend(["--build-arg", f"USER_NAME={self.config.user_name}"])
        options.extend(["--build-arg", f"USER_EMAIL={self.config.user_email}"])
        options.extend(["--build-arg", f"USER_GIT={self.config.user_git}"])
        options.extend(["--build-arg", f"GIT_TOKEN={self.config.git_token}"])
        options.extend(["--build-arg", f"CACHE_BUST={time.time()}"])
        subprocess.run(['docker', 'buildx', 'build'] + options)
        return tag


    def run(self, options):
        port = ''
        if '-b' in options:
            options.remove('-b')
            tag = self.build(options)
            port = self.config.odoo_version[:2]
        elif '-t' in options:
            t = options.pop(options.index('-t')+1)
            tag = self.config.project['user']['user'] + '/' + self.config.project_path.stem + f':{t}'
            port = t[:2]
        else:
            t = 'latest'
            tag = self.config.project['user']['user'] + '/' + self.config.project_path.stem + f':{t}'
            port = self.config.odoo_version[:2]

        pg_options = self.config.generate_postgres_options(options)
        odoo_options = self.config['odoo']
        odoo_options['image'] = tag

        odoo_options_list = self.config.generate_odoo_options(tag, port, odoo_options)
        if '-d' in options: odoo_options_list = '-d ' + odoo_options_list
        pg_command = "docker run " + pg_options
        odoo_command = "docker run " + odoo_options_list
        subprocess.run(pg_command.split())
        subprocess.run(odoo_command.split())

        print(f"Go to http://localhost:{port}69/")


    def execute(self, command, options, pg=False, odoo=False):
        if '--pg' in options: options.remove('--pg')
        if '-g' in options: options.remove('-g')
        if '--odoo' in options: options.remove('--odoo')
        if '-o' in options: options.remove('-o')
        if '-og' in options: options.remove('-og')
        if '-go' in options: options.remove('-go')
        if command == 'rm':
            options = ['-vf'] + options
        if pg:
            subprocess.run(['docker', command] + options + [self.config.pg_name])
        if odoo:
            subprocess.run(['docker', command] + options + [self.config.odoo_name])
            subprocess.run(f"docker logs -f {self.config.odoo_name}".split())
        if command == 'ps':
            self.list_containers(options)
        if command == 'im':
            if '--rm' in options:
                self.remove_image(options)
            self.list_images(options)
        if command == 'url':
            print(f"Go to {self.get_url(options)}")

    def get_url(self, options):
        container = self.docker.containers.get(self.config.odoo_name)
        ports = container.attrs['NetworkSettings']['Ports']
        url = ports['8069/tcp'][0]['HostIp']
        port = ports['8069/tcp'][0]['HostPort']
        return f"http://{url}:{port}/"

    def list_containers(self, options):
        subprocess.run(['docker', 'ps', '-f', f"name={self.config.project_name}*"] + options)

    def list_images(self, options):
        subprocess.run(['docker', 'images'] + [f"{self.config.repo}"] + options)

    def remove_image(self, options):
        try:
            tag = options[options.index('--rm')+1]
            options.remove(tag)
        except IndexError:
            tag = 'latest'
        options.remove('--rm')
        command = ['docker', 'image', 'rm', '-f'] + [f"{self.config.repo}:{tag}"] + options
        subprocess.run(command)

    def tag(self, tag, options):
        current_image = f"{self.config.repo}:latest"
        target_image = f"{self.config.repo}:{tag}"
        subprocess.run(['docker', 'image', 'tag'] +  [current_image, target_image] + options)
        print(f"tagged: {current_image} -> {target_image}")

    def workon(self, tag, options):
        target_tag = f"{self.config.repo}:{tag}"
        latest_tag = f"{self.config.repo}:latest"
        subprocess.run(['docker', 'image', 'tag'] +  [target_tag, latest_tag] + options)
        print(f"working on: {target_tag}")
        """
        TODO: handle port.
        When this is called the current default (latest) image changes
        but the port that should correspond does not update.
        """

    def get_into_container(self, options):
        if '-g' in options:
            options.remove('-g')
            subprocess.run(f"docker exec -it {self.config.pg_name} psql -U odoo -d postgres".split() + options)
        else:
            subprocess.run(f"docker exec -it {self.config.odoo_name} bash".split() + options)


if __name__ == '__main__':
    o = Dockerx()
    o.execute('start')
