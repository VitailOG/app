import io

import paramiko

from config import REMOTE_FOLDER_PATH
from responses import VPSInfo


def upload(filename: str, vps: VPSInfo, buffer: io.BytesIO) -> None:
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps.ip, username=vps.user, password=vps.password)
        with ssh.open_sftp() as sftp:
            sftp.putfo(buffer, REMOTE_FOLDER_PATH + filename)


def download(filename: str, vps: VPSInfo) -> io.BytesIO:
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps.ip, username=vps.user, password=vps.password)
        with ssh.open_sftp() as sftp:
            buffer = io.BytesIO()
            sftp.getfo(REMOTE_FOLDER_PATH + filename, buffer)
            return buffer
