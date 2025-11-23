# Code Review

Simple notes on code review

## Dependency Confusion

We can use `confused` to scan package requirement file

```
git clone https://github.com/visma-prodsec/confused 
cd confused
go get 
go build
```

* Usage

```
confused -l pip requirements.txt
confused -l npm package.json # default
confused -l composer composer.json
confused -l mvn pom.xml
confused -l rubygems Gemfile.lock
```

## Hijacking Dependencies

### Python-pip

* <https://github.com/zAbuQasem/dependecy-confusion-templates/tree/main/python-pip>

### Nodejs-npm

* TODO

## Static Application Security Analysis (SAST)

Here are a set of tools I usually use when I conduct a source code review:

* [**Semgrep**](https://github.com/returntocorp/semgrep): It has a good set of rules for pointing out weak code practices.

```
python3 -m pip install semgrep
semgrep --config auto | tee -a semgrep.out
```

* **Snyk**: Snyk is good (Available Vscode extension)
* **Trivy**:Built mainly for container security, it's suitable for dependency vulnerability scanning. (Available Vscode extension)

## Secrets Scanning

I personally prefer [gitleaks](https://github.com/zricethezav/gitleaks) for scanning a git repo, Because it points out informative information beside the secret.

```
# Require golang to be installed
git clone https://github.com/zricethezav/gitleaks.git
cd gitleaks
make build

# Usage
gitleaks detect --report-path gitleaks-report.json -v
```

For scanning container images for secrets and vulnerabilities, i would use [trivy](https://github.com/aquasecurity/trivy).

```
sudo apt install -y trivy
trivy image --severity HIGH,CRITICAL --security-checks vuln,secret,config <image> 
# Append --offline-scan to scan a local image
```

Other than that [trufflehog](https://github.com/trufflesecurity/trufflehog) is good.

```
git clone https://github.com/trufflesecurity/trufflehog.git
cd trufflehog
go install
```

```
# Scan a repo
trufflehog git <REPO-URL> --only-verified --json
# Scan a github organization
trufflehog git https://github.com/trufflesecurity/test_keys --only-verified --json
# Scan filesystem
trufflehog filesystem --directory <PATH> --json [--only-verified]
```

