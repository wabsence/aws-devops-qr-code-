provider "aws" {
  region = var.region
}

# VPC Module from Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  # Tags required for EKS
  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }

  tags = var.tags
}

# IAM Module for EKS from Terraform Registry
module "eks_iam" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "5.30.0"

  role_name = "${var.cluster_name}-cluster-role"
  
  role_policy_arns = {
    AmazonEKSClusterPolicy = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  }

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-node"]
    }
  }

  tags = var.tags
}

# Security Group Module from Terraform Registry
module "eks_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "${var.cluster_name}-cluster-sg"
  description = "Security group for EKS cluster"
  vpc_id      = module.vpc.vpc_id

  egress_rules = ["all-all"]

  tags = var.tags
}

# EKS Module from Terraform Registry
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  # Use EKS managed node groups
  eks_managed_node_groups = {
    main = {
      name = "main-node-group"

      instance_types = var.instance_types
      capacity_type  = var.capacity_type

      min_size     = var.node_group_min_size
      max_size     = var.node_group_max_size
      desired_size = var.node_group_desired_size

      disk_size = var.node_disk_size
    }
  }

  tags = var.tags
}