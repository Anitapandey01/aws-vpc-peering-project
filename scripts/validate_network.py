
import json
import ipaddress
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "vpc-peering-config.json", encoding="utf-8") as f:
    config = json.load(f)

with open(BASE_DIR / "network-rules.json", encoding="utf-8") as f:
    rules = json.load(f)

errors = []

# 1. Validate VPC CIDRs
vpcs = {vpc["name"]: vpc for vpc in config["vpcs"]}
vpc_networks = {
    name: ipaddress.ip_network(vpc["cidr"])
    for name, vpc in vpcs.items()
}

if vpc_networks["ewb-vpc-a"].overlaps(vpc_networks["ewb-vpc-b"]):
    errors.append("VPC CIDRs overlap.")
else:
    print("PASS: VPC CIDRs are valid.")

# 2. Validate subnet ranges
all_subnets = []

for vpc_name, vpc in vpcs.items():
    for subnet in vpc["subnets"]:
        subnet_network = ipaddress.ip_network(subnet["cidr"])

        if not subnet_network.subnet_of(vpc_networks[vpc_name]):
            errors.append(f"{subnet['name']} is outside {vpc_name}.")
        
        all_subnets.append((subnet["name"], subnet_network))

for i in range(len(all_subnets)):
    for j in range(i + 1, len(all_subnets)):
        if all_subnets[i][1].overlaps(all_subnets[j][1]):
            errors.append(
                f"Subnet overlap: {all_subnets[i][0]} and {all_subnets[j][0]}"
            )

if not any("subnet" in error.lower() for error in errors):
    print("PASS: Subnets are within their VPCs and do not overlap.")

# 3. Validate peering routes
route_tables = {
    table["name"]: table
    for table in rules["route_tables"]
}

required_routes = [
    ("ewb-rt-a-public", "10.20.0.0/16", "ewb-a-b-peer"),
    ("ewb-rt-a-private", "10.20.0.0/16", "ewb-a-b-peer"),
    ("ewb-rt-b-private", "10.10.0.0/16", "ewb-a-b-peer"),
]

for table_name, destination, target in required_routes:
    routes = route_tables.get(table_name, {}).get("routes", [])
    if not any(
        route.get("destination") == destination
        and route.get("target") == target
        for route in routes
    ):
        errors.append(f"Missing route: {table_name} -> {destination}")

if not any("Missing route" in error for error in errors):
    print("PASS: Required VPC peering routes are configured.")

# 4. Validate Internet Gateway default route
public_routes = route_tables.get("ewb-rt-a-public", {}).get("routes", [])

if not any(
    route.get("destination") == "0.0.0.0/0"
    and route.get("target") == "ewb-igw-a"
    for route in public_routes
):
    errors.append("Missing public Internet Gateway default route.")
else:
    print("PASS: Public route table has the Internet Gateway route.")

# 5. Validate security group inbound rules
security_groups = {
    group["name"]: group
    for group in rules["security_groups"]
}

required_rules = {
    "ewb-sg-bastion": [
        {"protocol": "tcp", "port": 22, "source": "YOUR_PUBLIC_IP/32"}
    ],
    "ewb-sg-app-a": [
        {"protocol": "tcp", "port": 22, "source": "10.10.1.10/32"},
        {"protocol": "icmp", "type": 8, "source": "10.20.1.10/32"}
    ],
    "ewb-sg-app-b": [
        {"protocol": "tcp", "port": 22, "source": "10.10.1.10/32"},
        {"protocol": "icmp", "type": 8, "source": "10.10.2.10/32"}
    ]
}

for group_name, expected_rules in required_rules.items():
    actual_rules = security_groups.get(group_name, {}).get("inbound", [])

    for expected in expected_rules:
        if expected not in actual_rules:
            errors.append(
                f"Missing or incorrect inbound rule in {group_name}: {expected}"
            )

if not any("inbound rule" in error for error in errors):
    print("PASS: Required security group inbound rules are valid.")

# Final result
if errors:
    print("\nVALIDATION FAILED:")
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1)

print("\nSUCCESS: All local network configuration checks passed.")
