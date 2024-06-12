module "terraform-github-repository" {
  source  = "ministryofjustice/repository/github"
  version = var.module_version

  name            = "terraform-github-repository"
  description     = "A Terraform module for GitHub repositories in the Ministry of Justice"
  has_discussions = true
  topics          = ["operations-engineering", "github", "terraform", "terraform-module"]
  type            = "module"

  team_access = {
    admin = [var.operations_engineering_team_id]
  }
}
