module "tech-docs-github-pages-publisher" {
  source  = "ministryofjustice/repository/github"
  version = "0.0.3"

  name             = "tech-docs-github-pages-publisher"
  application_name = "tech-docs-github-pages-publisher"
  description      = "Docker image to publish MoJ documentation repositories as github pages sites"
  homepage_url     = "https://hub.docker.com/r/ministryofjustice/tech-docs-github-pages-publisher"
}