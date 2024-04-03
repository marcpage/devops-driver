# How to deploy

## System setup for deploying

```bash
$ make venv
$ source .venv/bin/activate
$ python -m devopsdriver.setings --set_secrets
pypi_test.password (pypi_test/token): *********
pypi_prod.password (pypi/token): *********
$ 
```

## Deploy

1. Make sure `__version__` is updated to a version that does not exist on the test or productin PyPI server
2. Update the versions in `README.md` (twice in `status sheild`)
3. Execute `make deploy`
4. Create a PR with your changes after a successful deployment
5. After the PR merges, create a new release in GitHub
