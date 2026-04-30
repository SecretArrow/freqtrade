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

## 🧠 AI Multi-Provider Analysis

QuantumEdge supports multiple AI providers for analysis. The system automatically uses the first available provider in this order: OpenRouter (free models) → Ollama → OpenAI → Claude → Gemini.

### FREE Providers (Recommended):
| Provider | Free Models | Setup |
|----------|-------------|-------|
| **OpenRouter** | llama-3.2-3b, mistral-7b, etc | API key from openrouter.ai |
| **Ollama** | llama3.2, qwen, mistral (100% local) | Install from ollama.ai |
| **KiloCode** | Free tier | API key |
| **OpenCode** | Free tier | API key |

### PAID Providers:
| Provider | Model | Setup |
|----------|-------|-------|
| OpenAI | GPT-4, GPT-3.5 | API key |
| Claude | Claude-3 | API key |
| Gemini | Gemini-2.0 | API key |
| NVIDIA AI | Mixtral, Llama | API key |

### Quick Setup:
```bash
# Install
./install.sh

# Or manually set API keys
export OPENROUTER_API_KEY="sk-..."
export OPENAI_API_KEY="sk-..."
```

### AI Telegram Commands:
```
/ai_analyze BTC/USDT [timeframe]  - Full AI analysis
/ai_signal BTC/USDT               - Quick signal
/ai_status                        - Show provider status
/ai_set [provider]                - Switch provider
/ai_report                        - Market report
```

### Example Response:
```
🧠 AI ANALYSIS: BTC/USDT (1h)

Trend: 🟢 Bullish
Support: $49,200 | Resistance: $51,500

Signal: 🟢 BUY (75% confidence)
RSI oversold at 38, MACD bullish crossover

Risk: Medium
🤖 OpenRouter (llama-3.2-3b-instruct)
⏰ 14:30:00
```

---

## 📊 Auto Alert System

Automatically monitors pairs and sends alerts when signals are detected.

### Setup:
```bash
# Start with auto-alert
python3 user_data/auto_alert.py

# With custom settings
python3 user_data/auto_alert.py --timeframes 15m 1h 4h --confidence 70
```

### Alert Settings (in config.json):
```json
{
  "auto_alert": {
    "enabled": true,
    "timeframes": ["15m", "1h", "4h"],
    "min_confidence": 60,
    "alert_cooldown_minutes": 15
  }
}
```

### Alert Commands:
```
/alerts  - Show recent alerts
/health  - System health
```

---

## 🚀 Auto Install Script

Interactive installer with setup wizard:

```bash
# Run installer
./install.sh

# Minimal install (no prompts)
./install.sh --minimal

# Update existing
./install.sh --update
```

### Installer Features:
- System requirements check
- Virtual environment setup
- AI provider configuration
- Bot configuration wizard
- Historical data download
- Git sync

---

## Quick Start

```bash
# 1. Clone/Update
git clone https://github.com/SecretArrow/freqtrade.git
cd freqtrade

# 2. Install
./install.sh

# 3. Start
source .venv/bin/activate
python3 -m freqtrade trade --config user_data/config.json

# Or with protection
./start_quantum_edge.sh --guardian
```

---

## Feature Summary

| Feature | Status | Free? |
|---------|--------|-------|
| Multi-strategy | ✅ | ✅ |
| Futures trading | ✅ | ✅ |
| Telegram control | ✅ | ✅ |
| BotGuardian | ✅ | ✅ |
| Multi-Provider AI | ✅ | ✅ |
| Auto Alert | ✅ | ✅ |
| Health monitoring | ✅ | ✅ |
| FreqAI (ML) | ✅ | ✅ |

---

*Last updated: 2026-04-30*
