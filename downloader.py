import subprocess
import sys
import tarfile
import urllib.request as request

def main():
    download_url = sys.argv[1]
    output_dir = sys.argv[2]
    tar_file_path = f'{output_dir}/lua.tar.gz'
    print("Scope")
    print(tar_file_path)
    print("End scope")
    req = request.Request(download_url)
    with request.urlopen(req) as response:
        with open(tar_file_path, 'wb') as out_file:
            out_file.write(response.read())
    tar = tarfile.open(tar_file_path, 'r:gz')
    tar.extractall(path=output_dir)
    

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {e}", file=sys.stderr)
        sys.exit(1)