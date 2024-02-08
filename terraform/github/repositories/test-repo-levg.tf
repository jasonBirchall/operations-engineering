module "test-repo-levg" {
  source  = "ministryofjustice/repository/github"
  version = "0.0.6"
  providers = {
    github = github.ministryofjustice-test
  }

  name        = "test-repo-levg"
  description = "test repo"
  topics      = ["operations-engineering"]
}