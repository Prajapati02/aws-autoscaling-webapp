# 🌐 AWS Auto-Scaling Web App Infrastructure

A production-grade, highly available web application infrastructure built entirely on AWS — featuring automatic scaling, load balancing, and a managed relational database inside a custom VPC.

> **Built with:** Python · Flask · AWS EC2 · ALB · Auto Scaling · RDS MySQL · VPC · IAM · Security Groups

---

## 📐 Architecture

```
Internet
    ↓
Internet Gateway
    ↓
Application Load Balancer (Public - Internet Facing)
    ↓               ↓
EC2 (AZ-1)      EC2 (AZ-2)     ← Auto Scaling Group (min:1, max:3)
    ↓               ↓
    └──────┬─────────┘
           ↓
    RDS MySQL (Private Subnet)
```

---

## ✨ Features

- **Custom VPC** with public and private subnets across 2 Availability Zones
- **Application Load Balancer** distributes traffic across healthy EC2 instances
- **Auto Scaling Group** automatically adds/removes EC2s based on CPU utilization
- **RDS MySQL** in private subnet — never exposed to the internet
- **3-Layer Security Groups** — ALB → EC2 → RDS traffic isolation
- **User Data Script** — EC2 instances self-configure on launch (zero manual setup)
- **Health Check endpoint** `/health` for ALB target group monitoring
- **Visit counter** stored in RDS — proves database connectivity across instances
- **Hostname display** — proves load balancer is routing to different servers on refresh

---

## 🛠️ AWS Services Used

| Service | Purpose |
|---|---|
| **VPC** | Isolated private network with public/private subnets |
| **EC2** | Web servers running Flask app |
| **ALB** | Distributes traffic, performs health checks |
| **Auto Scaling Group** | Manages EC2 fleet based on CPU target (50%) |
| **Launch Template** | Defines EC2 config + User Data startup script |
| **RDS MySQL** | Managed relational database in private subnet |
| **Security Groups** | Layered firewall: ALB→EC2→RDS only |
| **Internet Gateway** | Allows public internet access to VPC |
| **CloudWatch** | Auto Scaling metrics and alarms |

---

## 📁 Project Structure

```
aws-autoscaling-webapp/
├── app.py           # Flask web application (Python)
├── userdata.sh      # EC2 User Data startup script
├── iam-policy.json  # IAM policy for EC2 instance role
└── README.md        # You are here
```

---

## 🚀 Deployment Guide

### Prerequisites
- AWS account (Free Tier)
- Basic AWS Console access

### Step 1 — VPC Setup
1. Create VPC using "VPC and more" wizard
2. Configure: 2 public subnets + 2 private subnets across 2 AZs
3. Enable auto-assign public IPv4 on both public subnets

### Step 2 — Security Groups (3 layers)

| Group | Inbound | Source |
|---|---|---|
| `alb-sg` | HTTP 80 | 0.0.0.0/0 |
| `ec2-sg` | HTTP 80 | alb-sg |
| `rds-sg` | MySQL 3306 | ec2-sg |

### Step 3 — RDS Database
1. Engine: MySQL 8.0, instance: `db.t3.micro`
2. Place in private subnets with `rds-sg`
3. Public access: **No**
4. Initial database name: `webappdb`

### Step 4 — Launch Template
1. AMI: Amazon Linux 2023
2. Instance type: `t2.micro`
3. Security group: `ec2-sg`
4. Paste `userdata.sh` content into User Data
5. Replace `YOUR-RDS-ENDPOINT` with actual RDS endpoint

### Step 5 — Auto Scaling Group
1. Use launch template created above
2. Select both public subnets
3. Attach to new ALB (internet-facing)
4. Target group: port 80, health check path `/health`
5. Desired: 2, Min: 1, Max: 3
6. Scaling policy: CPU target tracking at 50%

### Step 6 — Test
Open ALB DNS name in browser:
```
http://your-alb-dns.us-east-1.elb.amazonaws.com
```
Refresh multiple times — hostname changes proving load balancing works!

---

## 💰 Cost

Runs within AWS Free Tier:

| Service | Free Tier | Used |
|---|---|---|
| EC2 t2.micro | 750 hrs/month | 2 instances |
| RDS db.t3.micro | 750 hrs/month | 1 instance |
| ALB | 750 hrs/month | 1 ALB |
| VPC | Always free | 1 VPC |

> ⚠️ **To avoid charges:** Terminate EC2 instances via ASG, delete RDS, and delete ALB when not in use.

---

## 🔐 Security Design

```
Internet → ALB only (port 80)
ALB → EC2 only (port 80, from alb-sg)
EC2 → RDS only (port 3306, from ec2-sg)
RDS → No public access
```
Nobody on the internet can reach EC2 or RDS directly.

---

## 📌 Key Concepts Demonstrated

- **High Availability** — 2 AZs means one datacenter failure doesn't take down the app
- **Horizontal Scaling** — add more servers, not bigger servers
- **Infrastructure as Code mindset** — Launch Template defines everything
- **Least Privilege Security** — each layer only talks to the next layer
- **Managed Services** — RDS handles backups, patching, failover automatically
- **Self-healing** — ASG replaces failed instances automatically

---

## 👨‍💻 Author

**Akshat** — Cloud Engineer  
B.Tech CSE (IoT & Blockchain) · BBDU Lucknow · 2026  
AWS | Python | Docker | Linux | DevOps

---

## 📄 License

MIT License — free to use and modify.
