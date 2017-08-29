"""Delete resources in group

This script expects that the following environment vars are set:

AZURE_TENANT_ID: your Azure Active Directory TENANT_ID id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application CLIENT_SECRET
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
"""
from __future__ import print_function
import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient

from msrestazure.azure_exceptions import CloudError

# Resource Group
GROUP_NAME = 'cumulustest'

COMPUTE_API_VERSION = "2017-03-30"
NETWORK_API_VERSION = "2017-08-01"

def get_credentials():
    """
    Function to reach out to Azure and collect token
    """
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        CLIENT_SECRET=os.environ['AZURE_CLIENT_SECRET'],
        TENANT_ID=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

def delete_resources():

    """
    Main function to delete resources
    """
    #
    # Create all clients with an Application (service principal) token provider
    #
    print('Grabbing Credentials!')
    credentials, subscription_id = get_credentials()
    resource_client = ResourceManagementClient(credentials, subscription_id)

    resource_list = []

    try:

        test = resource_client.resources.list_by_resource_group(GROUP_NAME)

        for item in test:
            temp_dict = {}
            test_item_type = item.type
            test_item_provider = test_item_type.split('/')
            temp_dict['provider'] = test_item_provider[0]
            temp_dict['parent'] = test_item_provider[1]
            temp_dict['name'] = item.name
            temp_dict['id'] = item.id
            resource_list.append(temp_dict)

        print(resource_list)
        print('\n')

        for i, item in enumerate(resource_list):
            if item['parent'] == 'virtualMachines':
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    COMPUTE_API_VERSION)
                async_delete_item.wait()
                print('VM Deleted: ' + item['name'])
                del resource_list[i]

        for i, item in enumerate(resource_list):
            if item['parent'] == 'networkInterfaces':
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    NETWORK_API_VERSION)
                async_delete_item.wait()
                print('Network Interface Deleted: ' + item['name'])
                del resource_list[i]

        for i, item in enumerate(resource_list):
            if item['parent'] == 'virtualNetworks':
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    NETWORK_API_VERSION)
                async_delete_item.wait()
                print('Network Deleted: ' + item['name'])
                del resource_list[i]

        for i, item in enumerate(resource_list):
            if item['parent'] == 'publicIPAddresses':
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    NETWORK_API_VERSION)
                async_delete_item.wait()
                print('Public IP Deleted: ' + item['name'])
                del resource_list[i]

        for i, item in enumerate(resource_list):
            if item['parent'] == 'disks':
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    COMPUTE_API_VERSION)
                async_delete_item.wait()
                print('Disk Deleted: ' + item['name'])
                del resource_list[i]

        for i, item in enumerate(resource_list):
            if item['parent'] == 'storageAccounts':
                #DO NOT DELETE STORAGE ACCOUNT...TAKES FOREVER TO RECREATE
                #async_delete_item = resource_client.resources.delete_by_id(item['id'],
                #    STORAGE_API_VERSION)
                #async_delete_item.wait()
                print('DO NOT DELETE STORAGE ACCOUNT...TAKES FOREVER TO RECREATE...')
                print('Storage Account NOT Deleted: ' + item['name'])
                del resource_list[i]

        for item in resource_list:
            #
            if item['provider'] == "Microsoft.Network":
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    NETWORK_API_VERSION)
                async_delete_item.wait()
            else:
                async_delete_item = resource_client.resources.delete_by_id(item['id'], \
                    COMPUTE_API_VERSION)
                async_delete_item.wait()
            print('Item Deleted: ' + item['name'])

    except CloudError:
        print('A VM operation failed:', traceback.format_exc(), sep='\n')
    else:
        print('All operations completed successfully!')

if __name__ == "__main__":
    delete_resources()
