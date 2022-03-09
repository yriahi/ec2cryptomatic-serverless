## Changelog


# 1.3.0

- Rename `files` to `src`
- Move zip files to `dist` folder.
- Update `lambda-functions.tf` with `src` and `dist`.

# 1.2.0

- Upgrade providers.
- `terraform fmt`.
- Update region in `variables.tf`.

# 1.1.2

- Fix `errorMessage: 'ec2.Volume' object has no attribute 'io'`.
- Fix default `log_retention` value in `default.tfvars`
- Changed region to `us-east-1`.

# 1.1.1

- Increasing timeout and retry values for Boto3 waiters.

# 1.1.0

- Migrate to Terraform 0.12
