from pathlib import Path

def get_dockerfile(project_dir, odoo_version):

    content = """FROM odoo:""" + str(odoo_version) + """

ARG PROJECT_NAME
ARG CACHE_BUST=1
ARG USER_EMAIL
ARG USER_NAME

USER root
RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean
RUN git config --global --add safe.directory /${PROJECT_NAME} \
    && git config --global user.email ${USER_EMAIL}\
    && git config --global user.name ${USER_NAME}

WORKDIR /odoox
RUN git clone https://github.com/kajande/odoox.git . \
    && pip install . --no-cache-dir && echo "$CACHE_BUST"
ENV PATH="/var/lib/odoo/.local/bin:${PATH}"

WORKDIR /${PROJECT_NAME}
COPY . /${PROJECT_NAME}

CMD ["odoo"]
"""
    init_file = project_dir / 'Dockerfile'
    init_file.write_text(content)

if __name__ == "__main__":
    name = 'demo_project'
    print(get_dockerfile(name))
