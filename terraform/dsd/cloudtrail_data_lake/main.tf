module "github-cloudtrail-auditlog" {
  source                          = "github.com/aws-samples/aws-cloudtrail-lake-github-audit-log/terraform/terraform-aws-cloudtrail-lake-github-audit-log"
  create_github_auditlog_s3bucket = var.create_github_auditlog_s3bucket
  github_auditlog_s3bucket        = var.github_auditlog_s3bucket
  cloudtrail_lake_channel_arn     = var.cloudtrail_lake_channel_arn
  github_audit_allow_list         = var.github_audit_allow_list
}