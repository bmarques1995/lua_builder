import subprocess
import sys
import tarfile
import urllib.request as request
import os

def main():
    download_url = sys.argv[1]
    output_dir = os.path.normpath(sys.argv[2])
    tar_file_path = os.path.normpath(f'{output_dir}/lua.tar.gz')
    version_info = sys.version_info
    req = request.Request(download_url)
    with request.urlopen(req) as response:
        with open(tar_file_path, 'wb') as out_file:
            out_file.write(response.read())
    tar = tarfile.open(tar_file_path, 'r:gz')
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 12):
        tar.extractall(path=output_dir)
    else:
        tar.extractall(path=output_dir, filter='fully_trusted')

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {e}", file=sys.stderr)
        sys.exit(1)