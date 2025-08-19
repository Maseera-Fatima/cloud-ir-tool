from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
import os

subscription_id = os.getenv("3cf9b6f1-44fd-4df0-8096-73364685ce39")
credentials = DefaultAzureCredential()
compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)

def isolate_vm(resource_group, vm_name):
    compute_client.virtual_machines.begin_deallocate(resource_group, vm_name).wait()

def snapshot_disk(resource_group, vm_name):
    vm = compute_client.virtual_machines.get(resource_group, vm_name)
    os_disk = vm.storage_profile.os_disk
    snapshot_name = f"{vm_name}-snapshot"
    compute_client.snapshots.begin_create_or_update(
        resource_group,
        snapshot_name,
        {
            'location': vm.location,
            'creation_data': {
                'create_option': 'Copy',
                'source_uri': os_disk.managed_disk.id
            }
        }
    ).wait()

def revoke_user_access(user_email):
    print(f"Revoke access for {user_email} (manual or Graph API integration)")
