import os
import aioftp


class DynexFTPClient:
    """FTP client for Dynex solution files."""

    def __init__(self, host=None, user=None, password=None):
        self.host = host or os.getenv("DYNEX_FTP_HOST")
        self.user = user or os.getenv("DYNEX_FTP_USER")
        self.password = password or os.getenv("DYNEX_FTP_PASS")

    async def download(self, remote_path, local_path):
        async with aioftp.Client.context(self.host, self.user, self.password) as client:
            await client.download(remote_path, local_path)

    async def upload(self, local_path, remote_path):
        async with aioftp.Client.context(self.host, self.user, self.password) as client:
            await client.upload(local_path, remote_path)
