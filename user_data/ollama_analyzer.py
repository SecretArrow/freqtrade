"""
QuantumEdge Ollama AI Analyzer - FREE Local LLM Integration
Uses Ollama (100% free, no API keys needed)

Install Ollama: https://ollama.ai
Models to install: llama3.2, mistral, or any preferred model

Commands:
- /ai_analyze [pair] - Get AI analysis
- /ai_signal - Get AI trading signal
- /ai_report - Daily market report
- /ai_news - Market news summary
"""

import requests
import json
import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger("OllamaAI")


class OllamaAnalyzer:
    """
    Free AI analyzer using Ollama local LLM
    No API costs, fully private, runs locally
    """

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = os.environ.get("OLLAMA_MODEL", "llama3.2")
        self.timeout = 60  # seconds

        # Check if Ollama is available
        self.available = self.check_connection()

    def check_connection(self) -> bool:
        """Check if Ollama is running with our model"""
        try:
            # First check if server is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                logger.info(f"Ollama connected. Available models: {model_names}")

                # Check if our model is available
                if self.model in model_names:
                    logger.info(f"Model {self.model} is available")
                    return True
                else:
                    logger.warning(f"Model {self.model} not found. Available: {model_names}")
                    logger.warning(f"Install with: ollama pull {self.model}")
                    return False
        except requests.exceptions.ConnectionError:
            logger.warning("Ollama not connected. Install from https://ollama.ai")
        except Exception as e:
            logger.error(f"Ollama connection error: {e}")
        return False

    def generate(self, prompt: str, system: str = None) -> Optional[str]:
        """Generate response from Ollama"""
        if not self.available:
            return None

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "top_p": 0.9, "num_predict": 512},
            }

            if system:
                payload["system"] = system

            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(f"Ollama error: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
        except Exception as e:
            logger.error(f"Ollama generate error: {e}")

        return None

    def analyze_pair(self, pair: str, data: Dict[str, Any]) -> str:
        """Analyze a trading pair with AI"""
        if not self.available:
            return "❌ Ollama not available. Install from https://ollama.ai"

        prompt = f"""Analyze {pair} trading pair.

Current Data:
- Price: {data.get("price", "N/A")}
- RSI (14): {data.get("rsi", "N/A")}
- MACD: {data.get("macd", "N/A")}
- EMA 9: {data.get("ema_9", "N/A")}
- EMA 21: {data.get("ema_21", "N/A")}
- EMA 50: {data.get("ema_50", "N/A")}
- Bollinger Position: {data.get("bb_position", "N/A")}
- Volume Ratio: {data.get("volume_ratio", "N/A")}
- ATR: {data.get("atr", "N/A")}

Provide a brief analysis (under 200 words):
1. Trend direction (bullish/bearish/neutral)
2. Key support/resistance levels
3. Entry recommendation (buy/sell/hold)
4. Risk level (low/medium/high)
5. Suggested timeframes for entry

Be concise and actionable. Use emoji where appropriate."""

        response = self.generate(prompt)

        if response:
            return f"🧠 *AI ANALYSIS: {pair}*\n\n{response}\n\n🤖 Model: {self.model}\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        else:
            return "❌ AI analysis failed. Check Ollama connection."

    def get_trading_signal(self, pair: str, data: Dict[str, Any]) -> str:
        """Get AI-powered trading signal"""
        if not self.available:
            return "❌ Ollama not available."

        prompt = f"""Based on this {pair} data, give me a SINGLE trading signal:

RSI: {data.get("rsi", 50)}
MACD: {"Bullish" if data.get("macd", 0) > 0 else "Bearish"}
EMA Trend: {"Bullish" if data.get("ema_9", 0) > data.get("ema_21", 0) else "Bearish"}
BB Position: {data.get("bb_position", 0.5):.2f} (0=oversold, 1=overbought)
Volume: {"High" if data.get("volume_ratio", 1) > 1.5 else "Normal"}

Respond ONLY with:
🟢 BUY - if bullish setup
🔴 SELL - if bearish setup
⚪️ HOLD - if unclear/neutral

Add one line explanation after the signal."""

        response = self.generate(prompt)

        if response:
            # Clean and format response
            lines = response.strip().split("\n")
            signal = lines[0] if lines else "⚪️ HOLD"
            explanation = "\n".join(lines[1:]) if len(lines) > 1 else ""

            return f"📊 *AI SIGNAL: {pair}*\n\n{signal}\n{explanation}\n\n🤖 {self.model}"
        else:
            return "❌ Signal generation failed."

    def generate_market_report(self, pairs_data: Dict[str, Dict]) -> str:
        """Generate daily market report for multiple pairs"""
        if not self.available:
            return "❌ Ollama not available."

        pairs_text = "\n".join(
            [
                f"- {pair}: RSI={d.get('rsi', 'N/A')}, MACD={'+' if d.get('macd', 0) > 0 else ''}{d.get('macd', 0):.4f}, Trend={'↑' if d.get('ema_9', 0) > d.get('ema_21', 0) else '↓'}"
                for pair, d in pairs_data.items()
            ]
        )

        prompt = f"""Generate a brief crypto market report.

Pairs Data:
{pairs_text}

Current Time: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Include:
1. Overall market sentiment (bullish/bearish/neutral)
2. Best pair to trade now
3. Risk assessment
4. Suggested strategy for next 24h

Keep it under 300 words. Use emoji."""

        response = self.generate(prompt)

        if response:
            return f"📈 *DAILY MARKET REPORT*\n\n{response}\n\n🤖 {self.model}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        else:
            return "❌ Report generation failed."

    def explain_indicator(self, indicator: str) -> str:
        """Explain a technical indicator"""
        if not self.available:
            return "❌ Ollama not available."

        prompt = f"""Explain {indicator} in crypto trading:

1. What is it?
2. How is it calculated?
3. How to use it for entries/exits?
4. Common mistakes to avoid

Be educational but concise. Under 200 words."""

        response = self.generate(prompt)

        if response:
            return f"📚 *{indicator.upper()} EXPLAINED*\n\n{response}\n\n🤖 {self.model}"
        else:
            return f"❌ Could not explain {indicator}"


# Singleton instance
_analyzer: Optional[OllamaAnalyzer] = None


def get_analyzer() -> OllamaAnalyzer:
    """Get or create analyzer singleton"""
    global _analyzer
    if _analyzer is None:
        _analyzer = OllamaAnalyzer()
    return _analyzer


def is_ollama_available() -> bool:
    """Check if Ollama is available"""
    return get_analyzer().available


# Telegram command handlers
async def cmd_ai_analyze(freqtrade, args: List[str], send_msg) -> None:
    """Handle /ai_analyze command"""
    analyzer = get_analyzer()

    if not args:
        await send_msg("Usage: /ai_analyze BTC/USDT")
        return

    pair = args[0]

    try:
        # Get current data
        dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, freqtrade.timeframe)
        if dataframe.empty:
            await send_msg(f"❌ No data for {pair}")
            return

        last = dataframe.iloc[-1]

        data = {
            "price": last.get("close", 0),
            "rsi": last.get("rsi", 50),
            "macd": last.get("macd", 0),
            "ema_9": last.get("ema_9", 0),
            "ema_21": last.get("ema_21", 0),
            "ema_50": last.get("ema_50", 0),
            "bb_position": last.get("bb_position", 0.5),
            "volume_ratio": last.get("volume_ratio", 1),
            "atr": last.get("atr", 0),
        }

        result = analyzer.analyze_pair(pair, data)
        await send_msg(result)

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


async def cmd_ai_signal(freqtrade, args: List[str], send_msg) -> None:
    """Handle /ai_signal command"""
    analyzer = get_analyzer()

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

        result = analyzer.get_trading_signal(pair, data)
        await send_msg(result)

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


async def cmd_ai_report(freqtrade, send_msg) -> None:
    """Handle /ai_report command"""
    analyzer = get_analyzer()

    try:
        pairs = freqtrade.config.get("exchange", {}).get("pair_whitelist", [])
        pairs_data = {}

        for pair in pairs[:5]:  # Limit to 5 pairs
            try:
                dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, freqtrade.timeframe)
                if not dataframe.empty:
                    last = dataframe.iloc[-1]
                    pairs_data[pair] = {
                        "rsi": last.get("rsi", 50),
                        "macd": last.get("macd", 0),
                        "ema_9": last.get("ema_9", 0),
                        "ema_21": last.get("ema_21", 0),
                        "volume_ratio": last.get("volume_ratio", 1),
                    }
            except:
                pass

        if pairs_data:
            result = analyzer.generate_market_report(pairs_data)
            await send_msg(result)
        else:
            await send_msg("❌ No pair data available")

    except Exception as e:
        await send_msg(f"❌ Error: {str(e)}")


async def cmd_ai_learn(freqtrade, args: List[str], send_msg) -> None:
    """Handle /ai_learn command - explain indicators"""
    analyzer = get_analyzer()

    if not args:
        indicators = ["RSI", "MACD", "EMA", "Bollinger Bands", "ATR", "ADX"]
        await send_msg(
            "📚 *Available Indicators*\n\n" + "\n".join([f"/ai_learn {ind}" for ind in indicators])
        )
        return

    indicator = " ".join(args)
    result = analyzer.explain_indicator(indicator)
    await send_msg(result)


if __name__ == "__main__":
    # Test
    import os

    analyzer = OllamaAnalyzer()

    if analyzer.available:
        print("Testing AI analysis...")
        test_data = {
            "price": 50000,
            "rsi": 45,
            "macd": 150.5,
            "ema_9": 50100,
            "ema_21": 49900,
            "ema_50": 49500,
            "bb_position": 0.35,
            "volume_ratio": 1.3,
            "atr": 450,
        }
        print(analyzer.analyze_pair("BTC/USDT", test_data))
    else:
        print("Ollama not available. Install from https://ollama.ai")
