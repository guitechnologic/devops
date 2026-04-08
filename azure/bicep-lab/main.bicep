targetScope = 'subscription'

param rgName string = 'rg-bicep-lab'
param location string = 'eastus'

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: rgName
  location: location
}

module storage './modules/storage.bicep' = {
  name: 'storageDeploy'
  scope: resourceGroup(rg.name)
}
