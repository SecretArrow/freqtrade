#!/bin/bash
# QuantumEdge Git Sync - Silent Auto Push/Pull
# Token tersimpan di .git_token (di-gitignore)

TOKEN=$(cat .git_token 2>/dev/null || echo "")

if [ -z "$TOKEN" ]; then
    echo "Token not found. Please ensure .git_token exists"
    exit 1
fi

cd /home/testnet-warden/freqtrade

# Set remote with token
git remote set-url origin "https://${TOKEN}@github.com/SecretArrow/freqtrade.git"

case "${1:-push}" in
    push)
        echo "Pushing to GitHub..."
        git push origin stable
        ;;
    pull)
        echo "Pulling from GitHub..."
        git pull origin stable
        ;;
    sync)
        echo "Syncing with GitHub..."
        git pull origin stable && git push origin stable
        ;;
    status)
        git status
        ;;
    *)
        echo "Usage: ./git_sync.sh [push|pull|sync|status]"
        ;;
esac