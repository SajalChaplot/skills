# Publish this framework on GitHub

This project is ready to commit. It does not include a GitHub remote or a license.

## Recommended first publication

1. Create a **private** empty GitHub repository called `design-judgment-framework` (do not initialize it with a README or license).
2. In a terminal, from this folder, run:

```bash
git init -b main
git add .
git commit -m "Initial import: Design Judgment Framework v1.2.1"
git remote add origin https://github.com/YOUR_USERNAME/design-judgment-framework.git
git push -u origin main
```

Use your own GitHub identity and credentials; do not put tokens in files or the remote URL. To publish via GitHub CLI, `gh repo create design-judgment-framework --private --source=. --remote=origin --push` can replace the repository creation, remote and push steps once the project is committed and `gh auth login` has been completed.

Before making this repository public, review the contents and select an appropriate license.

## Verification

```bash
python3 -m unittest discover -s tests -v
```
