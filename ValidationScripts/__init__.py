import logging

import azure.functions as func
from . import upload_download_func as new_func


server = 'tcp:foxie-poc-ondemand.sql.azuresynapse.net'
database = 'test_db5'
username = 'dharani'
password = 'Clay$123'

storage_account_name = 'foxiepoc'
storage_account_key = '84a2MWWBq0r3nXpkznuPti8aENj2WI9tO9PFPkIV/ytuJISaDrWCPekcoBELxsK+e4ZF/Y7WeqL+9IC2tfLhYg=='


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        new_func.initialize_storage_account(storage_account_name, storage_account_key)
        con = new_func.fetch_result_into_file(server,database,username,password)
        new_func.abort_synapse_db_connection(con)
        new_func.upload_file_to_directory("sample_file.csv")
        return func.HttpResponse(
             "File downloaded and uploaded succesfully.",
             status_code=200
        )
        #download_file_from_directory("sample_file.csv")
    else:
        return func.HttpResponse(
             "Please pass a command to execute the validation functi",
             status_code=200
        )
