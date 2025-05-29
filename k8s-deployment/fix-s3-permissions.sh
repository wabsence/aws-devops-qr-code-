# Set your cluster and nodegroup names
export CLUSTER_NAME="qrcode-k8s-cluster"
export NODEGROUP_NAME="main-node-group-20250529081409417900000013"

# Create the policy file
cat > s3-access-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::qrcode-storage-devops-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::qrcode-storage-devops-bucket"
            ]
        }
    ]
}
EOF

# Get the node role ARN and extract just the role name
export NODE_ROLE_ARN=$(aws eks describe-nodegroup --cluster-name $CLUSTER_NAME --nodegroup-name $NODEGROUP_NAME --query 'nodegroup.nodeRole' --output text)
export NODE_ROLE_NAME=$(echo $NODE_ROLE_ARN | cut -d'/' -f2)

echo "Node Role ARN: $NODE_ROLE_ARN"
echo "Node Role Name: $NODE_ROLE_NAME"

# Create the IAM policy
aws iam create-policy \
    --policy-name QRCodeS3Access \
    --policy-document file://s3-access-policy.json \
    --description "Policy for QR Code app to access S3 bucket"

# Attach the policy to your node group role
aws iam attach-role-policy \
    --role-name $NODE_ROLE_NAME \
    --policy-arn arn:aws:iam::012229012261:policy/QRCodeS3Access

echo "Policy attached successfully!"

# Verify the policy is attached
echo "Verifying attached policies:"
aws iam list-attached-role-policies --role-name $NODE_ROLE_NAME
