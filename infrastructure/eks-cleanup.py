#!/usr/bin/env python3
"""
EKS Terraform Cleanup Script
Handles cleanup of resources left behind after EKS cluster deletion
"""

import boto3
import time
import sys
from botocore.exceptions import ClientError

# Configuration - UPDATE THESE WITH YOUR ACTUAL RESOURCE IDs
VPC_ID = "vpc-093389e8cb3478c10"
IGW_ID = "igw-039e1efce1e2f7d3f"
SUBNETS = ["subnet-0bad62f50d4ad37fd", "subnet-0da2ee3eb9b299021", "subnet-0003898703ba0998a"]

# AWS clients
ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')

def log(message, level="INFO"):
    """Simple logging function"""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
    print(f"{icons.get(level, 'ℹ️')} {message}")

def resource_exists(resource_type, resource_id):
    """Check if AWS resource exists"""
    try:
        if resource_type == "vpc":
            ec2.describe_vpcs(VpcIds=[resource_id])
        elif resource_type == "igw":
            ec2.describe_internet_gateways(InternetGatewayIds=[resource_id])
        elif resource_type == "subnet":
            ec2.describe_subnets(SubnetIds=[resource_id])
        return True
    except ClientError:
        return False

def cleanup_elastic_ips():
    """Release Elastic IPs"""
    log("Checking for Elastic IPs...")
    try:
        response = ec2.describe_addresses(Filters=[{'Name': 'domain', 'Values': ['vpc']}])
        
        for address in response['Addresses']:
            if 'AllocationId' in address:
                try:
                    log(f"Releasing Elastic IP: {address['AllocationId']}")
                    ec2.release_address(AllocationId=address['AllocationId'])
                except ClientError as e:
                    log(f"Failed to release EIP: {e}", "WARNING")
                    
    except ClientError as e:
        log(f"Error cleaning up Elastic IPs: {e}", "WARNING")

def cleanup_nat_gateways():
    """Delete NAT gateways in subnets"""
    log("Checking for NAT Gateways...")
    try:
        for subnet_id in SUBNETS:
            if not resource_exists("subnet", subnet_id):
                continue
                
            response = ec2.describe_nat_gateways(
                Filters=[
                    {'Name': 'subnet-id', 'Values': [subnet_id]},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
            
            for nat_gw in response['NatGateways']:
                log(f"Deleting NAT Gateway: {nat_gw['NatGatewayId']}")
                ec2.delete_nat_gateway(NatGatewayId=nat_gw['NatGatewayId'])
        
        # Check if we deleted any NAT gateways
        time.sleep(10)  # Brief wait to let deletions start
            
    except ClientError as e:
        log(f"Error cleaning up NAT Gateways: {e}", "WARNING")

def cleanup_internet_gateway():
    """Detach and delete Internet Gateway"""
    log("Attempting to delete Internet Gateway...")
    try:
        if resource_exists("igw", IGW_ID):
            # Try to detach first
            try:
                ec2.detach_internet_gateway(InternetGatewayId=IGW_ID, VpcId=VPC_ID)
                log("Internet Gateway detached")
            except ClientError:
                log("IGW might already be detached", "WARNING")
            
            # Delete the gateway
            ec2.delete_internet_gateway(InternetGatewayId=IGW_ID)
            log("Internet Gateway deleted", "SUCCESS")
        else:
            log("Internet Gateway already deleted")
            
    except ClientError as e:
        log(f"Failed to delete Internet Gateway: {e}", "ERROR")

def cleanup_subnets():
    """Delete subnets"""
    log("Attempting to delete Subnets...")
    for subnet_id in SUBNETS:
        try:
            if resource_exists("subnet", subnet_id):
                ec2.delete_subnet(SubnetId=subnet_id)
                log(f"Deleted subnet: {subnet_id}", "SUCCESS")
            else:
                log(f"Subnet {subnet_id} already deleted")
        except ClientError as e:
            log(f"Failed to delete subnet {subnet_id}: {e}", "ERROR")

def main():
    """Main cleanup process"""
    log("🧹 Starting EKS cleanup process...")
    
    # Step 1: Release Elastic IPs first
    cleanup_elastic_ips()
    
    # Step 2: Clean up NAT Gateways
    cleanup_nat_gateways()
    
    # Step 3: Wait for AWS to process deletions
    log("Waiting 60 seconds for AWS to process deletions...")
    time.sleep(60)
    
    # Step 4: Delete Internet Gateway
    cleanup_internet_gateway()
    
    # Step 5: Delete Subnets
    cleanup_subnets()
    
    log("✅ Cleanup completed!")
    log("💡 Now run 'terraform destroy -auto-approve' to clean up remaining resources")

if __name__ == "__main__":
    main()
