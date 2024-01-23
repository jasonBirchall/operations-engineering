module "moj-terraform-scim-github" {
  source = "github.com/ministryofjustice/operations-engineering-terraform-github-repositories"

  name             = "moj-terraform-scim-github"
  application_name = "moj-terraform-scim-github"
  description      = "Lambda function for automatic SCIM provisioning based on GitHub relationships"
  tags = {
    Team  = "operations-engineering"
    Phase = "production"
  }
}