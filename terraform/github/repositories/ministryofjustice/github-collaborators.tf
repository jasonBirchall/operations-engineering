module "github-collaborators" {
  source  = "ministryofjustice/repository/github"
  version = var.module_version

  name            = "github-collaborators"
  description     = "Manage outside collaborators on our Github repositories"
  has_discussions = true
  topics          = ["operations-engineering"]

  team_access = {
    admin = [var.operations_engineering_team_id]
  }
}
