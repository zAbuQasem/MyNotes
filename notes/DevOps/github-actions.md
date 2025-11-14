## GitHub OIDC with AWS

If you’re running into issues with the **trust policy `sub` claim**, you can debug by retrieving the ID token using this workflow:

```yaml
name: id-token

on:
  workflow_dispatch:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  get-id-token:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - name: Get OIDC Token
        run: |
          ID_TOKEN=$(curl -s -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
            "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=api://demo" | jq -r .value)
          echo "$ID_TOKEN" | base32
```

Once you have the decoded token, check the `sub` claim and make sure it matches what your IAM role’s trust policy expects.

### Example Trust Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:sub": [
                        "repo:<ORG>/<REPO>:ref:refs/heads/main",
                        "repo:<ORG>/<REPO>:pull_request"
                    ],
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```

* Replace `<ACCOUNT_ID>`, `<ORG>`, and `<REPO>` with your values.
* The `sub` claim typically follows the format:

  ```
  repo:<ORG>/<REPO>:ref:refs/heads/<BRANCH>
  ```

### References

* [StackOverflow: Error not authorized to perform `sts:AssumeRoleWithWebIdentity` during OIDC](https://stackoverflow.com/questions/78746014/error-not-authorized-to-perform-stsassumerolewithwebidentity-during-oidc-when)
