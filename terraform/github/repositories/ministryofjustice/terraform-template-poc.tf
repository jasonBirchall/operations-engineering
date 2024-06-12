module "terraform-template-poc" {
  source  = "ministryofjustice/repository/github"
  version = var.module_version

  name        = "terraform-template-poc"
  type        = "template"
  description = "A Proof of Concept for a resilient and scalable Terraform template, suitable for team use"
  topics      = ["operations-engineering", "standards-compliant"]

  team_access = {
    admin = [var.operations_engineering_team_id]
  }
}
