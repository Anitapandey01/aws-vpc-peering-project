# Resource inventory and submission details

Fill this in with your own details after building the AWS lab.

- Student name: `REPLACE_ME`
- Batch: `REPLACE_ME`
- AWS Region: `REPLACE_ME`
- Completion date: `YYYY-MM-DD`

| Resource | Name tag | Actual AWS ID | Notes |
|---|---|---|---|
| VPC A | `ewb-vpc-a` | `REPLACE_ME` | CIDR `10.10.0.0/16` |
| VPC B | `ewb-vpc-b` | `REPLACE_ME` | CIDR `10.20.0.0/16` |
| Public subnet A | `ewb-a-public` | `REPLACE_ME` | `10.10.1.0/24` |
| Private subnet A | `ewb-a-private` | `REPLACE_ME` | `10.10.2.0/24` |
| Private subnet B | `ewb-b-private` | `REPLACE_ME` | `10.20.1.0/24` |
| Public route table | `ewb-rt-a-public` | `REPLACE_ME` | Associated to public subnet A |
| Private route table A | `ewb-rt-a-private` | `REPLACE_ME` | Associated to private subnet A |
| Private route table B | `ewb-rt-b-private` | `REPLACE_ME` | Associated to private subnet B |
| Internet gateway | `ewb-igw-a` | `REPLACE_ME` | Attached to VPC A |
| Peering connection | `ewb-a-b-peer` | `REPLACE_ME` | Status should be Active |
| Bastion | `ewb-bastion` | `REPLACE_ME` | Public IPv4: `REPLACE_ME` |
| App-A | `ewb-app-a` | `REPLACE_ME` | Private IP: `10.10.2.10` |
| App-B | `ewb-app-b` | `REPLACE_ME` | Private IP: `10.20.1.10` |

## Evidence captured

| Evidence | File path | Actual result/notes |
|---|---|---|
| Architecture and CIDR plan | `evidence/01-architecture.png` | `REPLACE_ME` |
| Subnet associations and routes | `evidence/02-route-tables.png` | `REPLACE_ME` |
| Active peering connection | `evidence/03-peering-active.png` | `REPLACE_ME` |
| Baseline ping before routes | `evidence/04-baseline-ping.png` | `REPLACE_ME` |
| Forward and reverse ping | `evidence/05-private-ping-success.png` | `REPLACE_ME` |
| SSH to App-B through bastion | `evidence/06-proxyjump-ssh.png` | `REPLACE_ME` |
| Controlled failure and recovery | `evidence/07-rule-failure-recovery.png` | `REPLACE_ME` |
| Cleanup | `evidence/08-cleanup.png` | `REPLACE_ME` |

Do not leave `REPLACE_ME` entries in the final report if your assignment requires actual execution evidence.
