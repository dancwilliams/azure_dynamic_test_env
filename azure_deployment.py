import os.path
from deployer import Deployer


# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret

my_subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID', '11111111-1111-1111-1111-111111111111')   # your Azure Subscription Id
my_resource_group = 'cumulustest'            # the resource group for deployment
my_pub_ssh_key_path = os.path.expanduser('/home/travis/build/dancwilliams/azure_dynamic_test_env/id_rsa.pub')   # the path to your rsa public key file

print (my_pub_ssh_key_path)

msg = "\nInitializing the Deployer class\n"
print(msg)

# Initialize the deployer class
deployer = Deployer(my_subscription_id, my_resource_group, my_pub_ssh_key_path)

print("Beginning the deployment... \n\n")
# Deploy the template
my_deployment = deployer.deploy()

print("Done deploying!!\n\nYou can connect via: `ssh cumulus@{}.eastus.cloudapp.azure.com`".format(deployer.dns_label_prefix))

dns_name = ("{}.eastus.cloudapp.azure.com".format(deployer.dns_label_prefix))

with open("azure_dns", "wr") as f: 
    f.write(dns_name) 

# Destroy the resource group which contains the deployment
# deployer.destroy()
