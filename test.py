import os
import paramiko


def download_files(padid, directory_path, remote_tmp_path, remote_db_path, ssh_host, ssh_port, ssh_user, ssh_password):
    # Ensure the specified directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

    # Setup SFTP session
    sftp = ssh.open_sftp()

    # Execute command to get file names from SQLite database
    query = f"SELECT file_name FROM file_info WHERE file_name LIKE '%_{padid}'"
    sqlite_cmd = f"sqlite3 {remote_db_path} \"{query}\""
    stdin, stdout, stderr = ssh.exec_command(sqlite_cmd)
    file_names = stdout.read().decode().splitlines()
    

    # Download files using SFTP
    for file_name in file_names:
        query2 = f"SELECT writefile('{remote_tmp_path}{file_name}', file_content) FROM file_info WHERE file_name = '{file_name}'"
        sqlite_cmd2 = f"sqlite3 {remote_db_path} \"{query2}\""
        ssh.exec_command(sqlite_cmd2)
        
        remote_file_path = os.path.join(os.path.dirname(remote_tmp_path), file_name)
        local_file_path = os.path.join(directory_path, file_name)
        
        if not os.path.exists(local_file_path):
            print(f"Downloading {file_name}...")
            sftp.get(remote_file_path, local_file_path)
        else:
            print(f"{file_name} already exists.")

    # Close SFTP and SSH connections
    sftp.close()
    ssh.close()

# Example usage
download_files(
    padid='1', 
    directory_path='./testdb',
    remote_tmp_path="D:/0612/build/OsakaTest_Data/StreamingAssets/tmppath/",
    remote_db_path="D:/0612/build/OsakaTest_Data/StreamingAssets/Flower.db",
    ssh_host='140.96.76.36',
    ssh_port=22,
    ssh_user='user',
    ssh_password='itriJ100'
)
