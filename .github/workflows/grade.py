name: Autograding

on: pull_request

env:
  internal_pat: ${{ secrets.ORG_PAT }}
  is_local: ${{ env.ACT || 'false' }}
  pr_number: ${{ github.event.number }}
  repository: ${{ github.repository }}

jobs:
  autograding:
    runs-on: ubuntu-22.04
    steps:
      - name: Environment variables
        if: ${{ env.is_local == 'true' }}
        run: |
          echo ${{ env.internal_pat }}
          echo ${{ env.is_local }}
          echo ${{ env.pr_number }}
      - name: Installing Python (only on act)
        if: ${{ env.is_local == 'true' }}
        run: | 
          apt update
          apt install -y python3 python3-pip git
      - name: Repository name
        if: ${{ env.is_local == 'true' }}
        run: echo ${{ github.repository }} | cut -d'/' -f2
      - name: Set repository name
        run: echo "REPO_NAME=$(echo ${{ github.repository }} | cut -d'/' -f2)" >> $GITHUB_ENV
      - name: Get repo name
        if: ${{ env.is_local == 'true' }}
        run: echo ${{ env.REPO_NAME }}
      - name: PAT
        if: ${{ env.is_local == 'true' }}
        run: echo ${{ secrets.ORG_PAT }}
      - name: Checking out current repository
        uses: actions/checkout@v4
        with:
          path: main
      - name: Checking out solutions repository
        uses: actions/checkout@v4
        with:
          repository: git-mastery/solution-${{ env.REPO_NAME }}
          token: ${{ secrets.ORG_PAT }}
          path: solution/
      - name: Current file structure
        if: ${{ env.is_local == 'true' }}
        run: ls ../*/* -a
      - name: Setup Python (only on Github Actions)
        if: ${{ env.is_local == 'false' }}
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Installing GitPython
        run: |
          pip install GitPython PyGithub
      - name: Run Python
        run: python3 grade.py
        working-directory: solution
            

