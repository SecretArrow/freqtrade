#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
#  QuantumEdge Auto Installer & Setup
#  Complete installation script with interactive setup
# ═══════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/SecretArrow/freqtrade.git"
INSTALL_DIR="/home/testnet-warden/freqtrade"
GIT_TOKEN="${GIT_TOKEN:-}"

# ═══════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

log_error() {
    echo -e "${RED}[❌]${NC} $1"
}

ask() {
    echo -e "${CYAN}[?${NC}] $1"
}

ask_password() {
    echo -ne "${CYAN}[?${NC}] $1: "
    read -s password
    echo
    echo "$password"
}

confirm() {
    echo -ne "${CYAN}[?${NC}] $1 [y/N]: "
    read answer
    [[ "$answer" =~ ^[Yy]$ ]]
}

section() {
    echo ""
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  $1${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════
# Banner
# ═══════════════════════════════════════════════════════════════════

show_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🤖 QUANTUMEDGE TRADING BOT                               ║
    ║     Auto Installer & Setup                                   ║
    ║                                                               ║
    ║     AI-Powered • Multi-Provider • Auto Alert                  ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════
# System Checks
# ═══════════════════════════════════════════════════════════════════

check_system() {
    section "System Requirements"

    # Check OS
    log "Checking OS..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_success "Linux detected"
    else
        log_warning "Non-Linux OS detected. Some features may not work."
    fi

    # Check Python
    log "Checking Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python3 not found. Please install Python 3.10+"
        exit 1
    fi

    # Check pip
    log "Checking pip..."
    if python3 -m pip --version &> /dev/null; then
        log_success "pip found"
    else
        log_warning "pip not found, installing..."
        python3 -m ensurepip --default-pip 2>/dev/null || true
    fi

    # Check git
    log "Checking git..."
    if command -v git &> /dev/null; then
        log_success "git found"
    else
        log_warning "git not found, installing..."
        apt-get update && apt-get install -y git 2>/dev/null || sudo apt-get update && sudo apt-get install -y git 2>/dev/null || true
    fi

    # Check disk space
    log "Checking disk space..."
    FREE_SPACE=$(df -h / | tail -1 | awk '{print $4}')
    log_success "Free space: $FREE_SPACE"
}

# ═══════════════════════════════════════════════════════════════════
# Dependencies Installation
# ═══════════════════════════════════════════════════════════════════

install_dependencies() {
    section "Installing Dependencies"

    # Update packages
    log "Updating package list..."
    sudo apt-get update -qq 2>/dev/null || apt-get update -qq 2>/dev/null || true

    # Essential packages
    log "Installing essential packages..."
    sudo apt-get install -y \
        python3 python3-pip python3-venv \
        git curl wget htop \
        build-essential libssl-dev libffi-dev \
        2>/dev/null || \
    apt-get install -y \
        python3 python3-pip python3-venv \
        git curl wget htop \
        build-essential libssl-dev libffi-dev \
        2>/dev/null || true

    # Install psutil for system monitoring
    log "Installing psutil..."
    pip install psutil --quiet 2>/dev/null || pip3 install psutil --quiet 2>/dev/null || true

    log_success "Dependencies installed"
}

# ═══════════════════════════════════════════════════════════════════
# Repository Setup
# ═══════════════════════════════════════════════════════════════════

setup_repository() {
    section "Repository Setup"

    if [ -d "$INSTALL_DIR/.git" ]; then
        log "Repository already exists at $INSTALL_DIR"

        if confirm "Pull latest changes from GitHub?"; then
            cd "$INSTALL_DIR"
            git remote set-url origin "https://x-access-token:${GIT_TOKEN}@github.com/SecretArrow/freqtrade.git" 2>/dev/null || true
            git pull origin main 2>/dev/null || git pull origin stable 2>/dev/null || true
            log_success "Repository updated"
        fi
    else
        ask "Install directory [$INSTALL_DIR]: "
        read -e input_dir
        INSTALL_DIR="${input_dir:-$INSTALL_DIR}"

        log "Cloning repository..."
        mkdir -p "$(dirname "$INSTALL_DIR")"

        if [ -n "$GIT_TOKEN" ]; then
            git clone "https://x-access-token:${GIT_TOKEN}@github.com/SecretArrow/freqtrade.git" "$INSTALL_DIR" 2>/dev/null || \
            git clone "$REPO_URL" "$INSTALL_DIR"
        else
            git clone "$REPO_URL" "$INSTALL_DIR"
        fi

        log_success "Repository cloned to $INSTALL_DIR"
    fi

    cd "$INSTALL_DIR"
}

# ═══════════════════════════════════════════════════════════════════
# Virtual Environment
# ═══════════════════════════════════════════════════════════════════

setup_venv() {
    section "Python Virtual Environment"

    if [ -d "$INSTALL_DIR/.venv" ]; then
        log "Virtual environment already exists"

        if confirm "Recreate virtual environment?"; then
            log "Removing old venv..."
            rm -rf "$INSTALL_DIR/.venv"
            python3 -m venv .venv
            log_success "Virtual environment recreated"
        fi
    else
        log "Creating virtual environment..."
        python3 -m venv .venv
        log_success "Virtual environment created"
    fi

    log "Activating virtual environment..."
    source .venv/bin/activate

    log "Upgrading pip..."
    pip install --upgrade pip --quiet

    log "Installing freqtrade..."
    pip install -e . --quiet 2>/dev/null || pip install -e .

    log_success "FreqTrade installed"
}

# ═══════════════════════════════════════════════════════════════════
# AI Provider Setup
# ═══════════════════════════════════════════════════════════════════

setup_ai_providers() {
    section "AI Provider Setup"

    echo "Supported AI Providers:"
    echo ""
    echo "  ${GREEN}FREE:${NC}"
    echo "    1. OpenRouter  - Free models (llama-3.2, mistral)"
    echo "    2. Ollama      - 100% local, no internet needed"
    echo "    3. KiloCode    - Free tier available"
    echo "    4. OpenCode    - Free tier available"
    echo ""
    echo "  ${YELLOW}PAID:${NC}"
    echo "    5. OpenAI      - GPT-4, GPT-3.5"
    echo "    6. Claude      - Anthropic's Claude"
    echo "    7. Gemini      - Google's Gemini"
    echo "    8. NVIDIA AI   - Mixtral, Llama models"
    echo ""

    # Get API keys
    echo -e "${BOLD}API Key Setup (optional - press Enter to skip)${NC}"
    echo "You can also set these via environment variables later"
    echo ""

    # OpenRouter
    echo -e "${CYAN}── OpenRouter (Recommended - FREE models) ──${NC}"
    ask "  API Key: "
    read -e OPENROUTER_KEY
    if [ -n "$OPENROUTER_KEY" ]; then
        export OPENROUTER_API_KEY="$OPENROUTER_KEY"
        log_success "OpenRouter key set"
    fi

    # Ollama (check if installed)
    echo -e "${CYAN}── Ollama (100% FREE, local) ──${NC}"
    if command -v ollama &> /dev/null; then
        log "Ollama is installed"
        OLLAMA_INSTALLED=true
        ask "Model [llama3.2]: "
        read -e OLLAMA_MODEL
        OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2}"
        export OLLAMA_MODEL
        log_success "Ollama configured"
    else
        log_warning "Ollama not installed"
        if confirm "Install Ollama?"; then
            curl -fsSL https://ollama.ai/install.sh | sh
            if command -v ollama &> /dev/null; then
                log_success "Ollama installed"
                OLLAMA_INSTALLED=true
                export OLLAMA_MODEL="llama3.2"
                log "Run 'ollama pull llama3.2' to download model"
            fi
        fi
    fi

    # OpenAI
    echo -e "${CYAN}── OpenAI (GPT-4) ──${NC}"
    ask "  API Key (or Enter to skip): "
    read -e OPENAI_KEY
    if [ -n "$OPENAI_KEY" ]; then
        export OPENAI_API_KEY="$OPENAI_KEY"
        log_success "OpenAI key set"
    fi

    # Claude
    echo -e "${CYAN}── Claude (Anthropic) ──${NC}"
    ask "  API Key (or Enter to skip): "
    read -e ANTHROPIC_KEY
    if [ -n "$ANTHROPIC_KEY" ]; then
        export ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
        log_success "Claude key set"
    fi

    # Gemini
    echo -e "${CYAN}── Gemini (Google) ──${NC}"
    ask "  API Key (or Enter to skip): "
    read -e GEMINI_KEY
    if [ -n "$GEMINI_KEY" ]; then
        export GEMINI_API_KEY="$GEMINI_KEY"
        log_success "Gemini key set"
    fi

    # Save to .env
    save_env_file

    log_success "AI providers configured"
}

save_env_file() {
    cat > "$INSTALL_DIR/.env" << EOF
# QuantumEdge Environment Variables
# Generated by installer on $(date)

# AI Providers
EOF

    [ -n "$OPENROUTER_API_KEY" ] && echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" >> "$INSTALL_DIR/.env"
    [ -n "$OPENAI_API_KEY" ] && echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> "$INSTALL_DIR/.env"
    [ -n "$ANTHROPIC_API_KEY" ] && echo "ANTHROPIC_API_KEY=$ANTHROPIC_KEY" >> "$INSTALL_DIR/.env"
    [ -n "$GEMINI_API_KEY" ] && echo "GEMINI_API_KEY=$GEMINI_KEY" >> "$INSTALL_DIR/.env"
    [ -n "$NVIDIA_API_KEY" ] && echo "NVIDIA_API_KEY=$NVIDIA_KEY" >> "$INSTALL_DIR/.env"
    [ -n "$OLLAMA_MODEL" ] && echo "OLLAMA_MODEL=$OLLAMA_MODEL" >> "$INSTALL_DIR/.env"

    echo "" >> "$INSTALL_DIR/.env"
    echo "# Git Token (for auto-push)" >> "$INSTALL_DIR/.env"
    echo "GIT_TOKEN=$GIT_TOKEN" >> "$INSTALL_DIR/.env"
}

# ═══════════════════════════════════════════════════════════════════
# Config Setup
# ═══════════════════════════════════════════════════════════════════

setup_config() {
    section "Bot Configuration"

    CONFIG_FILE="$INSTALL_DIR/user_data/config.json"

    if [ -f "$CONFIG_FILE" ]; then
        log "Config file exists at $CONFIG_FILE"

        if confirm "Use existing config?"; then
            log_success "Using existing config"
            return
        fi
    fi

    # Dry run or Live
    echo ""
    echo -e "${BOLD}Trading Mode${NC}"
    echo "1. Dry Run (Simulation) - Recommended for beginners"
    echo "2. Live Trading (Real money)"

    ask "Select [1]: "
    read -e mode_choice
    mode_choice="${mode_choice:-1}"

    if [ "$mode_choice" == "1" ]; then
        DRY_RUN=true
        INITIAL_WALLET=100
    else
        DRY_RUN=false
        ask "Initial wallet amount: "
        read -e INITIAL_WALLET
        INITIAL_WALLET="${INITIAL_WALLET:-1000}"
    fi

    # Trading mode
    echo ""
    echo -e "${BOLD}Trading Type${NC}"
    echo "1. Futures (with SHORT enabled)"
    echo "2. Spot (LONG only)"

    ask "Select [1]: "
    read -e trade_choice
    trade_choice="${trade_choice:-1}"

    if [ "$trade_choice" == "1" ]; then
        TRADING_MODE="futures"
        MARGIN_MODE="isolated"
    else
        TRADING_MODE="spot"
        MARGIN_MODE=""
    fi

    # Pairs
    echo ""
    ask "Trading pairs (comma separated) [BTC/USDT, ETH/USDT, BNB/USDT]: "
    read -e pairs_input
    PAIRS="${pairs_input:-BTC/USDT,ETH/USDT,BNB/USDT}"

    # Stake amount
    echo ""
    ask "Stake amount per trade [50]: "
    read -e stake_input
    STAKE_AMOUNT="${stake_input:-50}"

    # Telegram
    echo ""
    echo -e "${BOLD}Telegram Setup${NC}"
    ask "Telegram Bot Token: "
    read -e TELEGRAM_TOKEN

    ask "Telegram Chat ID: "
    read -e TELEGRAM_CHAT_ID

    # Create config
    create_config

    log_success "Configuration created"
}

create_config() {
    cat > "$CONFIG_FILE" << EOF
{
    "\$schema": "https://schema.freqtrade.io/schema.json",
    "max_open_trades": 2,
    "stake_currency": "USDT",
    "stake_amount": $STAKE_AMOUNT,
    "tradable_balance_ratio": 0.99,
    "fiat_display_currency": "USD",
    "dry_run": $DRY_RUN,
    "dry_run_wallet": $INITIAL_WALLET,
    "cancel_open_orders_on_exit": false,
    "trading_mode": "$TRADING_MODE",
    "margin_mode": "$MARGIN_MODE",
    "unfilledtimeout": {
        "entry": 10,
        "exit": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    },
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_to_ask_delta": 1
        }
    },
    "exit_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1
    },
    "exchange": {
        "name": "binance",
        "key": "",
        "secret": "",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": [$(echo "$PAIRS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/')],
        "pair_blacklist": []
    },
    "pairlists": [
        {
            "method": "StaticPairList",
            "refresh_period": 1800
        }
    ],
    "telegram": {
        "enabled": true,
        "token": "$TELEGRAM_TOKEN",
        "chat_id": "$TELEGRAM_CHAT_ID",
        "notification_settings": {
            "entry": true,
            "exit": true,
            "entry_cancel": true,
            "entry_fill": true,
            "exit_fill": true,
            "status": true,
            "warning": true,
            "startup": true,
            "strategy_msg": true,
            "show_config": true,
            "show_trades": true,
            "ask_orderfill": true,
            "ask_order_cancel": true
        },
        "allow_custom_messages": true
    },
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "enable_openapi": true,
        "jwt_secret_key": "$(openssl rand -hex 32)",
        "ws_token": "$(openssl rand -hex 32)",
        "CORS_origins": [],
        "username": "freqtrade",
        "password": "freqtrade123"
    },
    "bot_name": "QuantumEdgeBot",
    "initial_state": "running",
    "force_entry_enable": true,
    "internals": {
        "process_throttle_secs": 5
    },
    "ai_analyzer": {
        "provider": "openrouter",
        "openrouter": {
            "api_key": "$OPENROUTER_API_KEY",
            "model": "meta-llama/llama-3.2-3b-instruct:free"
        },
        "ollama": {
            "base_url": "http://localhost:11434",
            "model": "$OLLAMA_MODEL"
        },
        "opena": {
            "api_key": "$OPENAI_API_KEY",
            "model": "gpt-4o-mini"
        },
        "claude": {
            "api_key": "$ANTHROPIC_KEY",
            "model": "claude-3-haiku-20240307"
        },
        "gemini": {
            "api_key": "$GEMINI_KEY",
            "model": "gemini-2.0-flash"
        }
    },
    "auto_alert": {
        "enabled": true,
        "timeframes": ["15m", "1h", "4h"],
        "min_confidence": 60,
        "alert_cooldown_minutes": 15
    }
}
EOF
}

# ═══════════════════════════════════════════════════════════════════
# Download Data
# ═══════════════════════════════════════════════════════════════════

download_data() {
    section "Download Historical Data"

    if confirm "Download historical data (recommended)?"; then
        log "Downloading BTC, ETH, BNB data for 1h and 15m..."

        cd "$INSTALL_DIR"

        # Activate venv
        source .venv/bin/activate

        # Download data
        python3 -m freqtrade download-data \
            --config user_data/config.json \
            --pairs BTC/USDT ETH/USDT BNB/USDT \
            --timeframe 1h \
            --timerange 20180101- \
            --erase 2>/dev/null || true

        python3 -m freqtrade download-data \
            --config user_data/config.json \
            --pairs BTC/USDT ETH/USDT \
            --timeframe 15m \
            --timerange 20200101- \
            --erase 2>/dev/null || true

        log_success "Data download complete"
    fi
}

# ═══════════════════════════════════════════════════════════════════
# Download Strategies
# ═══════════════════════════════════════════════════════════════════

git_sync() {
    section "Git Sync"

    if [ -z "$GIT_TOKEN" ]; then
        ask "GitHub Token (for auto-push, press Enter to skip): "
        read -e GIT_TOKEN_INPUT
        GIT_TOKEN="${GIT_TOKEN_INPUT:-}"
    fi

    if [ -n "$GIT_TOKEN" ]; then
        cd "$INSTALL_DIR"

        git config user.email "bot@freqtrade.local"
        git config user.name "QuantumEdge Bot"

        git remote set-url origin "https://x-access-token:${GIT_TOKEN}@github.com/SecretArrow/freqtrade.git"

        if confirm "Pull latest from GitHub?"; then
            log "Pulling from GitHub..."
            git pull origin stable 2>/dev/null || git pull origin main 2>/dev/null || true
            log_success "Sync complete"
        fi
    fi
}

# ═══════════════════════════════════════════════════════════════════
# Start Bot
# ═══════════════════════════════════════════════════════════════════

start_bot() {
    section "Start Bot"

    echo "Ready to start!"
    echo ""
    echo "Options:"
    echo "  1. Start normally"
    echo "  2. Start with BotGuardian (auto-restart on crash)"
    echo "  3. Start with auto-alert analysis"
    echo "  4. Just test (dry run)"
    echo ""

    ask "Select [1]: "
    read -e start_choice
    start_choice="${start_choice:-1}"

    cd "$INSTALL_DIR"

    case $start_choice in
        1)
            log "Starting bot..."
            source .venv/bin/activate
            python3 -m freqtrade trade \
                --config user_data/config.json \
                --strategy QuantumEdge_Adaptive \
                2>&1 | tee -a user_data/logs/freqtrade.log &
            ;;
        2)
            log "Starting with BotGuardian..."
            source .venv/bin/activate
            python3 user_data/bot_guardian.py &
            ;;
        3)
            log "Starting with auto-alert..."
            source .venv/bin/activate
            # Start bot and alert system
            python3 -m freqtrade trade \
                --config user_data/config.json \
                --strategy QuantumEdge_Adaptive &

            sleep 5
            python3 user_data/auto_alert.py &
            ;;
        *)
            log "Test mode - starting in dry run..."
            source .venv/bin/activate
            python3 -m freqtrade trade \
                --config user_data/config.json \
                --strategy QuantumEdge_Adaptive \
                --dry-run-only
            ;;
    esac

    log_success "Bot starting..."
    log "Check logs: tail -f user_data/logs/freqtrade.log"
}

# ═══════════════════════════════════════════════════════════════════
# Show Help
# ═══════════════════════════════════════════════════════════════════

show_help() {
    echo ""
    echo -e "${BOLD}Usage:${NC}"
    echo "  ./install.sh              Interactive installation"
    echo "  ./install.sh --minimal   Minimal install (no prompts)"
    echo "  ./install.sh --update    Update existing installation"
    echo ""
    echo -e "${BOLD}Commands after install:${NC}"
    echo "  cd $INSTALL_DIR"
    echo "  source .venv/bin/activate"
    echo "  python3 -m freqtrade trade --config user_data/config.json"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

main() {
    show_banner

    case "${1:-}" in
        --minimal)
            log "Minimal installation mode"
            MINIMAL=true
            ;;
        --update)
            log "Update mode"
            UPDATE=true
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            ;;
    esac

    # System check
    check_system

    # Install dependencies
    install_dependencies

    # Setup repo
    setup_repository

    # Setup venv
    setup_venv

    # Setup AI providers
    setup_ai_providers

    # Setup config
    setup_config

    # Download data
    download_data

    # Git sync
    git_sync

    # Start
    if [ "${MINIMAL:-false}" != "true" ]; then
        if confirm "Start the bot now?"; then
            start_bot
        else
            echo ""
            echo -e "${GREEN}Installation complete!${NC}"
            echo ""
            echo -e "${BOLD}To start manually:${NC}"
            echo "  cd $INSTALL_DIR"
            echo "  source .venv/bin/activate"
            echo "  python3 -m freqtrade trade --config user_data/config.json"
            echo ""
        fi
    else
        log_success "Installation complete!"
    fi
}

main "$@"