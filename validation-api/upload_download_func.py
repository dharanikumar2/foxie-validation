import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
import pyodbc as po
import sys


def initialize_synapse_db_connection(server,database,username,password):
    cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
        server+';DATABASE='+database+';UID='+username+';PWD=' + password)
    return cnxn

def abort_synapse_db_connection(connection):
    connection.commit()
    connection.close()

def fetch_result_into_file(server,database,username,password):
    cnxn = initialize_synapse_db_connection(server,database,username,password)
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT TOP 10 * from external_table where C4>=12000;")
    columns = [i[0] for i in cursor.description]
    row = cursor.fetchone()
    with open('sample_file.csv', 'w') as f:
        f.write(f"{columns[0]},{columns[1]},{columns[2]},{columns[3]}\n")
        while row:
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
            row = cursor.fetchone()

    cursor.close()
    del cursor
    return cnxn

def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)

def create_file_system():
    try:
        global file_system_client

        file_system_client = service_client.create_file_system(file_system="my-file-system")
    
    except Exception as e:
        print(e)

def create_directory():
    try:
        file_system_client.create_directory("my-directory")
    
    except Exception as e:
     print(e)

def upload_file_to_directory(file_to_be_uploaded):
    try:

        file_system_client = service_client.get_file_system_client(file_system="foxiepoc1")

        directory_client = file_system_client.get_directory_client("blob_test")
        
        file_client = directory_client.create_file(file_to_be_uploaded)
        local_file = open(file_to_be_uploaded,'r')

        file_contents = local_file.read()

        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))

        file_client.flush_data(len(file_contents))

    except Exception as e:
      print(e)

def download_file_from_directory(file_to_be_downloaded):
    try:
        file_system_client = service_client.get_file_system_client(file_system="foxiepoc1")

        directory_client = file_system_client.get_directory_client("blob_test")
        
        local_file = open(file_to_be_downloaded,'wb')

        file_client = directory_client.get_file_client(file_to_be_downloaded)

        download = file_client.download_file()

        downloaded_bytes = download.readall()

        local_file.write(downloaded_bytes)

        local_file.close()

    except Exception as e:
     print(e)