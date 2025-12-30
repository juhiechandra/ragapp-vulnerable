"""
Payment gateway configuration.
Contains sensitive API keys for payment processing.
NEVER expose these keys publicly.
"""

# Stripe Configuration
STRIPE_CONFIG = {
    "publishable_key": "PLACEHOLDER_STRIPE_PUBLISHABLE_KEY",
    "secret_key": "PLACEHOLDER_STRIPE_SECRET_KEY",
    "webhook_secret": "PLACEHOLDER_STRIPE_WEBHOOK_SECRET",
    "connect_client_id": "PLACEHOLDER_STRIPE_CONNECT_CLIENT_ID"
}

# PayPal Configuration  
PAYPAL_CONFIG = {
    "client_id": "AZDxjDScFpFAKE1234567890abcdefghijklmnopqrstuvwxyz",
    "client_secret": "EGnHDjcFAKE1234567890abcdefghijklmnopqrstuvwxyzABCD",
    "mode": "live",
    "webhook_id": "WH-FAKE1234567890-ABCDEFGHIJ"
}

# Internal billing database
BILLING_DB = {
    "connection_string": "postgresql://billing_admin:B1ll1ngAdm1n!2024@billing-db.internal:5432/billing",
    "read_replica": "postgresql://billing_read:B1ll1ngR3ad!@billing-replica.internal:5432/billing"
}

# PCI DSS Encryption Keys (DO NOT SHARE)
PCI_ENCRYPTION = {
    "card_encryption_key": "pci-dss-compliant-encryption-key-32bytes!",
    "tokenization_salt": "unique-tokenization-salt-for-card-data",
    "hmac_key": "hmac-key-for-payment-signature-verification"
}

# Merchant accounts
MERCHANT_ACCOUNTS = {
    "primary": {
        "merchant_id": "MERCHANT_001_PROD",
        "terminal_id": "TERM_001",
        "api_password": "M3rch@ntP@ss2024!"
    },
    "backup": {
        "merchant_id": "MERCHANT_002_BACKUP", 
        "terminal_id": "TERM_002",
        "api_password": "B@ckupM3rch@nt!2024"
    }
}

