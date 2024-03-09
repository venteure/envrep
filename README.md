# Environment Variable Replacer or envrep

GitHub Action `envrep` replaces placeholders in files (.yaml, .yml, .json, etc.)
within a specified directory with environment variable values.
Ideal for updating Kubernetes manifests, Docker compose files,
and other JSON/YAML configurations in CI/CD workflows.

## Features

- Supports a variety of file extensions, including `.yaml`, `.yml`, `.json`, `.conf`, and `.hcl` by default.
  You can specify additional extensions to process or override the default list by using the `extensions` parameter.
- Supports secrets by encoding them as base64 strings and replacing placeholders with the encoded values.
- Recursively processes files in the specified directory.
- Replaces placeholders formatted as `$(VAR_NAME)` with the corresponding environment variable `VAR_NAME` values.

## Usage

To use `envrep` in your GitHub Actions workflow, add a step that uses this action
after checking out your repository and setting any necessary environment variables.
Placeholders in your files should be formatted as `$(VAR_NAME)`, where `VAR_NAME` is the
name of an environment variable you've defined in your workflow or in the action's `env` block.

For secrets that needs to be encoded as base64 strings, use `$*(VAR_NAME)` format.s

### Basic Example

This example demonstrates using `envrep` to process files in the `k8s` directory:

```yaml
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Replace values in YAML and JSON files
        uses: venteure/envrep@v0.1.0
        with:
          directory: k8s
        env:
          COMMIT_SHA: ${{ github.sha }}
          IMAGE_TAG: dev
```

### Parameters

- `directory`: The directory where your `.yaml`, `.yml`, and `.json` files are located. This path is relative to the
  root of your repository.
- `extensions`: (Optional) A comma-separated list of file extensions to process. Defaults to `yaml,yml,json,conf,hcl`.

### Environment Variables

You can define any number of environment variables to be used for replacement in your files. For each placeholder in
your files, ensure there is a matching environment variable defined in the workflow or the action's `env` block.

### Placeholder Format

Placeholders in your files should follow the format `$(VAR_NAME)`, where `VAR_NAME` is the name of the environment
variable whose value should replace the placeholder.

### Example File Before Replacement

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  externalIPs:
    - $(SITE_ADDRESS)
```

### Example File After Replacement

Assuming `SITE_ADDRESS` is set to `example.com`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  externalIPs:
    - example.com
```

## Contributing

Contributions are welcome! If you have a feature request, bug report, or a pull request, please open an issue or submit
a PR to the repository.