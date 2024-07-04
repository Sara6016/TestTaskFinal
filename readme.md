# Folder Synchronization Script

This Python script synchronizes two directories (source and replica) periodically. The synchronization ensures that the replica folder is a complete and identical copy of the source folder. The script also logs the synchronization activities.

## Usage

To run the script, use the following command:

python synchronization.py &lt;source_folder&gt; &lt;replica_folder&gt; &lt;interval&gt; &lt;log_file_path&gt;

<source_folder>: Path to the source directory which needs to be synchronized.  
<replica_folder>: Path to the replica directory where the source directory will be copied.  
&lt;interval&gt;: Time interval (in seconds) between each synchronization.  
<log_file_path>: Path to the directory where the log file will be stored.  

## Example (input)
python synchronization.py C:/Users/Sara/Source C:/Users/Sara/Replica 60 C:/Users/Sara/Logs

## Stopping the script
To interrupt the program, press 'q' on the keyboard. After pressing 'q' the last synchronization will occur.
