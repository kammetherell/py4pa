import pysftp
import os
from datetime import datetime as datetime
import logging

class SFTP:
    """Helper class to manage connections to an SFTP site, file collection and upload

    Parameters
    ----------
    host : str
        The host address you wish to use as the SFTP connection.

    user : str
        The username of the SFTP account you are connecting to.

    pword : str
        The password of the SFTP account you are connecting to.

    port : int
        The port through which the connection to the SFTP server is made.
        522 is used as the default port.
    """

    # Datetime is used to append to folder names
    def __init__(self, host, user, pword, port, date_time=None):
        self.host = host
        self.user = user
        self.pword = pword
        self.port = port
        if date_time is not None:
            self.date_time = date_time
        else:
            now = datetime.now()
            self.date_time = now.strftime('%m-%d-%y_%H-%M-%S')

    def download_file(self, 
                     master_folder, 
                     sub_folder, 
                     local_file=False, 
                     remote_file=False, 
                     return_file_path=False, 
                     return_folder_path=False, 
                     delete_original=True, 
                     use_date_stamp=True):
        """Collects file from STS account and saves within folder location.Package
        can also currently used to create folders without interaction with SFTP site.

        Parameters
        ----------
        master_folder: String ()
            Path to the root directory for the process
        sub_folder: String ()
            Name used for the sub folder within the root directory. This is where the output will be saved.
            Example: Inputting "Output Files" will create a separate folder "Output Files" within the 
            root directory for files to be saved.
        local_file: String () default = False
            Path to where the file will be saved locally.
        remote_file: String () default = False
            Path to where the file is stored in the SFTP portal.
        return_file_path: Boolean default = False
            Determines whether the filepath to the outputs is returned by the function or not.
        return_folder_path: Boolean default = False
            Determines whether the folder path to the outputs is returned by the function or not.
        delete_original: Boolean default = False
            Determines whether the file is removed from the SFTP portal after it has been downloaded.
        use_date_stamp: Boolean default = True
            Determines whether a date stamp is appended to the sub folder name or not.
        Returns
        -------
        Dependant on the parameters, the function will optionally return the filepath of output 
        and/or path to the sub folder where output is stored.
        """

        if use_date_stamp and sub_folder:
            folder_location = "{0}_{1}".format(sub_folder, self.date_time)
        elif sub_folder:
            folder_location = "{0}".format(sub_folder)
        else:
            folder_location = ""
        folder = r'{0}\\{1}'.format(master_folder, folder_location)

        if not os.path.exists(folder):
            logging.debug(f"Creating folder directory at {folder}")
            os.makedirs(folder)
            logging.debug(f"Successfully created folder directory at {folder}")

        if local_file:
            # Define the local path where the file will be saved
            localFilePath = r'{0}\\{1}'.format(folder, local_file)

        if remote_file and local_file:
            self.__file_collect(remote_file, localFilePath)

            if delete_original:
                self.__file_remove(remote_file)

        if return_file_path and return_folder_path and local_file:
            return localFilePath, folder
        elif return_file_path and local_file:
            return localFilePath
        elif return_folder_path:
            return folder
        else:
            return None

    def upload_file(self, local_file_path, remote_file_path):
        """Uploads file to SFTP account

        Parameters
        ----------
        local_file_path: String ()
            Path to where the file is saved locally.
        remote_file_path: String ()
            Path to where the file will be stored in the SFTP portal.

        Returns
        -------
        Nothing is returned by the function.

        """
        logging.debug(f"Uploading local file: {local_file_path}")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        logging.debug(f"Establishing new SFTP connection with {self.host}")

        with pysftp.Connection(
            host=self.host,
            username=self.user,
            password=self.pword,
            cnopts=cnopts,
            port=self.port
        ) as sftp:
            sftp.put(local_file_path, remote_file_path, confirm=False)

        logging.debug(f"Successfully uploaded {local_file_path}")

    def list_files(self, remote_dir="/"):
        """Lists file directory within SFTP account

        Parameters
        ----------
        remote_dir: String () default = '/'
            This is the folder name that you would like to see a directory for,
            change to see more/less granular directories.

        Returns
        -------
        Function returns a list of files within the directory.

        """
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(
            host=self.host,
            username=self.user,
            password=self.pword,
            cnopts=cnopts,
            port=self.port
        ) as sftp:

            files = sftp.listdir(remote_dir)

        return files

    # Code to collect file from SFTP site based and save at local path
    def __file_collect(self, remote_file_path, local_file_path):
        """Function to collect files from SFTP account

        Parameters
        ----------
        remote_file_path: String ()
            Path to where the file is stored in the SFTP portal.
        local_file_path: String ()
            Path to where the file will be saved locally.

        Returns
        -------
        Nothing is returned by the function.

        """

        logging.debug(f"Downloading remote file: {remote_file_path}")

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        logging.debug(f"Establishing new SFTP connection with {self.host}")

        with pysftp.Connection(
            host=self.host,
            username=self.user,
            password=self.pword,
            cnopts=cnopts,
            port=self.port
        ) as sftp:

            sftp.get(remote_file_path, local_file_path)

        logging.debug(f"Successfully downloaded {remote_file_path}")

    # Code to remove file from SFTP site once it has been downloaded
    def __file_remove(self, remote_file_path):
        """Function to remove files from SFTP account

        Parameters
        ----------
        remote_file_path: String ()
            Path to where the file is stored in the SFTP portal.
        Returns
        -------
        Nothing is returned by the function.

        """

        logging.debug(f"Removing remote file: {remote_file_path}")

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        logging.debug(f"Establishing new SFTP connection with {self.host}")

        with pysftp.Connection(
            host=self.host,
            username=self.user,
            password=self.pword,
            cnopts=cnopts,
            port=self.port
        ) as sftp:

            sftp.remove(remote_file_path)

        logging.debug(f"Successfully removed {remote_file_path}")
