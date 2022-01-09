from zerionAPI import DFA
from pprint import pprint
import json

def copyDataflow(api, original_dataflow_id, new_dataflow_name):
    error = None

    # Check if Dataflow Exists
    result = api.Dataflows('GET', original_dataflow_id)

    if result.status_code == 200:
        # Check if New Name is Available
        result = api.DataflowCount(new_dataflow_name)
        if result.status_code == 200 and result.response['count'] == 0:
            # Export Dataflow
            result = api.DataflowExport(original_dataflow_id)

            if result.status_code == 200:
                # Replace Name
                dataflow = result.response
                dataflow['name'] = new_dataflow_name          

                # Import
                result = api.DataflowImport(dataflow)
                
                if result.status_code == 200:
                    return result.response.get('dataflowId')
                else:
                    error = 'Error importing Dataflow'
            else:
                error = 'Error exporting Dataflow'
        else:
            error = 'New Dataflow name is not available'
    else:
        error = 'Dataflow does not exist'
    
    return error

if __name__ == "__main__":
    print('Not directly accessible')
    exit()