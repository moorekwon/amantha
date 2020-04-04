#!/usr/bin/env python

import os
import subprocess
from pathlib import Path

HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'mini.pem')
USER = 'ubuntu'
HOST = '13.209.3.115'
TARGET = f'{USER}@{HOST}'
DOCKER_IMAGE_TAG = 'raccoonhj33/amantha'
PROJECT_NAME = 'amantha'
SOURCE = os.path.join(HOME, 'final-project', 'amantha')
SECRETS_FILE = os.path.join(SOURCE, 'secrets.json')

DOCKER_OPTIONS = (
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('--name', 'amantha'),
    ('-p', '88:8000'),
)


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)

    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    run(f'ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} {cmd}', ignore_error=ignore_error)


# host에서 도커 이미지 build, push
def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')
    run(f'docker system prune --force')
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')


# server 초기설정
def server_init():
    ssh_run(f'sudo apt -y update')
    ssh_run(f'sudo apt -y dist-upgrade')
    ssh_run(f'sudo apt -y autoremove')
    ssh_run(f'sudo apt -y install docker.io')


# 실행중인 컨테이너 종료, pull, run
def server_pull_run():
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run(f'sudo docker stop {PROJECT_NAME}', ignore_error=True)
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([f'{key} {value}' for key, value in DOCKER_OPTIONS]),
        tag=DOCKER_IMAGE_TAG
    ))


# host에서 ec2로 secrets.json 전송
# ec2에서 컨테이너로 다시 전송
def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp')
    ssh_run(f'sudo docker cp /tmp/secrets.json {PROJECT_NAME}:/srv/{PROJECT_NAME}')


# 컨테이너에서 runserver 실행
# nginx는 알아서 static 파일들을 처리할(모아줄) 수 없기 때문에 collectstatic 써줘야 함
def server_runserver():
    ssh_run(f'sudo docker exec {PROJECT_NAME} python manage.py collectstatic --noinput')
    ssh_run(f'sudo docker exec -d {PROJECT_NAME} supervisord -c /srv/amantha/.config/supervisord.conf')


if __name__ == '__main__':
    try:
        print('--- Deploy start! ---')
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_runserver()
        print('--- Deploy completed! ---')
    except subprocess.CalledProcessError as e:
        print('cmd, returncode, output, stdout, stderr >> ')
        print(e.cmd, e.returncode, e.output, e.stdout, e.stderr)
