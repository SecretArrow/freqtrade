#!/usr/bin/env python3
"""
QuantumEdge Auto Alert System
Automatically analyzes pairs per timeframe and sends alerts
"""

import os
import sys
import json
import time
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger("AutoAlert")


class AutoAlertSystem:
    """
    Auto alert system that:
    - Monitors multiple timeframes
    - Uses selected AI provider for analysis
    - Sends alerts when signals detected
    - Prevents alert spam with cooldown
    """

    def __init__(self, config_path: str = None, telegram=None):
        self.config = self._load_config(config_path)
        self.telegram = telegram
        self.running = False
        self.check_interval = self.config.get("check_interval_seconds", 300)  # 5 min default
        self.alert_cooldown = self.config.get("alert_cooldown_minutes", 15)
        self.enabled_timeframes = self.config.get("timeframes", ["15m", "1h", "4h"])
        self.min_confidence = self.config.get("min_confidence", 60)

        self.last_alerts: Dict[str, datetime] = {}
        self.alert_count = 0

        # Import AI analyzer
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from user_data.ai_analyzer import get_analyzer, MultiProviderAnalyzer

            self.ai_analyzer = MultiProviderAnalyzer(config_path)
        except ImportError as e:
            logger.warning(f"Could not import AI analyzer: {e}")
            self.ai_analyzer = None

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        if config_path is None:
            config_path = os.path.join(Path(__file__).parent.parent, "config.json")

        try:
            with open(config_path, "r") as f:
                full_config = json.load(f)
                return full_config.get("auto_alert", {})
        except Exception as e:
            logger.warning(f"Could not load auto_alert config: {e}")
            return {
                "enabled": True,
                "timeframes": ["15m", "1h", "4h"],
                "min_confidence": 60,
                "alert_cooldown_minutes": 15,
                "check_interval_seconds": 300,
            }

    def _send_telegram(self, message: str):
        """Send message via Telegram if available"""
        if self.telegram:
            try:
                import asyncio

                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.telegram._send_msg(message))
            except Exception as e:
                logger.error(f"Error sending Telegram message: {e}")
        else:
            logger.info(f"Alert: {message}")

    def can_alert(self, key: str) -> bool:
        """Check if alert is not in cooldown"""
        if key not in self.last_alerts:
            return True

        elapsed = (datetime.now() - self.last_alerts[key]).total_seconds() / 60
        return elapsed >= self.alert_cooldown

    def record_alert(self, key: str):
        """Record alert timestamp"""
        self.last_alerts[key] = datetime.now()
        self.alert_count += 1

    def get_indicators(self, pair: str, timeframe: str) -> Optional[Dict]:
        """Get indicators from dataframe"""
        try:
            # Import freqtrade modules
            from freqtrade.configuration import Configuration
            from freqtrade.exchange import Exchange

            config = Configuration.from_files([])

            # Try to get data from exchange
            # This is simplified - actual implementation would need bot instance
            return None

        except Exception as e:
            logger.debug(f"Could not get indicators: {e}")
            return None

    def calculate_signal(self, data: Dict) -> Dict:
        """Calculate signal from indicators"""
        if not data:
            return {"signal": "HOLD", "confidence": 0}

        rsi = data.get("rsi", 50)
        ema_9 = data.get("ema_9", 0)
        ema_21 = data.get("ema_21", 0)
        macd = data.get("macd", 0)
        macdsignal = data.get("macdsignal", 0)
        bb_position = data.get("bb_position", 0.5)
        volume_ratio = data.get("volume_ratio", 1)

        # Count bullish/bearish factors
        bullish = 0
        bearish = 0

        # EMA trend
        if ema_9 > ema_21:
            bullish += 1
        else:
            bearish += 1

        # RSI
        if rsi < 30:
            bullish += 2  # Oversold - strong buy signal
        elif rsi < 40:
            bullish += 1
        elif rsi > 70:
            bearish += 2
        elif rsi > 60:
            bearish += 1

        # MACD
        if macd > macdsignal:
            bullish += 1
        else:
            bearish += 1

        # Bollinger
        if bb_position < 0.2:
            bullish += 1
        elif bb_position > 0.8:
            bearish += 1

        # Volume
        if volume_ratio > 1.5:
            bullish += 1

        # Calculate signal
        total = bullish + bearish
        if total == 0:
            return {"signal": "HOLD", "confidence": 50}

        bullish_pct = (bullish / total) * 100

        if bullish_pct >= 70:
            confidence = bullish_pct
            signal = "BUY"
        elif bullish_pct <= 30:
            confidence = 100 - bullish_pct
            signal = "SELL"
        else:
            confidence = 100 - abs(50 - bullish_pct) * 2
            signal = "HOLD"

        return {
            "signal": signal,
            "confidence": min(100, int(confidence)),
            "bullish": bullish,
            "bearish": bearish,
            "rsi": rsi,
            "ema_trend": "bullish" if ema_9 > ema_21 else "bearish",
            "macd": "bullish" if macd > macdsignal else "bearish",
        }

    def format_alert(self, pair: str, timeframe: str, signal: Dict, price: float) -> str:
        """Format alert message"""
        emoji = "🟢" if signal["signal"] == "BUY" else "🔴" if signal["signal"] == "SELL" else "⚪️"

        provider_name = "Unknown"
        if self.ai_analyzer:
            provider = self.ai_analyzer.get_provider()
            if provider:
                provider_name = provider.get_name()

        return f"""{emoji} *AUTO ALERT: {signal["signal"]}*

📊 Pair: {pair}
⏱️ Timeframe: {timeframe}
📈 Signal: {signal["signal"]}
🎯 Confidence: {signal["confidence"]}%
💰 Price: {price:.6f}

📉 Indicators:
• RSI: {signal.get("rsi", "N/A"):.1f}
• EMA: {signal.get("ema_trend", "N/A")}
• MACD: {signal.get("macd", "N/A")}

🤖 AI Provider: {provider_name}
⏰ Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

    def check_pair(self, pair: str, timeframes: List[str]) -> List[Dict]:
        """Check a pair across all timeframes"""
        signals = []

        for tf in timeframes:
            try:
                # This would need access to the bot's datapoints
                # For now, we use placeholder - actual implementation
                # would integrate with freqtrade's data provider
                continue

            except Exception as e:
                logger.debug(f"Error checking {pair} {tf}: {e}")

        return signals

    def run_check(self, freqtrade=None) -> List[Dict]:
        """Run one check cycle"""
        all_signals = []

        if not freqtrade:
            logger.debug("No freqtrade instance, skipping check")
            return all_signals

        try:
            # Get whitelist
            pairs = freqtrade.config.get("exchange", {}).get("pair_whitelist", [])

            for pair in pairs:
                for tf in self.enabled_timeframes:
                    key = f"{pair}_{tf}"

                    try:
                        # Get dataframe
                        dataframe, _ = freqtrade.dp.get_analyzed_dataframe(pair, tf)
                        if dataframe.empty:
                            continue

                        last = dataframe.iloc[-1]

                        data = {
                            "close": last.get("close", 0),
                            "rsi": last.get("rsi", 50),
                            "ema_9": last.get("ema_9", 0),
                            "ema_21": last.get("ema_21", 0),
                            "macd": last.get("macd", 0),
                            "macdsignal": last.get("macdsignal", 0),
                            "bb_position": last.get("bb_position", 0.5),
                            "volume_ratio": last.get("volume_ratio", 1),
                        }

                        signal = self.calculate_signal(data)

                        if (
                            signal["confidence"] >= self.min_confidence
                            and signal["signal"] != "HOLD"
                        ):
                            if self.can_alert(key):
                                self.record_alert(key)

                                signal_data = {
                                    "pair": pair,
                                    "timeframe": tf,
                                    "signal": signal["signal"],
                                    "confidence": signal["confidence"],
                                    "price": data["close"],
                                    "rsi": data["rsi"],
                                }

                                all_signals.append(signal_data)

                                # Send alert
                                msg = self.format_alert(pair, tf, signal, data["close"])
                                self._send_telegram(msg)

                    except Exception as e:
                        logger.debug(f"Error analyzing {pair} {tf}: {e}")

        except Exception as e:
            logger.error(f"Error in run_check: {e}")

        return all_signals

    def start(self, freqtrade=None):
        """Start the alert system"""
        self.running = True
        logger.info(f"AutoAlert started - checking every {self.check_interval}s")
        logger.info(f"Timeframes: {', '.join(self.enabled_timeframes)}")
        logger.info(f"Min confidence: {self.min_confidence}%")

        self._send_telegram(
            "🔔 *Auto Alert Started*\n\n"
            f"Checking: {', '.join(self.enabled_timeframes)}\n"
            f"Min confidence: {self.min_confidence}%\n"
            f"Cooldown: {self.alert_cooldown} min"
        )

        while self.running:
            try:
                self.run_check(freqtrade)
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("AutoAlert stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in alert loop: {e}")
                time.sleep(60)

        self._send_telegram("🔕 *Auto Alert Stopped*")

    def stop(self):
        """Stop the alert system"""
        self.running = False


def main():
    """Run as standalone script"""
    import argparse

    parser = argparse.ArgumentParser(description="QuantumEdge Auto Alert System")
    parser.add_argument("--config", "-c", help="Config file path")
    parser.add_argument("--interval", "-i", type=int, default=300, help="Check interval in seconds")
    parser.add_argument(
        "--timeframes", "-t", nargs="+", default=["15m", "1h", "4h"], help="Timeframes to check"
    )
    parser.add_argument("--confidence", "-n", type=int, default=60, help="Min confidence %")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create alert system
    system = AutoAlertSystem(args.config)

    if args.interval:
        system.check_interval = args.interval
    if args.timeframes:
        system.enabled_timeframes = args.timeframes
    if args.confidence:
        system.min_confidence = args.confidence

    # Start
    print("Starting QuantumEdge Auto Alert System...")
    print(f"Timeframes: {system.enabled_timeframes}")
    print(f"Check interval: {system.check_interval}s")
    print(f"Min confidence: {system.min_confidence}%")
    print("")
    print("Press Ctrl+C to stop")
    print("")

    system.start()


if __name__ == "__main__":
    main()
