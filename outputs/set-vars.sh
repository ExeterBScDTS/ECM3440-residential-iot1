RES_GROUP=IoTEdgeResources
ACCT_NAME=msaunby
# az account list
az account set -s "f6172f53-57cf-4de0-a52b-4944b34d8320"
export ACCOUNT_URI=$(az cosmosdb show --resource-group $RES_GROUP --name $ACCT_NAME --query documentEndpoint --output tsv)
export ACCOUNT_KEY=$(az cosmosdb list-keys --resource-group $RES_GROUP --name $ACCT_NAME --query primaryMasterKey --output tsv)
echo $ACCOUNT_KEY