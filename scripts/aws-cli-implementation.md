# AWS VPC Peering – AWS CLI Implementation

## 1. Prerequisites

Install and verify AWS CLI:

```powershell
aws --version
```

Check AWS identity:

```powershell
aws sts get-caller-identity
```

Set the AWS Region:

```powershell
aws configure
```

## 2. Create VPCs

```powershell
aws ec2 create-vpc --cidr-block 10.10.0.0/16
aws ec2 create-vpc --cidr-block 10.20.0.0/16
```

## 3. Create Subnets

VPC A public subnet:

```powershell
aws ec2 create-subnet --vpc-id VPC_A_ID --cidr-block 10.10.1.0/24
```

VPC A private subnet:

```powershell
aws ec2 create-subnet --vpc-id VPC_A_ID --cidr-block 10.10.2.0/24
```

VPC B private subnet:

```powershell
aws ec2 create-subnet --vpc-id VPC_B_ID --cidr-block 10.20.1.0/24
```

Replace placeholder IDs with actual AWS resource IDs.

## 4. Create Internet Gateway

```powershell
aws ec2 create-internet-gateway
```

Attach it to VPC A:

```powershell
aws ec2 attach-internet-gateway --internet-gateway-id IGW_ID --vpc-id VPC_A_ID
```

## 5. Create VPC Peering

```powershell
aws ec2 create-vpc-peering-connection --vpc-id VPC_A_ID --peer-vpc-id VPC_B_ID
```

Accept the peering request:

```powershell
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id PCX_ID
```

Verify status:

```powershell
aws ec2 describe-vpc-peering-connections --vpc-peering-connection-ids PCX_ID
```

## 6. Route Configuration

Add the VPC B route to VPC A route tables:

```powershell
aws ec2 create-route --route-table-id ROUTE_TABLE_A_PUBLIC --destination-cidr-block 10.20.0.0/16 --vpc-peering-connection-id PCX_ID

aws ec2 create-route --route-table-id ROUTE_TABLE_A_PRIVATE --destination-cidr-block 10.20.0.0/16 --vpc-peering-connection-id PCX_ID
```

Add the return route in VPC B:

```powershell
aws ec2 create-route --route-table-id ROUTE_TABLE_B_PRIVATE --destination-cidr-block 10.10.0.0/16 --vpc-peering-connection-id PCX_ID
```

## 7. Verify Routes

```powershell
aws ec2 describe-route-tables
```

## Important

These commands are implementation references, not execution evidence. Replace placeholders with actual IDs before execution. Do not launch EC2 instances or create billable resources without checking account access and costs.