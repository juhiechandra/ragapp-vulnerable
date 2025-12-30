"""
Internal SSH key configuration for deployment automation.
These keys are used for automated deployments and should be rotated regularly.
"""

# SSH Private Key for production deployment
DEPLOY_PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZgAAAJgAAAAAAAAA
AGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYAAAAAAAAAAAAAAAAtzc2gtZWQy
NTUxOQAAACBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZgAAAJgAAAAAAAAA
DEPLOY_KEY_FAKE_1234567890abcdefghijklmnopqrstuvwxyz
-----END OPENSSH PRIVATE KEY-----"""

# Deployment server credentials
DEPLOY_SERVERS = {
    "production": {
        "host": "prod-deploy.internal.corp.net",
        "user": "deploy",
        "port": 22,
        "key": DEPLOY_PRIVATE_KEY
    },
    "staging": {
        "host": "staging-deploy.internal.corp.net", 
        "user": "deploy",
        "port": 22,
        "password": "StagingDeploy2024!"
    }
}

# Database migration credentials
DB_MIGRATION_CREDS = {
    "host": "prod-db.internal.corp.net",
    "user": "migration_admin",
    "password": "M1gr@t10nAdm1n!2024",
    "database": "ragapp_production"
}

# Cloud provider tokens
CLOUD_TOKENS = {
    "digitalocean": "dop_v1_fake1234567890abcdefghijklmnopqrstuvwxyzABCDEF",
    "linode": "lin_fake1234567890abcdefghijklmnopqrstuvwxyz",
    "vultr": "VULTR_FAKE_API_KEY_1234567890ABCDEF"
}

