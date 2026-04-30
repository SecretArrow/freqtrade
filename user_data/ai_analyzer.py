"""
QuantumEdge AI Analyzer - Multi-Provider Support
Supports: OpenRouter, OpenAI, Claude (Anthropic), KiloCode, NVIDIA AI, Gemini, Ollama, Custom

Free Providers (with free tiers):
- OpenRouter (free models like llama-3.2, mixtral)
- KiloCode (free tier)
- Ollama (100% free, local)
- OpenCode (free tier)

Paid Providers:
- OpenAI (GPT-4, GPT-3.5)
- Claude (Anthropic)
- NVIDIA AI
- Gemini (Google)

Configuration via environment or config.json
"""

import os
import json
import logging
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger("AIAnalyzer")


class Provider(Enum):
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    CLAUDE = "claude"
    KILOCODE = "kilocode"
    NVIDIA = "nvidia"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    OPENCODE = "opencode"
    CUSTOM = "custom"


class BaseAIProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = False

    @abstractmethod
    def analyze(self, prompt: str) -> Optional[str]:
        """Generate analysis from AI"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get provider name"""
        pass

    def format_error(self, error: str) -> str:
        return f"❌ {self.get_name()} Error: {error}"


class OpenRouterProvider(BaseAIProvider):
    """OpenRouter - supports many free models"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = config.get("model", "meta-llama/llama-3.2-3b-instruct:free")
        self.site_url = config.get("site_url", "https://github.com/SecretArrow/freqtrade")
        self.site_name = config.get("site_name", "QuantumEdge Bot")

        # Free models available on OpenRouter
        self.free_models = [
            "meta-llama/llama-3.2-3b-instruct:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free",
            "openchat/openchat-7b:free",
            "undi95/toppy-m-7b:free",
            "sophosympatheia/rogue-7b:free",
            "agentica-agent/openorca-platypus-7b:free",
        ]

        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"OpenRouter ({self.model.split('/')[-1]})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.site_url,
                "X-Title": self.site_name,
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter error: {response.status_code} - {response.text}")
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            logger.error(f"OpenRouter exception: {e}")
            return self.format_error(str(e))


class KiloCodeProvider(BaseAIProvider):
    """KiloCode - free tier available"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("KILOCODE_API_KEY", "")
        self.base_url = "https://api.kilocode.io/v1"
        self.model = config.get("model", "kilocode-llama-3.2-3b")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"KiloCode ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class OpenCodeProvider(BaseAIProvider):
    """OpenCode - free tier"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("OPENCODE_API_KEY", "")
        self.base_url = "https://api.opencode.ai/v1"
        self.model = config.get("model", "opencode-3b")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"OpenCode ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class OpenAIProvider(BaseAIProvider):
    """OpenAI - GPT-4, GPT-3.5"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1"
        self.model = config.get("model", "gpt-4o-mini")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"OpenAI ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class ClaudeProvider(BaseAIProvider):
    """Claude - Anthropic"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY", "")
        self.base_url = "https://api.anthropic.com/v1"
        self.model = config.get("model", "claude-3-haiku-20240307")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"Claude ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
                "temperature": 0.7,
            }

            response = requests.post(
                f"{self.base_url}/messages", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                return data["content"][0]["text"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class NVIDIAProvider(BaseAIProvider):
    """NVIDIA AI - free tier available"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("NVIDIA_API_KEY", "")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = config.get("model", "mistralai/mixtral-8x7b-instruct-v0.1")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"NVIDIA AI ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class GeminiProvider(BaseAIProvider):
    """Google Gemini"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("GEMINI_API_KEY", "")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = config.get("model", "gemini-2.0-flash")
        self.enabled = bool(self.api_key)

    def get_name(self) -> str:
        return f"Gemini ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024,
                },
            }

            response = requests.post(url, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class OllamaProvider(BaseAIProvider):
    """Ollama - 100% free, local"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", os.environ.get("OLLAMA_MODEL", "llama3.2"))
        self.enabled = self._check_connection()

    def get_name(self) -> str:
        return f"Ollama ({self.model})"

    def _check_connection(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [m["name"] for m in response.json().get("models", [])]
                if self.model in models or any(self.model in m for m in models):
                    logger.info(f"Ollama connected with model {self.model}")
                    return True
                else:
                    logger.warning(f"Ollama model {self.model} not found. Available: {models}")
                    return False
        except:
            return False
        return False

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1024,
                },
            }

            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class CustomProvider(BaseAIProvider):
    """Custom/Others compatible with OpenAI API format"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.environ.get("CUSTOM_API_KEY", "")
        self.base_url = config.get("base_url", "https://api.example.com/v1")
        self.model = config.get("model", "custom-model")
        self.enabled = bool(self.api_key) and bool(self.base_url)

    def get_name(self) -> str:
        return f"Custom ({self.model})"

    def analyze(self, prompt: str) -> Optional[str]:
        if not self.enabled:
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.format_error(f"Status {response.status_code}")

        except Exception as e:
            return self.format_error(str(e))


class MultiProviderAnalyzer:
    """
    Multi-provider AI Analyzer
    Supports all major AI providers
    """

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.providers: Dict[str, BaseAIProvider] = {}
        self.current_provider_name = self.config.get("provider", "openrouter")
        self._init_providers()

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load config from file or environment"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

        try:
            with open(config_path, "r") as f:
                full_config = json.load(f)
                return full_config.get("ai_analyzer", {})
        except:
            return {}

    def _init_providers(self):
        """Initialize all providers"""
        self.providers = {
            "openrouter": OpenRouterProvider(self.config.get("openrouter", {})),
            "opena": OpenAIProvider(self.config.get("opena", {})),
            "claude": ClaudeProvider(self.config.get("claude", {})),
            "kilocode": KiloCodeProvider(self.config.get("kilocode", {})),
            "nvidia": NVIDIAProvider(self.config.get("nvidia", {})),
            "gemini": GeminiProvider(self.config.get("gemini", {})),
            "ollama": OllamaProvider(self.config.get("ollama", {})),
            "opencode": OpenCodeProvider(self.config.get("opencode", {})),
            "custom": CustomProvider(self.config.get("custom", {})),
        }

    def get_provider(self, name: str = None) -> Optional[BaseAIProvider]:
        """Get provider by name or current"""
        if name is None:
            name = self.current_provider_name
        return self.providers.get(name)

    def get_enabled_providers(self) -> Dict[str, bool]:
        """Get all providers with their status"""
        return {name: p.enabled for name, p in self.providers.items()}

    def set_provider(self, name: str) -> bool:
        """Set current provider"""
        if name in self.providers:
            if self.providers[name].enabled:
                self.current_provider_name = name
                return True
            else:
                logger.warning(f"Provider {name} is not enabled")
                return False
        return False

    def analyze(self, prompt: str, provider: str = None) -> Optional[str]:
        """Analyze with specified or current provider"""
        p = self.get_provider(provider)
        if p:
            return p.analyze(prompt)
        return None

    def analyze_pair(self, pair: str, data: Dict[str, Any], timeframe: str = "1h") -> str:
        """Analyze a trading pair"""
        provider = self.get_provider()
        if not provider:
            return "❌ No AI provider enabled"

        prompt = f"""Analyze {pair} on {timeframe} timeframe for trading.

Current Data:
- Price: {data.get("price", "N/A")}
- RSI (14): {data.get("rsi", "N/A")}
- MACD: {data.get("macd", "N/A")}
- MACD Signal: {data.get("macdsignal", "N/A")}
- EMA 9: {data.get("ema_9", "N/A")}
- EMA 21: {data.get("ema_21", "N/A")}
- EMA 50: {data.get("ema_50", "N/A")}
- EMA 200: {data.get("ema_200", "N/A")}
- Bollinger Position: {data.get("bb_position", "N/A")}
- Volume Ratio: {data.get("volume_ratio", "N/A")}
- ATR: {data.get("atr", "N/A")}
- ADX: {data.get("adx", "N/A")}

Provide in <200 words:
1. Trend (bullish/bearish/neutral)
2. Key support/resistance
3. Entry signal (buy/sell/hold) with confidence %
4. Risk level (low/medium/high)
5. Best timeframe for entry

Be concise and actionable."""

        result = provider.analyze(prompt)
        if result:
            return (
                f"🧠 *AI ANALYSIS: {pair}* ({timeframe})\n\n"
                f"{result}\n\n"
                f"🤖 Provider: {provider.get_name()}\n"
                f"⏰ {datetime.now().strftime('%H:%M:%S')}"
            )
        return f"❌ Analysis failed. Provider: {provider.get_name()}"

    def get_signal(self, pair: str, data: Dict[str, Any]) -> str:
        """Get quick trading signal"""
        provider = self.get_provider()
        if not provider:
            return "❌ No provider"

        prompt = f"""Give a SINGLE trading signal for {pair}:

RSI: {data.get("rsi", 50)}
MACD: {"+" if data.get("macd", 0) > 0 else ""}{data.get("macd", 0):.4f}
EMA Trend: {"↑" if data.get("ema_9", 0) > data.get("ema_21", 0) else "↓"}
BB Position: {data.get("bb_position", 0.5):.2f} (0=oversold, 1=overbought)
Volume: {"High" if data.get("volume_ratio", 1) > 1.5 else "Normal"}

Respond ONLY with:
🟢 BUY - [reason]
🔴 SELL - [reason]
⚪️ HOLD - [reason]"""

        result = provider.analyze(prompt)
        if result:
            return f"📊 *SIGNAL: {pair}*\n\n{result}\n\n🤖 {provider.get_name()}"
        return "❌ Signal failed"


class AutoAlertAnalyzer:
    """
    Auto alert analyzer - analyzes pairs per timeframe
    Sends alerts when signals detected
    """

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.analyzer = MultiProviderAnalyzer(config_path)
        self.alert_cooldown = self.config.get("alert_cooldown_minutes", 15)
        self.last_alerts: Dict[str, datetime] = {}
        self.enabled_timeframes = self.config.get("timeframes", ["15m", "1h", "4h"])
        self.min_confidence = self.config.get("min_confidence", 60)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        try:
            with open(config_path, "r") as f:
                full_config = json.load(f)
                return full_config.get("auto_alert", {})
        except:
            return {}

    def can_alert(self, key: str) -> bool:
        """Check if alert is not in cooldown"""
        if key not in self.last_alerts:
            return True

        elapsed = (datetime.now() - self.last_alerts[key]).total_seconds() / 60
        return elapsed >= self.alert_cooldown

    def record_alert(self, key: str):
        """Record alert timestamp"""
        self.last_alerts[key] = datetime.now()

    def analyze_all_timeframes(self, pair: str, data_by_tf: Dict[str, Dict]) -> List[Dict]:
        """Analyze pair across all timeframes"""
        signals = []

        for tf in self.enabled_timeframes:
            if tf not in data_by_tf:
                continue

            data = data_by_tf[tf]
            key = f"{pair}_{tf}"

            # Quick signal check
            rsi = data.get("rsi", 50)
            ema_9 = data.get("ema_9", 0)
            ema_21 = data.get("ema_21", 0)

            # Simple signal from indicators
            if ema_9 > ema_21 and rsi < 40:
                signal = "BUY"
                confidence = min(100, (50 - rsi) * 2 + 30)
            elif ema_9 < ema_21 and rsi > 60:
                signal = "SELL"
                confidence = min(100, (rsi - 50) * 2 + 30)
            else:
                signal = "HOLD"
                confidence = 50

            if confidence >= self.min_confidence and self.can_alert(key):
                self.record_alert(key)
                signals.append(
                    {
                        "pair": pair,
                        "timeframe": tf,
                        "signal": signal,
                        "confidence": confidence,
                        "rsi": rsi,
                        "price": data.get("close", 0),
                        "provider": self.analyzer.current_provider_name,
                    }
                )

        return signals

    def format_alert(self, signal: Dict) -> str:
        """Format alert message"""
        emoji = "🟢" if signal["signal"] == "BUY" else "🔴" if signal["signal"] == "SELL" else "⚪️"

        return (
            f"{emoji} *{signal['signal']} SIGNAL*\n\n"
            f"Pair: {signal['pair']}\n"
            f"Timeframe: {signal['timeframe']}\n"
            f"Confidence: {signal['confidence']}%\n"
            f"RSI: {signal['rsi']:.1f}\n"
            f"Price: {signal['price']:.6f}\n"
            f"Provider: {signal['provider']}\n"
            f"⏰ {datetime.now().strftime('%H:%M:%S')}"
        )


# Singleton
_analyzer: Optional[MultiProviderAnalyzer] = None
_auto_alert: Optional[AutoAlertAnalyzer] = None


def get_analyzer() -> MultiProviderAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = MultiProviderAnalyzer()
    return _analyzer


def get_auto_alert() -> AutoAlertAnalyzer:
    global _auto_alert
    if _auto_alert is None:
        _auto_alert = AutoAlertAnalyzer()
    return _auto_alert


def is_ai_available() -> bool:
    """Check if any AI provider is available"""
    return get_analyzer().get_provider() is not None


# Quick status
def get_status() -> Dict[str, Any]:
    """Get AI status"""
    analyzer = get_analyzer()
    enabled = analyzer.get_enabled_providers()
    current = analyzer.current_provider_name
    current_provider = analyzer.get_provider()

    return {
        "current_provider": current,
        "current_enabled": current_provider.enabled if current_provider else False,
        "provider_name": current_provider.get_name() if current_provider else "None",
        "all_providers": enabled,
    }


# Telegram handlers
async def cmd_ai_analyze(freqtrade, args: List[str], send_msg) -> None:
    """Handle /ai_analyze"""
    if not args:
        await send_msg("Usage: /ai_analyze BTC/USDT [timeframe]\nExample: /ai_analyze BTC/USDT 1h")
        return

    pair = args[0]
    timeframe = args[1] if len(args) > 1 else freqtrade.timeframe

    try:
        dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, timeframe)
        if dataframe.empty:
            await send_msg(f"❌ No data for {pair}")
            return

        last = dataframe.iloc[-1]
        data = {
            "price": last.get("close", 0),
            "rsi": last.get("rsi", 50),
            "macd": last.get("macd", 0),
            "macdsignal": last.get("macdsignal", 0),
            "ema_9": last.get("ema_9", 0),
            "ema_21": last.get("ema_21", 0),
            "ema_50": last.get("ema_50", 0),
            "ema_200": last.get("ema_200", 0),
            "bb_position": last.get("bb_position", 0.5),
            "volume_ratio": last.get("volume_ratio", 1),
            "atr": last.get("atr", 0),
            "adx": last.get("adx", 0),
        }

        result = get_analyzer().analyze_pair(pair, data, timeframe)
        await send_msg(result)

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


async def cmd_ai_signal(freqtrade, args: List[str], send_msg) -> None:
    """Handle /ai_signal"""
    if not args:
        await send_msg("Usage: /ai_signal BTC/USDT")
        return

    pair = args[0]

    try:
        dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, freqtrade.timeframe)
        if dataframe.empty:
            await send_msg(f"❌ No data for {pair}")
            return

        last = dataframe.iloc[-1]
        data = {
            "rsi": last.get("rsi", 50),
            "macd": last.get("macd", 0),
            "ema_9": last.get("ema_9", 0),
            "ema_21": last.get("ema_21", 0),
            "bb_position": last.get("bb_position", 0.5),
            "volume_ratio": last.get("volume_ratio", 1),
        }

        result = get_analyzer().get_signal(pair, data)
        await send_msg(result)

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


async def cmd_ai_status(send_msg) -> None:
    """Handle /ai_status"""
    status = get_status()

    providers_text = "\n".join(
        [
            f"{'✅' if enabled else '❌'} {name}: {name.upper()}"
            for name, enabled in status["all_providers"].items()
        ]
    )

    text = (
        f"🧠 *AI PROVIDER STATUS*\n\n"
        f"Current: {status['provider_name']}\n"
        f"Enabled: {'Yes ✅' if status['current_enabled'] else 'No ❌'}\n\n"
        f"Available Providers:\n{providers_text}\n\n"
        f"Commands:\n"
        f"/ai_set openrouter - Use OpenRouter\n"
        f"/ai_set claude - Use Claude\n"
        f"/ai_set gemini - Use Gemini\n"
        f"/ai_set ollama - Use Ollama (local)"
    )

    await send_msg(text)


async def cmd_ai_set(args: List[str], send_msg) -> None:
    """Handle /ai_set [provider]"""
    if not args:
        await send_msg(
            "Usage: /ai_set [provider]\nProviders: openrouter, claude, gemini, ollama, openai"
        )
        return

    provider = args[0].lower()
    analyzer = get_analyzer()

    if analyzer.set_provider(provider):
        await send_msg(f"✅ Provider set to: {provider.upper()}")
    else:
        enabled = analyzer.get_enabled_providers()
        await send_msg(
            f"❌ Provider {provider} not available/enabled\n\n"
            f"Enabled providers: {[k for k, v in enabled.items() if v]}"
        )


async def cmd_ai_report(freqtrade, send_msg) -> None:
    """Handle /ai_report - Market report"""
    analyzer = get_analyzer()

    try:
        pairs = freqtrade.config.get("exchange", {}).get("pair_whitelist", [])
        pairs_text = ""

        for pair in pairs[:5]:
            try:
                dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, freqtrade.timeframe)
                if not dataframe.empty:
                    last = dataframe.iloc[-1]
                    rsi = last.get("rsi", 50)
                    macd = last.get("macd", 0)
                    ema_9 = last.get("ema_9", 0)
                    ema_21 = last.get("ema_21", 0)

                    trend = "↑" if ema_9 > ema_21 else "↓"
                    pairs_text += f"- {pair}: RSI={rsi:.0f}, MACD={'+' if macd > 0 else ''}{macd:.2f}, {trend}\n"
            except:
                pass

        prompt = f"""Generate a brief crypto market report.

Pairs:
{pairs_text}

Current: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Include:
1. Overall sentiment (bullish/bearish/neutral)
2. Best pair to trade
3. Risk assessment
4. Suggested strategy for next 24h

Keep under 200 words."""

        result = analyzer.analyze(prompt)
        if result:
            await send_msg(
                f"📈 *MARKET REPORT*\n\n{result}\n\n"
                f"🤖 {analyzer.get_provider().get_name()}\n"
                f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        else:
            await send_msg("❌ Report generation failed")

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    # Test
    analyzer = MultiProviderAnalyzer()
    status = get_status()

    print("AI Analyzer Status:")
    print(f"Current provider: {status['current_provider']}")
    print(f"Provider name: {status['provider_name']}")
    print(f"Enabled: {status['current_enabled']}")
    print("\nAll providers:")
    for name, enabled in status["all_providers"].items():
        print(f"  {'✅' if enabled else '❌'} {name}")
