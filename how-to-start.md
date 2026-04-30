# QuantumEdge Bot - Full Control via Telegram

## Daftar Lengkap Command Telegram

### 🟢 Start/Stop/Restart
```
/start     - Start bot trading
/stop      - Stop bot (trades stay open)
/restart   - Restart bot
```

### 📊 Status & Info
```
/status          - Show bot status
/status full     - Detailed status + open trades
/balance         - Show wallet balance
/profit          - Profit summary
/profit extended - Detailed profit report
/trades          - Recent trades (5)
/trades 10       - Recent trades (10)
/settings        - All current settings
/whois           - Bot info
```

### 📋 Strategy Switching
```
/strategy         - List all strategies
/strategy FreqAIQuantumEdge    - Switch to FreqAI
/strategy QuantumEdge_Pro     - Switch to Pro
/strategy QuantumEdge_15m     - Switch to 15m scalping
/strategy QuantumEdge_Futures  - Switch to Futures
```

### ⚡ Mode Control
```
/mode            - Show current mode
/mode futures    - Switch to Futures (LONG+SHORT)
/mode spot       - Switch to Spot (LONG only)
/mode dry        - Dry Run mode (simulation)
/mode live       - Live trading (real money)
```

### 📉 Short Trading
```
/short           - Show short status
/short on        - Enable SHORT orders
/short off       - Disable SHORT orders
```

### 📊 Analysis
```
/analyze BTC/USDT     - Analyze specific pair
/signals              - All pair signals
/indicators BTC/USDT   - Show indicator values
```

### 🧠 FreqAI Control
```
/freqai           - FreqAI status
/freqai train     - Train ML model
/freqai status    - Detailed status
```

### 📝 Pair Management
```
/whitelist              - Show whitelist
/whitelist add SOL/USDT - Add pair
/whitelist remove SOL/USDT - Remove pair
/blacklist              - Show blacklist
```

### 🔧 Trading Control
```
/entry BTC/USDT      - Force entry
/entry BTC/USDT short - Force SHORT entry
/exit 1              - Exit trade ID 1
/exit all              - Exit all trades
```

### 💰 Stake Settings
```
/stake 100       - $100 per trade
/stake 50        - $50 per trade
/stake unlimited - Unlimited stake
```

---

## Quick Command Reference

| Command | Description |
|---------|-------------|
| /status | Bot status |
| /strategy | Switch strategy |
| /mode | Futures/Spot/Dry |
| /short | Enable/disable short |
| /analyze | Analyze pair |
| /signals | All signals |
| /profit | Profit summary |
| /freqai | FreqAI control |
| /help | Help menu |

---

## Strategy List

| Strategy | Timeframe | Description |
|----------|-----------|-------------|
| FreqAIQuantumEdge | 15m | ML-powered |
| QuantumEdge_Pro | 15m | Advanced indicators |
| QuantumEdge_15m | 15m | Scalping |
| QuantumEdge_Futures | 15m | Futures optimized |
| QuantumEdge_Adaptive | 1h | Long-term |

---

## Mode Explanation

| Mode | Description | Can Short? |
|------|-------------|------------|
| Spot | Buy only | No |
| Futures | Long + Short | Yes |

| Run Mode | Description |
|----------|-------------|
| Dry Run | Simulation, no real money |
| Live | Real money |

---

## Example Usage

### Start trading:
```
/strategy FreqAIQuantumEdge
/mode futures
/short on
/start
```

### Check before trading:
```
/status
/profit
/signals
/balance
```

---

## ⚠️ Important Notes

1. **Dry Run** = Simulation (safe)
2. **Live** = Real money (careful!)
3. **Short** = Only in Futures mode

---

## File Locations

```
/home/testnet-warden/freqtrade/
├── user_data/
│   ├── strategies/
│   │   ├── FreqAIQuantumEdge.py
│   │   ├── QuantumEdge_Pro.py
│   │   └── QuantumEdge_15m.py
│   └── config.json
└── how-to-start.md
```

---

**⚠️ WARNING: This is not financial advice. Always use dry run first!**

---

## 1. Dry Run Mode

---

## 1. Dry Run Mode

### Apa itu Dry Run?

**Dry Run = MODE SIMULASI** adalah cara aman untuk testing bot tanpa uang nyata.

### Konfigurasi di config.json:

```json
{
    "dry_run": true,
    "dry_run_wallet": 100,
    "trading_mode": "futures",
    "margin_mode": "isolated"
}
```

### Perbedaan Dry Run vs Live:

| Aspek | Dry Run ⚪️ | Live 🟢 |
|-------|------------|---------|
| Uang | Fake $100 (atau sesuai setting) | Uang nyata |
| Profit/Loss | Simulasi | Real |
| Risiko | Tidak ada | Ada |
| Fees | Ada (simulasi) | Real |
| Slippages | Tidak ada | Mungkin ada |

### Cara Toggle Dry Run:

1. Edit config.json:
```json
"dry_run": false,  // true = simulasi, false = real
```

2. Atau via Telegram (setelah direstart):
```
/toggle_dryrun
```

### Dry Run Wallet:

```json
"dry_run_wallet": 100  // Balance fake $100
```

---

## 2. Telegram Commands

### Command Dasar:

```
/start         - Start bot
/stop          - Stop bot
/status        - Show status
/balance       - Show balance
/profit        - Show profit
/trades        - Show recent trades
/whitelist     - Show pair whitelist
/blacklist     - Show pair blacklist
```

### Command Trading:

```
/entry BTC/USDT    - Force entry on pair
/exit 1            - Force exit trade ID 1
/cancel-open-orders - Cancel open orders
/force_entry_enable  - Enable force entry
/force_entry_disable - Disable force entry
```

### Command Analysis:

```
/analyze BTC/USDT   - Analyze specific pair
/signals           - Show all current signals
/indicators BTC/USDT - Show indicator values
```

### Custom Commands (QuantumEdge):

```
/analyze [pair]        - Analyze pair
/signals              - Show all signals
/train_freqai          - Train FreqAI model
/freqai_status         - Show FreqAI status
/toggle_futures        - Toggle futures/spot
/toggle_dryrun         - Toggle dry run/live
/set_short on/off      - Enable/disable short
/profit_summary        - Detailed profit report
/help_extended         - Show extended help
```

---

## 3. FreqAI Setup

FreqAI adalah machine learning module Freqtrade untuk prediction.

### Install:

```bash
pip install freqtrade[freqai]
```

### Konfigurasi FreqAI di config.json:

```json
"freqai": {
    "enabled": true,
    "purge_old_models": 5,
    "train_seconds": 3600,
    "live_retrain_hours": 24,
    "period_days": 30,
    "backtest_period_days": 15,
    "data_start_days": 60,
    "feature_parameters": {
        "include_timeframes": ["5m", "15m", "1h"],
        "include_corr_pairlist": true,
        "corr_pairlist": ["BTC/USDT", "ETH/USDT", "BNB/USDT"],
        "include_shifted_candles": true,
        "num_shifted_candles": 3,
        "num_candles": 20,
        "indicator_periods_candles": [10, 20, 30]
    },
    "model": {
        "type": "lightgbm",
        "feature_names": [
            "RSI", "EMA_9", "EMA_21", "MACD",
            "BB_position", "Volume_ratio", "ATR"
        ],
        "target": "predict",
        "activation": "relu",
        "epochs": 100,
        "batch_size": 256
    }
}
```

### Buat FreqAI Strategy:

```python
from freqtrade.strategy import IStrategy
from freqtrade.freqai.data_klitter import DataKline

class FreqAIQuantumEdge(IStrategy):
    freqai = FreqAI()

    def feature_engineering(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        # Add features for ML
        dataframe["RSI"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["EMA_9"] = ta.EMA(dataframe, timeperiod=9)
        # ... more features
        return dataframe

    def labels直播间(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        # Define what to predict
        dataframe["do_predict"] = (
            (dataframe["close"].pct_change() > 0.005).astype(int)
        )
        return dataframe
```

### Train FreqAI:

```bash
# Via command line
freqtrade freqai --config user_data/config.json train

# Via Telegram
/train_freqai
```

---

## 4. Multi-Provider Support (OpenRouter, Ollama, Custom)

### 4.1 OpenRouter (Claude, GPT, dll)

OpenRouter connects to various LLM providers.

#### Install:
```bash
pip install openrouter
```

#### Konfigurasi:
```bash
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

#### Usage dengan FreqAI:
```python
# In strategy or custom script
import openrouter

response = openrouter.ChatCompletion.create(
    model="anthropic/claude-3-sonnet",
    messages=[{
        "role": "user",
        "content": f"Analyze {pair}: RSI={rsi}, MACD={macd}"
    }],
    api_key=os.getenv("OPENROUTER_API_KEY")
)
```

### 4.2 Ollama (Local LLM)

Ollama runs LLMs locally on your machine.

#### Install Ollama:
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve
```

#### Pull Models:
```bash
ollama pull llama3
ollama pull mistral
ollama pull codellama
```

#### Usage:
```python
import ollama

response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': f"Analyze {pair} trading signal",
    },
])
```

### 4.3 Custom Provider

#### Implementasi Custom Provider:

```python
from freqtrade.freqai.RL.BaseReinforcementLearningModel import BaseReinforcementLearningModel

class CustomLLMProvider:
    def __init__(self, config: dict):
        self.provider = config.get("provider", "ollama")
        self.model = config.get("model", "llama3")
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "http://localhost:11434")

    def predict(self, prompt: str) -> str:
        if self.provider == "ollama":
            return self._ollama_predict(prompt)
        elif self.provider == "openrouter":
            return self._openrouter_predict(prompt)
        else:
            return self._custom_predict(prompt)

    def _ollama_predict(self, prompt: str) -> str:
        import ollama
        response = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"]

    def _openrouter_predict(self, prompt: str) -> str:
        import openrouter
        response = openrouter.ChatCompletion.create(
            model="anthropic/claude-3-sonnet",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### 4.4 Complete Setup dengan Multi-Provider

```python
# user_data/llm_integration.py

class LLMTradingAssistant:
    """
    LLM Integration untuk Trading Analysis
    Supports: OpenRouter, Ollama, Custom API
    """
    def __init__(self, config: dict):
        self.provider = config.get("llm_provider", "ollama")
        self.model = config.get("llm_model", "llama3")
        self._init_provider()

    def _init_provider(self):
        if self.provider == "ollama":
            self._init_ollama()
        elif self.provider == "openrouter":
            self._init_openrouter()

    def analyze_market(self, pair: str, indicators: dict) -> dict:
        """Analyze market using LLM"""
        prompt = self._build_analysis_prompt(pair, indicators)

        if self.provider == "ollama":
            response = self._ollama_chat(prompt)
        elif self.provider == "openrouter":
            response = self._openrouter_chat(prompt)

        return self._parse_response(response)

    def _build_analysis_prompt(self, pair: str, indicators: dict) -> str:
        return f"""Analyze {pair} trading opportunity:

RSI: {indicators.get('rsi', 'N/A')}
MACD: {indicators.get('macd', 'N/A')}
EMA Cross: {'Bullish' if indicators.get('ema_cross', False) else 'Bearish'}
BB Position: {indicators.get('bb_position', 'N/A')}
Volume: {indicators.get('volume_ratio', 'N/A')}

Provide:
1. Signal (BUY/SELL/HOLD)
2. Confidence (0-100%)
3. Reasoning
"""

    def _parse_response(self, response: str) -> dict:
        """Parse LLM response"""
        signal = "HOLD"
        confidence = 50

        if "BUY" in response.upper():
            signal = "BUY"
        elif "SELL" in response.upper():
            signal = "SELL"

        # Extract confidence
        import re
        match = re.search(r'(\d+)%', response)
        if match:
            confidence = int(match.group(1))

        return {"signal": signal, "confidence": confidence, "reasoning": response}
```

---

## 5. Custom Telegram Commands

### File: user_data/custom_telegram.py

Commands yang tersedia:

| Command | Deskripsi |
|---------|-----------|
| `/train_freqai` | Train FreqAI model |
| `/toggle_futures` | Toggle futures/spot |
| `/toggle_dryrun` | Toggle dry run/live |
| `/analyze [pair]` | Analyze specific pair |
| `/signals` | Show all signals |
| `/freqai_status` | Show FreqAI status |
| `/set_short on/off` | Enable/disable short |
| `/profit_summary` | Detailed profit report |
| `/help_extended` | Extended help |

### Enable Custom Commands:

Tambahkan di config.json:

```json
"telegram": {
    "enabled": true,
    "token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
}
```

### Activate Custom Plugin:

```python
# Buat file user_data/plugins.py
from freqtrade.plugins import Plugin

class CustomPlugin(Plugin):
    def __init__(self, config: dict):
        self.telegram = CustomTelegramCommands(config)

    def on_start(self):
        self.telegram.register()
```

---

## 6. Quick Reference

### Start Bot:

```bash
# Activate environment
cd /home/testnet-warden/freqtrade
source .venv/bin/activate

# Start dengan dry run
freqtrade trade --config user_data/config.json --strategy FreqAIQuantumEdge --dry-run

# Start live
freqtrade trade --config user_data/config.json --strategy FreqAIQuantumEdge
```

### Train FreqAI:

```bash
freqtrade freqai --config user_data/config.json train
```

### Backtest:

```bash
freqtrade backtesting --config user_data/config.json --strategy FreqAIQuantumEdge --timerange 20220101-20260430 -i 15m
```

### Hyperopt:

```bash
freqtrade hyperopt --config user_data/config.json --strategy FreqAIQuantumEdge --epochs 500 --timerange 20220101-20260430
```

### Telegram Bot Token:

Dapatkan dari @BotFather di Telegram.

### File Structure:

```
/home/testnet-warden/freqtrade/
├── user_data/
│   ├── strategies/
│   │   ├── FreqAIQuantumEdge.py      # ML strategy
│   │   ├── QuantumEdge_Pro.py         # Pro strategy
│   │   ├── QuantumEdge_15m.py         # 15m scalping
│   │   └── QuantumEdge_Futures.py     # Futures strategy
│   ├── config.json                    # Main config
│   ├── custom_telegram.py            # Custom commands
│   ├── llm_integration.py             # LLM provider integration
│   └── data/
│       └── binance/                  # Data historis
├── how-to-start.md                   # Dokumentasi
└── requirements.txt
```

---

## Warning

⚠️ **INI BUKAN SARAN FINANCIAL**

- Selalu test dengan dry run dulu
- Modal trading adalah uang yang kamu siap kehilangan
- Backtest results tidak menjamin profit di masa depan
- Pasar kripto sangat volatil

---

## Support

- Freqtrade Docs: https://www.freqtrade.io/en/stable/
- FreqAI Docs: https://www.freqtrade.io/en/stable/freqai/
- OpenBB: https://docs.openbb.co/
- Jesse: https://jesse-ai.com/docs
- Ollama: https://ollama.ai/

---

## 🤖 BotGuardian - Anti-Crash System

BotGuardian adalah sistem monitoring yang memastikan bot tidak pernah crash dan auto-restart jika terjadi error.

### Fitur:
- ✅ Auto restart on crash
- ✅ Memory leak detection
- ✅ CPU overheating protection
- ✅ Disk space monitoring
- ✅ Auto backup sebelum restart
- ✅ Auto Git sync

### Start dengan Guardian:
```bash
./start_quantum_edge.sh --guardian
# atau
python3 user_data/bot_guardian.py
```

### Monitoring:
```bash
# Lihat logs
tail -f user_data/logs/freqtrade.log

# Check system health
python3 -c "from user_data.system_monitor import SystemMonitor; print(SystemMonitor().format_health_report())"
```

### Health Check Thresholds:
| Metric | Threshold | Action |
|--------|-----------|--------|
| Memory | >85% | Alert |
| CPU | >95% | Alert |
| Disk | >85% | Alert |
| Disk Free | <2GB | Emergency backup |

---

## 🧠 AI Analysis (Ollama - FREE)

AI analysis menggunakan Ollama - 100% gratis, runs local, no API keys needed.

### Install Ollama:
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download dari https://ollama.ai
```

### Install Model:
```bash
ollama pull llama3.2
# atau model lain yang tersedia:
ollama pull qwen3.5:2b
ollama pull mistral
```

### Set Environment:
```bash
export OLLAMA_MODEL=llama3.2
```

### Telegram AI Commands:
```
/ai_analyze BTC/USDT  - AI analysis of pair
/ai_signal BTC/USDT   - AI trading signal
/ai_report           - Daily market report
/ai_learn RSI         - Learn about indicator
```

### Example Response:
```
🧠 AI ANALYSIS: BTC/USDT

Trend: 🟢 Bullish (EMA crossover)
Support: $49,200
Resistance: $51,500

Recommendation: 🟢 BUY
- RSI oversold at 38
- MACD bullish crossover
- Volume increasing

Risk: Medium
Timeframe: 1H for entry

🤖 Model: llama3.2
⏰ 14:30:00
```

---

## 📊 System Health Monitoring

Monitor sistem via Telegram untuk ensure bot runs smooth.

### Telegram Commands:
```
/health        - System health status
/performance   - Trading performance
/alerts        - Recent system alerts
```

### Health Report Example:
```
🔧 SYSTEM HEALTH

⏱️ Uptime: 2h 15m
🧠 Memory: 🟢██░░░░░░░░ 26.0%
💻 CPU: 🟢░░░░░░░░░░ 4.8%
💾 Disk: 🟢███░░░░░░░ 31.4%

📊 PROCESS INFO
Memory: 17.4 MB
Threads: 3

🖥️ SYSTEM
CPU Cores: 12
Total RAM: 31.3 GB
Free Disk: 662.5 GB
```

---

## 💾 Git Auto-Sync

Auto backup konfigurasi dan strategies ke GitHub.

### Setup Git Token:
```bash
export GIT_TOKEN="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"
```

### Telegram Commands:
```
/backup   - Push semua perubahan ke GitHub
/sync     - Pull terbaru dari GitHub
```

### Auto-Backup:
BotGuardian auto backup setiap:
- Sebelum restart
- Setiap 6 jam
- Jika disk space low

### Git Repo:
https://github.com/SecretArrow/freqtrade

---

## 🚀 New Telegram Commands

### Quick Commands:
```
/quick_profit   - Quick profit summary
/health         - System health
/performance    - Trading stats
/alerts         - System alerts
```

### AI Commands:
```
/ai_analyze [pair]   - Analyze with AI
/ai_signal [pair]    - Get AI signal
/ai_report          - Daily report
/ai_learn [ind]     - Learn indicator
```

### Git Commands:
```
/backup    - Backup to GitHub
/sync      - Sync from GitHub
```

### Guardian:
```
/restart_guardian   - Restart dengan protection
```

### Enhanced Commands:
```
/setshort on/off    - Alternative short toggle
/profit             - Full profit report
/quick_profit       - Quick summary
/health             - System + bot health
```

---

## 📁 File Structure (Updated)

```
/home/testnet-warden/freqtrade/
├── user_data/
│   ├── strategies/
│   │   ├── FreqAIQuantumEdge.py      # ML strategy
│   │   ├── QuantumEdge_Pro.py         # Pro strategy
│   │   ├── QuantumEdge_15m.py         # 15m scalping
│   │   ├── QuantumEdge_Futures.py     # Futures strategy
│   │   └── QuantumEdge_Adaptive.py    # 1h trend following
│   ├── config.json                    # Main config
│   ├── bot_guardian.py               # Anti-crash system
│   ├── ollama_analyzer.py            # Free AI analysis
│   ├── system_monitor.py             # Health monitoring
│   ├── telegram_control.py           # Full Telegram control
│   └── data/
│       └── binance/                  # Historical data
├── start_quantum_edge.sh            # Startup script
├── how-to-start.md                   # Dokumentasi
└── requirements.txt
```

---

## 🎯 Quick Start Guide

### 1. First Time Setup:
```bash
# Install dependencies
pip install psutil requests -q

# Setup git
git config user.email "bot@freqtrade.local"
git config user.name "QuantumEdge Bot"

# Test run
./start_quantum_edge.sh --dry-run
```

### 2. Daily Usage:
```bash
# Start with protection (recommended)
./start_quantum_edge.sh --guardian --dry-run

# Or regular start
./start_quantum_edge.sh --dry-run

# Check logs
tail -f user_data/logs/freqtrade.log
```

### 3. Telegram Commands:
```
/start              - Start bot
/health             - Check system
/ai_analyze BTC/USDT - AI analysis
/backup             - Backup to GitHub
```

### 4. Emergency:
```
/stop              - Stop bot
/restart          - Restart bot
/restart_guardian  - Restart with guardian
```

---

## 🔧 Troubleshooting

### Bot tidak mau start:
```bash
# Check config
cat user_data/config.json | python3 -m json.tool

# Check logs
tail -50 user_data/logs/freqtrade.log
```

### Ollama not available:
```bash
# Check Ollama running
curl http://localhost:11434/api/tags

# Install model
ollama pull llama3.2

# Set model
export OLLAMA_MODEL=llama3.2
```

### Git push failed:
```bash
# Set token
export GIT_TOKEN="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"

# Manual push
cd /home/testnet-warden/freqtrade
git add -A
git commit -m "backup"
git push origin main
```

### Memory high:
```bash
# Check memory
free -h

# Restart if needed
./start_quantum_edge.sh --guardian
```

---

## ⚠️ Important Notes

1. **Always use --guardian for production** - ensures auto-restart
2. **Test with --dry-run first** - sebelum live trading
3. **Regular backups** - Gunakan /backup command
4. **Monitor health** - Check /health secara berkala
5. **Install Ollama** - Untuk AI features (optional tapi recommended)

---

## 🎉 Feature Summary

| Feature | Status | Free? |
|---------|--------|-------|
| Multi-strategy | ✅ | ✅ |
| Futures trading | ✅ | ✅ |
| Telegram control | ✅ | ✅ |
| BotGuardian | ✅ | ✅ |
| AI Analysis (Ollama) | ✅ | ✅ |
| Health monitoring | ✅ | ✅ |
| Auto Git backup | ✅ | ✅ |
| FreqAI (ML) | ✅ | ✅ |
| Multi-timeframe | ✅ | ✅ |

---

*Last updated: 2026-04-30*
