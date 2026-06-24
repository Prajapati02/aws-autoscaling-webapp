# 🗄️ AWS S3 Backup Automation Bot

An event-driven, serverless backup system built on AWS that automatically copies files from a source S3 bucket to a backup bucket on a daily schedule — with email alerts on failure.

> **Built with:** Python · AWS Lambda · Amazon S3 · EventBridge · SNS · IAM · CloudWatch

---

## 📐 Architecture

```
EventBridge (cron: daily 2AM UTC)
          │
          ▼
   Lambda Function (Python 3.12)
          │
    ┌─────┴─────┐
    ▼           ▼
Source S3    Backup S3
Bucket       Bucket
             └── backup/
                 └── 2026-06-22_02-00-00/
                     └── your-files...
          │
          ▼ (on failure only)
    SNS Topic → Email Alert
```

---

## ✨ Features

- **Fully automated** — runs every day at 2AM UTC via EventBridge cron
- **Timestamped backups** — each run creates an isolated `backup/YYYY-MM-DD_HH-MM-SS/` folder
- **Partial failure handling** — if one file fails, the rest continue copying
- **Email alerts** — SNS notifies you instantly on any failure
- **Auto-cleanup** — S3 Lifecycle Policy deletes backups older than 30 days
- **Zero cost** — runs entirely within AWS Free Tier limits
- **Least privilege IAM** — Lambda role has only the exact permissions it needs

---

## 🛠️ AWS Services Used

| Service | Purpose |
|---|---|
| **AWS Lambda** | Runs the Python backup logic serverlessly |
| **Amazon S3** | Source and backup bucket storage |
| **EventBridge** | Cron scheduler — triggers Lambda daily |
| **Amazon SNS** | Email alerts on backup failure |
| **IAM** | Custom role and policy for Lambda permissions |
| **CloudWatch Logs** | Logs every backup run for monitoring |

---

## 📁 Project Structure

```
aws-s3-backup-bot/
├── lambda_function.py   # Main Lambda handler (Python)
├── iam-policy.json      # IAM policy for least-privilege access
└── README.md            # You are here
```

---

## 🚀 Deployment Guide

### Prerequisites
- AWS account (Free Tier)
- Two S3 buckets created in the same region
- SNS topic with email subscription confirmed

### Step 1 — IAM Setup
1. Create policy using `iam-policy.json` — update bucket names to match yours
2. Create role `s3-backup-bot-role` with trusted entity: **Lambda**
3. Attach the policy to the role

### Step 2 — S3 Buckets
1. Create source bucket (versioning optional)
2. Create backup bucket — **enable versioning**
3. Add Lifecycle Policy on backup bucket: expire objects after **30 days**

### Step 3 — SNS Alerts
1. Create Standard SNS topic: `backup-alerts`
2. Add Email subscription and confirm via email

### Step 4 — Lambda Function
1. Create Lambda function — runtime **Python 3.12**
2. Attach `s3-backup-bot-role`
3. Paste code from `lambda_function.py`
4. Set environment variables:

| Key | Value |
|---|---|
| `SOURCE_BUCKET` | your-source-bucket-name |
| `BACKUP_BUCKET` | your-backup-bucket-name |
| `SNS_TOPIC_ARN` | arn:aws:sns:region:account-id:backup-alerts |

5. Set timeout to **5 minutes**

### Step 5 — Schedule
1. Add EventBridge trigger to Lambda
2. Schedule expression: `cron(0 2 * * ? *)`

---

## 🧪 Testing

1. Upload any file to source bucket
2. Go to Lambda → Test tab → Create test event → Run
3. Expected response:
```json
{
  "status": "success",
  "copied": 1,
  "failed": 0
}
```
4. Verify timestamped folder appears in backup bucket
5. Check logs in CloudWatch → Log Groups → `/aws/lambda/s3-backup-bot`

---

## 💰 Cost

This project runs at **$0/month** within AWS Free Tier:

| Service | Free Tier Limit | This Project Uses |
|---|---|---|
| Lambda | 1M requests/month | ~30 runs/month |
| S3 | 5GB storage | A few KB |
| SNS | 1,000 emails/month | ~30/month |
| CloudWatch | 5GB logs/month | A few KB |
| EventBridge | 14M events/month | 30 events/month |

---

## 📌 Key Concepts Demonstrated

- **Serverless architecture** — no EC2, no servers to manage
- **Event-driven design** — Lambda triggered automatically by EventBridge
- **IAM least privilege** — role scoped to only required S3 and SNS actions
- **Operational best practices** — logging, alerting, auto-cleanup, error handling
- **Infrastructure as Code mindset** — all config stored as code/JSON

---

## 👨‍💻 Author

**Akshat** — Cloud Engineer  
B.Tech CSE (IoT & Blockchain) · BBDU Lucknow · 2026  
AWS | Python | Docker | Linux | DevOps

---

## 📄 License

MIT License — free to use and modify.
