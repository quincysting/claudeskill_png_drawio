"""Verified AWS mxgraph.aws4 resourceIcon names + category colours.

Every name below was confirmed to RENDER (not a blank tile) in draw.io desktop
30.x via the verify_icons.py loop. Keys are short aliases; values are
(resIcon_name, category). See references/aws4-icon-map.md for the known-BLANK
names to avoid. Add a new entry ONLY after verifying it renders.
"""

# alias -> (mxgraph.aws4 resIcon name, category)
AWS4 = {
    # storage
    "s3": ("s3", "storage"),
    # analytics (purple)
    "glue": ("glue", "analytics"), "athena": ("athena", "analytics"),
    "lakeformation": ("lake_formation", "analytics"),
    "kinesis": ("kinesis_data_streams", "analytics"),
    "firehose": ("kinesis_data_firehose", "analytics"),
    "quicksight": ("quicksight", "analytics"),
    "opensearch": ("elasticsearch_service", "analytics"),   # NOT opensearch_service
    "emr": ("emr", "analytics"), "databrew": ("glue_databrew", "analytics"),
    # security / identity (red)
    "kms": ("key_management_service", "security"), "macie": ("macie", "security"),
    "secrets": ("secrets_manager", "security"),
    "iam": ("identity_and_access_management", "security"),  # NOT iam_identity_center
    "sso": ("single_sign_on", "security"), "shield": ("shield", "security"),
    "detective": ("detective", "security"), "guardduty": ("guardduty", "security"),
    "seclake": ("security_lake", "security"),
    "nacl": ("network_access_control_list", "security"),
    # ml / ai (teal)
    "sagemaker": ("sagemaker", "ml"),                       # NOT sagemaker_ai
    "bedrock": ("bedrock", "ml"),                           # NOT amazon_bedrock
    "comprehend": ("comprehend", "ml"), "kendra": ("kendra", "ml"),
    "qbiz": ("q", "ml"), "rekognition": ("rekognition", "ml"),
    "augmented_ai": ("augmented_ai", "ml"),
    # compute (orange)
    "lambda": ("lambda", "compute"), "ec2": ("ec2", "compute"),
    "eks": ("eks", "compute"),                              # NOT elastic_kubernetes_service
    "server": ("traditional_server", "general"),
    # app integration (pink)
    "sfn": ("step_functions", "appint"), "eventbridge": ("eventbridge", "appint"),
    "apigw": ("api_gateway", "appint"), "mq": ("mq", "appint"),
    "appint": ("application_integration", "appint"),
    # management (magenta)
    "ssm": ("systems_manager", "mgmt"), "cw": ("cloudwatch", "mgmt"),
    "cloudtrail": ("cloudtrail", "mgmt"), "trail": ("cloudtrail", "mgmt"),
    "config": ("config", "mgmt"), "xray": ("xray", "mgmt"),
    # networking (deep purple)
    "tgw": ("transit_gateway", "net"), "dx": ("direct_connect", "net"),
    "vpc": ("virtual_private_cloud", "net"), "igw": ("internet_gateway", "net"),
    "internet": ("internet_gateway", "net"), "nat": ("nat_gateway", "net"),
    "alb": ("elastic_load_balancing_application_load_balancer", "net"),
    "vpn": ("site_to_site_vpn", "net"), "router": ("router", "net"),
    "rtb": ("route_table", "net"), "endpoints": ("endpoints", "net"),
    "eni": ("elastic_network_interface", "net"),
    # databases (blue)
    "rds": ("rds", "db"), "aurora": ("aurora", "db"), "dynamodb": ("dynamodb", "db"),
    # generic (blue)
    "users": ("users", "general"), "user": ("user", "general"),
    "onprem": ("corporate_data_center", "general"),
}

# category -> (fill, gradient) — the AWS-ish tile colour
CAT = {
    "storage": ("#277116", "#7AA116"), "analytics": ("#4D27AA", "#945DF2"),
    "security": ("#BD0816", "#FF5252"), "ml": ("#055F4E", "#56C0A7"),
    "compute": ("#D45B07", "#F78E04"), "appint": ("#B0084D", "#FF4F8B"),
    "mgmt": ("#7D2105", "#E7157B"), "net": ("#5A30B5", "#945DF2"),
    "general": ("#3334B9", "#4D72F3"), "db": ("#2E27AD", "#527FFF"),
}

def soft(h, t=0.45):
    """Blend a hex colour toward white by t (0..1). Used to lighten borders so
    dense diagrams read calmer. Pass-through for 'none'."""
    if not h or h == "none":
        return h
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return "#%02X%02X%02X" % (int(r + (255 - r) * t), int(g + (255 - g) * t), int(b + (255 - b) * t))
