# Project Evidence — AWS VPC Peering

## 1. Configuration Validation
The local network configuration was validated using:

```cmd
python scripts\validate_network.py
```

Validation results:
- PASS: VPC CIDRs are valid.
- PASS: Subnets are within their VPCs and do not overlap.
- PASS: Required VPC peering routes are configured.
- PASS: All required security groups are defined.
- SUCCESS: Network configuration validation completed.

## 2. AWS Console Evidence
Add genuine screenshots here if AWS resources are deployed:
- VPC A and VPC B details
- Subnet configuration
- Route table entries
- VPC peering connection status
- Security group inbound rules
- EC2 instance configuration

## 3. Connectivity Evidence
Add genuine test screenshots or terminal output only after running the tests in AWS:
- App-A to App-B ping
- App-B to App-A ping
- SSH through the bastion host

## 4. Cleanup Evidence
Add screenshots showing deletion of temporary AWS resources, if any were created.

**Note:** No AWS deployment or connectivity test is claimed by this local validation evidence.