# GitHub Bootstrap Kit

## Windows
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\bootstrap\publish_to_github.ps1
```

## macOS / Linux
```bash
./bootstrap/publish_to_github.sh
```

The scripts initialize Git, add the official remote, commit the project and push
`main`. They do not store passwords or tokens.
