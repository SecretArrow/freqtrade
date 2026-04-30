#!/bin/bash
# QuantumEdge Bot Starter - Complete startup with all features
# Usage: ./start_quantum_edge.sh [options]
#
# Options:
#   --guardian    Start with BotGuardian (auto-restart, monitoring)
#   --dry-run     Start in dry-run mode (default)
#   --live        Start in live trading mode
#   --futures     Start in futures mode (default)
#   --spot        Start in spot mode
#   --strategy    Specify strategy name

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FREQTRADE_DIR="$SCRIPT_DIR"
USER_DATA="$SCRIPT_DIR/user_data"
CONFIG="$USER_DATA/config.json"
STRATEGIES_DIR="$USER_DATA/strategies"

# Git config
GIT_TOKEN="${GIT_TOKEN:-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}"
GIT_REPO="https://github.com/SecretArrow/freqtrade.git"

# Default settings
USE_GUARDIAN=false
DRY_RUN=true
TRADING_MODE="futures"
STRATEGY="QuantumEdge_Adaptive"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║     🤖 QUANTUMEDGE TRADING BOT v2.0 🤖                   ║"
    echo "║                                                           ║"
    echo "║     AI-Powered • Self-Healing • Auto-Backup               ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_requirements() {
    log_info "Checking requirements..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 not found!"
        exit 1
    fi

    # Check if freqtrade is installed
    if ! python3 -c "import freqtrade" 2>/dev/null; then
        log_info "Installing freqtrade..."
        pip install -e "$FREQTRADE_DIR" -q
    fi

    # Check psutil for system monitoring
    if ! python3 -c "import psutil" 2>/dev/null; then
        log_info "Installing psutil for system monitoring..."
        pip install psutil -q
    fi

    # Check config exists
    if [ ! -f "$CONFIG" ]; then
        log_error "Config file not found: $CONFIG"
        exit 1
    fi

    log_success "All requirements met!"
}

git_sync() {
    log_info "Syncing with GitHub..."

    cd "$FREQTRADE_DIR"

    # Configure git
    git config user.email "bot@freqtrade.local" 2>/dev/null || true
    git config user.name "QuantumEdge Bot" 2>/dev/null || true

    # Set remote with token
    git remote set-url origin "https://x-access-token:${GIT_TOKEN}@github.com/SecretArrow/freqtrade.git" 2>/dev/null || true

    # Try to pull first
    if git pull origin main 2>/dev/null; then
        log_success "Synced from GitHub"
    else
        log_warning "Could not pull from GitHub (might be up to date)"
    fi
}

git_push() {
    log_info "Backing up to GitHub..."

    cd "$FREQTRADE_DIR"

    git config user.email "bot@freqtrade.local" 2>/dev/null || true
    git config user.name "QuantumEdge Bot" 2>/dev/null || true

    git remote set-url origin "https://x-access-token:${GIT_TOKEN}@github.com/SecretArrow/freqtrade.git" 2>/dev/null || true

    # Add all changes
    git add -A

    # Commit
    if git diff --cached --quiet; then
        log_info "Nothing to commit"
    else
        git commit -m "Auto-backup - $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null || true

        # Push
        if git push origin main 2>/dev/null; then
            log_success "Backed up to GitHub"
        else
            log_warning "Could not push to GitHub"
        fi
    fi
}

update_config() {
    log_info "Updating config..."

    # Update dry_run mode
    if [ "$DRY_RUN" = true ]; then
        sed -i 's/"dry_run": false/"dry_run": true/' "$CONFIG" 2>/dev/null || true
        sed -i 's/"dry_run_wallet": [0-9]*/"dry_run_wallet": 100/' "$CONFIG" 2>/dev/null || true
    else
        sed -i 's/"dry_run": true/"dry_run": false/' "$CONFIG" 2>/dev/null || true
    fi

    # Update trading mode
    sed -i "s/\"trading_mode\": \"[^\"]*\"/\"trading_mode\": \"$TRADING_MODE\"/" "$CONFIG" 2>/dev/null || true

    log_success "Config updated!"
}

start_guardian() {
    log_info "Starting BotGuardian..."

    cd "$FREQTRADE_DIR"

    # Export git token for bot_guardian
    export GIT_TOKEN="$GIT_TOKEN"

    # Run guardian
    python3 "$USER_DATA/bot_guardian.py" "$CONFIG" &

    log_success "BotGuardian started!"
    log_info "Use 'tail -f $USER_DATA/logs/freqtrade.log' to see logs"
}

start_bot() {
    log_info "Starting FreqTrade Bot..."

    cd "$FREQTRADE_DIR"

    # Run freqtrade
    python3 -m freqtrade trade \
        --config "$CONFIG" \
        --strategy "$STRATEGY" \
        2>&1 | tee -a "$USER_DATA/logs/freqtrade.log" &

    BOT_PID=$!
    log_success "FreqTrade started! (PID: $BOT_PID)"
    log_info "Use 'tail -f $USER_DATA/logs/freqtrade.log' to see logs"
}

show_help() {
    echo "QuantumEdge Bot Starter"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --guardian    Start with BotGuardian (auto-restart, monitoring)"
    echo "  --dry-run     Start in dry-run mode (default)"
    echo "  --live        Start in live trading mode"
    echo "  --futures     Start in futures mode (default)"
    echo "  --spot        Start in spot mode"
    echo "  --strategy    Specify strategy name"
    echo "  --sync        Sync from GitHub before start"
    echo "  --backup      Backup to GitHub before start"
    echo "  --help        Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 --guardian --dry-run --strategy QuantumEdge_Adaptive"
    echo "  $0 --live --futures --backup"
    echo "  $0 --sync --guardian"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --guardian)
            USE_GUARDIAN=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --live)
            DRY_RUN=false
            shift
            ;;
        --futures)
            TRADING_MODE="futures"
            shift
            ;;
        --spot)
            TRADING_MODE="spot"
            shift
            ;;
        --strategy)
            STRATEGY="$2"
            shift 2
            ;;
        --sync)
            DO_SYNC=true
            shift
            ;;
        --backup)
            DO_BACKUP=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main
main() {
    show_banner

    echo "Mode: $([ "$DRY_RUN" = true ] && echo "DRY RUN ⚪️" || echo "LIVE 🟢")"
    echo "Trading: $TRADING_MODE"
    echo "Strategy: $STRATEGY"
    echo "Guardian: $([ "$USE_GUARDIAN" = true ] && echo "ON 🛡️" || echo "OFF")"
    echo ""

    # Check requirements
    check_requirements

    # Git sync if requested
    if [ "$DO_SYNC" = true ]; then
        git_sync
    fi

    # Git backup if requested
    if [ "$DO_BACKUP" = true ]; then
        git_push
    fi

    # Update config
    update_config

    # Start
    if [ "$USE_GUARDIAN" = true ]; then
        start_guardian
    else
        start_bot
    fi

    echo ""
    log_success "QuantumEdge Bot is starting!"
    log_info "Check Telegram for bot status"
    log_info "Press Ctrl+C to stop"

    # Wait
    trap "log_info 'Shutting down...'; kill 0 2>/dev/null; exit 0" SIGINT SIGTERM
    wait
}

main