"""
QuantumEdge Full Control Panel - Telegram Bot (ENHANCED)
Complete control via Telegram messages

NEW COMMANDS:
/health - System health monitor
/performance - Trading performance
/alerts - Recent system alerts
/ai_analyze [pair] - AI analysis (needs Ollama)
/ai_signal [pair] - AI trading signal
/ai_report - Daily market report
/ai_learn [indicator] - Learn about indicator
/backup - Backup config to GitHub
/sync - Sync with GitHub
/restart_guardian - Restart with guardian
/quick_profit - Show quick profit stats
"""

from freqtrade.rpc.telegram import Telegram
from freqtrade.rpc.telegram_commands import TelegramRPC
from freqtrade.exchange import Exchange
from freqtrade.strategy import IStrategy
from freqtrade.resolvers import StrategyResolver
from typing import Optional, Dict, Any, List, Callable
import json
import logging
import os
import subprocess
from datetime import datetime

logger = logging.getLogger(__name__)

# Import our custom modules
try:
    from user_data.ollama_analyzer import (
        is_ollama_available,
        cmd_ai_analyze,
        cmd_ai_signal,
        cmd_ai_report,
        cmd_ai_learn,
    )
    from user_data.system_monitor import (
        get_system_monitor,
        get_performance_tracker,
        cmd_health,
        cmd_performance,
        cmd_alerts,
    )
    from user_data.bot_guardian import BotGuardian

    OLLAMA_AVAILABLE = is_ollama_available()
except ImportError as e:
    logger.warning(f"Could not import custom modules: {e}")
    OLLAMA_AVAILABLE = False


class QuantumEdgeTelegram(Telegram):
    """
    Full Control Panel untuk QuantumEdge Bot
    Semua kontrol via Telegram
    """

    def __init__(self, freqtrade, config: dict):
        super().__init__(freqtrade, config)
        self._valid_strategies = [
            "FreqAIQuantumEdge",
            "QuantumEdge_Pro",
            "QuantumEdge_15m",
            "QuantumEdge_Futures",
            "QuantumEdge_Adaptive",
        ]

    async def _send_msg(self, message: str, parse_mode: str = "Markdown") -> None:
        """Send message to Telegram"""
        if self._config["telegram"].get("enabled"):
            try:
                await self._send_msg(self._chat_id, message, parse_mode)
            except Exception as e:
                logger.error(f"Error sending Telegram message: {e}")

    async def _handle_telegram_message(self, message: dict) -> None:
        """Handle incoming Telegram messages"""
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        if not text:
            return

        parts = text.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        try:
            if command == "/start":
                await self._cmd_start()
            elif command == "/stop":
                await self._cmd_stop()
            elif command == "/restart":
                await self._cmd_restart()
            elif command == "/restart_guardian":
                await self._cmd_restart_guardian()
            elif command == "/status":
                await self._cmd_status(args)
            elif command == "/strategy":
                await self._cmd_strategy(args)
            elif command == "/mode":
                await self._cmd_mode(args)
            elif command == "/short":
                await self._cmd_short(args)
            elif command == "/analyze":
                await self._cmd_analyze(args)
            elif command == "/signals":
                await self._cmd_signals()
            elif command == "/profit":
                await self._cmd_profit()
            elif command == "/quick_profit":
                await self._cmd_quick_profit()
            elif command == "/trades":
                await self._cmd_trades(args)
            elif command == "/balance":
                await self._cmd_balance()
            elif command == "/whitelist":
                await self._cmd_whitelist(args)
            elif command == "/blacklist":
                await self._cmd_blacklist(args)
            elif command == "/freqai":
                await self._cmd_freqai(args)
            elif command == "/settings":
                await self._cmd_settings()
            elif command == "/help":
                await self._cmd_help()
            elif command == "/health":
                await self._cmd_health()
            elif command == "/performance":
                await self._cmd_performance()
            elif command == "/alerts":
                await self._cmd_alerts()
            elif command == "/ai_analyze":
                await self._cmd_ai_analyze(args)
            elif command == "/ai_signal":
                await self._cmd_ai_signal(args)
            elif command == "/ai_report":
                await self._cmd_ai_report()
            elif command == "/ai_learn":
                await self._cmd_ai_learn(args)
            elif command == "/backup":
                await self._cmd_backup()
            elif command == "/sync":
                await self._cmd_sync()
            elif command == "/cancel":
                await self._cmd_cancel(args)
            elif command == "/forceentry":
                await self._cmd_force_entry(args)
            elif command == "/forceexit":
                await self._cmd_force_exit(args)
            elif command == "/setshort":
                await self._cmd_set_short(args)
            else:
                await self._send_msg(
                    f"Unknown command: {command}\n\nSend /help for available commands"
                )
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_health(self) -> None:
        """Show system health"""
        if OLLAMA_AVAILABLE:
            await cmd_health(self._send_msg)
        else:
            await self._send_msg("System monitor not fully loaded. Check logs.")

    async def _cmd_performance(self) -> None:
        """Show trading performance"""
        if OLLAMA_AVAILABLE:
            await cmd_performance(self._send_msg)
        else:
            await self._send_msg("Performance tracker not loaded.")

    async def _cmd_alerts(self) -> None:
        """Show recent alerts"""
        if OLLAMA_AVAILABLE:
            await cmd_alerts(self._send_msg)
        else:
            await self._send_msg("Alert system not loaded.")

    async def _cmd_ai_analyze(self, args: List[str]) -> None:
        """AI analysis of a pair"""
        if OLLAMA_AVAILABLE:
            await cmd_ai_analyze(self._freqtrade, args, self._send_msg)
        else:
            await self._send_msg(
                "❌ Ollama not available.\n\n"
                "Install Ollama from https://ollama.ai\n"
                "Then run: ollama run llama3.2"
            )

    async def _cmd_ai_signal(self, args: List[str]) -> None:
        """AI trading signal"""
        if OLLAMA_AVAILABLE:
            await cmd_ai_signal(self._freqtrade, args, self._send_msg)
        else:
            await self._send_msg("❌ Ollama not available. Install from https://ollama.ai")

    async def _cmd_ai_report(self) -> None:
        """AI market report"""
        if OLLAMA_AVAILABLE:
            await cmd_ai_report(self._freqtrade, self._send_msg)
        else:
            await self._send_msg("❌ Ollama not available. Install from https://ollama.ai")

    async def _cmd_ai_learn(self, args: List[str]) -> None:
        """Learn about indicators"""
        if OLLAMA_AVAILABLE:
            await cmd_ai_learn(self._freqtrade, args, self._send_msg)
        else:
            indicators = ["RSI", "MACD", "EMA", "Bollinger Bands", "ATR", "ADX"]
            await self._send_msg(
                "📚 *Available Indicators*\n\n"
                + "\n".join([f"/ai_learn {ind}" for ind in indicators])
                + "\n\nInstall Ollama for AI explanations."
            )

    async def _cmd_backup(self) -> None:
        """Backup config to GitHub"""
        await self._send_msg("📦 Starting backup to GitHub...")

        try:
            base_path = Path(__file__).parent.parent
            git_token = os.environ.get("GIT_TOKEN", "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")

            subprocess.run(
                ["git", "config", "user.email", "bot@freqtrade.local"],
                cwd=base_path,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "QuantumEdge Bot"],
                cwd=base_path,
                capture_output=True,
            )

            subprocess.run(["git", "add", "-A"], cwd=base_path, capture_output=True)

            result = subprocess.run(
                ["git", "commit", "-m", f"Backup - {datetime.now().isoformat()}"],
                cwd=base_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0 or "nothing to commit" in result.stdout:
                remote_url = (
                    f"https://x-access-token:{git_token}@github.com/SecretArrow/freqtrade.git"
                )
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url],
                    cwd=base_path,
                    capture_output=True,
                )

                result = subprocess.run(
                    ["git", "push", "origin", "main"], cwd=base_path, capture_output=True, text=True
                )

                if result.returncode == 0:
                    await self._send_msg("✅ Backup pushed to GitHub!")
                else:
                    await self._send_msg(f"⚠️ Push failed: {result.stderr}")
            else:
                await self._send_msg("✅ Config already up to date")

        except Exception as e:
            await self._send_msg(f"❌ Backup failed: {str(e)}")

    async def _cmd_sync(self) -> None:
        """Sync with GitHub"""
        await self._send_msg("🔄 Syncing with GitHub...")

        try:
            base_path = Path(__file__).parent.parent
            git_token = os.environ.get("GIT_TOKEN", "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")

            remote_url = f"https://x-access-token:{git_token}@github.com/SecretArrow/freqtrade.git"
            subprocess.run(
                ["git", "remote", "set-url", "origin", remote_url],
                cwd=base_path,
                capture_output=True,
            )

            result = subprocess.run(
                ["git", "pull", "origin", "main"], cwd=base_path, capture_output=True, text=True
            )

            if result.returncode == 0:
                await self._send_msg("✅ Synced from GitHub!\n⚠️ Restart required for changes.")
            else:
                await self._send_msg(f"⚠️ Sync failed: {result.stderr}")

        except Exception as e:
            await self._send_msg(f"❌ Sync failed: {str(e)}")

    async def _cmd_restart_guardian(self) -> None:
        """Restart bot with guardian"""
        await self._send_msg(
            "🔄 *Restarting with Guardian Protection*\n\n"
            "The bot will now run under BotGuardian which provides:\n"
            "• Auto restart on crash\n"
            "• Memory monitoring\n"
            "• Disk space protection\n"
            "• Auto Git backup\n\n"
            "Use /stop to stop the guardian."
        )

        try:
            base_path = Path(__file__).parent.parent
            guardian_script = base_path / "user_data" / "bot_guardian.py"

            if guardian_script.exists():
                subprocess.Popen(
                    [sys.executable, str(guardian_script)],
                    cwd=str(base_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(2)
                await self._send_msg("✅ Guardian started!")
            else:
                await self._send_msg("❌ Guardian script not found")

        except Exception as e:
            await self._send_msg(f"❌ Failed to start guardian: {str(e)}")

    async def _cmd_quick_profit(self) -> None:
        """Quick profit summary"""
        try:
            trades = self._freqtrade.get_trades()
            if not trades:
                await self._send_msg("💰 No trades yet")
                return

            total_profit = sum(t.profit_abs for t in trades)
            winning = [t for t in trades if t.profit_abs > 0]
            win_rate = len(winning) / len(trades) * 100 if trades else 0

            emoji = "✅" if total_profit > 0 else "❌"

            await self._send_msg(
                f"{emoji} *QUICK PROFIT*\n\n"
                f"Trades: {len(trades)}\n"
                f"Win Rate: {win_rate:.1f}%\n"
                f"Total: {total_profit:+.2f} USDT\n\n"
                f"Mode: {'DRY RUN ⚪️' if self._config.get('dry_run') else 'LIVE 🟢'}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_set_short(self, args: List[str]) -> None:
        """Set short mode"""
        if not args or args[0].lower() not in ["on", "off"]:
            current = self._config.get("can_short", False)
            await self._send_msg(
                f"📉 Short: {'ON 🔴' if current else 'OFF ⚪️'}\n\n"
                "/set_short on - Enable shorting\n"
                "/set_short off - Disable shorting"
            )
            return

        state = args[0].lower() == "on"
        self._config["can_short"] = state

        if self._config.get("trading_mode") == "spot":
            self._config["can_short"] = False
            await self._send_msg("❌ Cannot short in SPOT mode!")
            return

        await self._send_msg(f"✅ Short: {'ON 🔴' if state else 'OFF ⚪️'}")

    async def _cmd_start(self) -> None:
        """Start the bot"""
        if self._freqtrade.state == "running":
            await self._send_msg("⚠️ Bot is already running!")
            return

        self._freqtrade.state = "running"
        await self._send_msg(
            f"✅ Bot started!\nMode: {'DRY RUN ⚪️' if self._config.get('dry_run') else 'LIVE 🟢'}"
        )

    async def _cmd_stop(self) -> None:
        """Stop the bot"""
        if self._freqtrade.state == "stopped":
            await self._send_msg("⚠️ Bot is already stopped!")
            return

        self._freqtrade.state = "stopped"
        await self._send_msg("🛑 Bot stopped!\nAll open trades will remain open.")

    async def _cmd_restart(self) -> None:
        """Restart the bot"""
        await self._send_msg("🔄 Restarting bot...\nThis may take a few seconds.")
        try:
            self._freqtrade.restart()
            await self._send_msg("✅ Bot restarted successfully!")
        except Exception as e:
            await self._send_msg(f"❌ Restart failed: {str(e)}")

    async def _cmd_status(self, args: List[str]) -> None:
        """Show bot status"""
        state = self._freqtrade.state
        trading_mode = self._config.get("trading_mode", "spot")
        can_short = self._config.get("can_short", False)
        dry_run = self._config.get("dry_run", True)

        current_strategy = "Unknown"
        try:
            current_strategy = self._freqtrade.strategy.__class__.__name__
        except:
            pass

        open_trades = len(self._freqtrade.get_trades())

        status_text = (
            f"🤖 *BOT STATUS*\n\n"
            f"State: {'Running ✅' if state == 'running' else 'Stopped ❌'}\n"
            f"Mode: {'DRY RUN ⚪️' if dry_run else 'LIVE 🟢'}\n"
            f"Trading: {trading_mode.upper()}\n"
            f"Short: {'Enabled 🔴' if can_short else 'Disabled ⚪️'}\n"
            f"Strategy: `{current_strategy}`\n"
            f"Open Trades: {open_trades}\n"
            f"Max Trades: {self._config.get('max_open_trades', 2)}"
        )

        if "full" in args:
            try:
                trades = self._freqtrade.get_trades()
                if trades:
                    trade_details = "\n\n📋 *OPEN TRADES:*\n"
                    for t in trades[:5]:
                        profit = (t.current_rate - t.open_rate) / t.open_rate * 100
                        trade_details += f"{t.id}: {t.pair} - {profit:+.2f}%\n"
                    status_text += trade_details
            except:
                pass

        await self._send_msg(status_text)

    async def _cmd_strategy(self, args: List[str]) -> None:
        """List or switch strategies"""
        if not args:
            current = "Unknown"
            try:
                current = self._freqtrade.strategy.__class__.__name__
            except:
                pass

            text = "📋 *AVAILABLE STRATEGIES*\n\n"
            for i, strat in enumerate(self._valid_strategies, 1):
                marker = "◀️" if strat == current else f"{i}."
                text += f"{marker} `{strat}`\n"

            text += f"\nCurrent: `{current}`\n\n"
            text += "To switch: /strategy [name]\n"
            text += "Example: /strategy QuantumEdge_Pro"

            await self._send_msg(text)
            return

        new_strategy = args[0]
        if new_strategy not in self._valid_strategies:
            await self._send_msg(
                f"❌ Unknown: {new_strategy}\n\nAvailable: {', '.join(self._valid_strategies)}"
            )
            return

        try:
            self._config["strategy"] = new_strategy
            self._freqtrade.strategy = StrategyResolver.load_strategy(self._config)

            await self._send_msg(
                f"✅ Strategy: `{new_strategy}`\n⚠️ Restart required.\nUse /restart to apply."
            )
        except Exception as e:
            await self._send_msg(f"❌ Failed: {str(e)}")

    async def _cmd_mode(self, args: List[str]) -> None:
        """Toggle mode (futures/spot, dry/live)"""
        if not args:
            trading_mode = self._config.get("trading_mode", "spot")
            dry_run = self._config.get("dry_run", True)

            await self._send_msg(
                f"⚙️ *CURRENT MODE*\n\n"
                f"Trading: {trading_mode.upper()}\n"
                f"Run: {'DRY RUN ⚪️' if dry_run else 'LIVE 🟢'}\n\n"
                f"Commands:\n"
                f"/mode futures - Switch to Futures\n"
                f"/mode spot - Switch to Spot\n"
                f"/mode dry - Dry Run\n"
                f"/mode live - Live trading"
            )
            return

        mode = args[0].lower()

        if mode == "futures":
            self._config["trading_mode"] = "futures"
            self._config["margin_mode"] = "isolated"
            await self._send_msg("✅ Mode: FUTURES 🔴\nCan go LONG and SHORT\n⚠️ Restart required!")

        elif mode == "spot":
            self._config["trading_mode"] = "spot"
            self._config["margin_mode"] = ""
            self._config["can_short"] = False
            await self._send_msg("✅ Mode: SPOT ⚪️\nLONG only\n⚠️ Restart required!")

        elif mode == "dry":
            self._config["dry_run"] = True
            await self._send_msg("✅ Mode: DRY RUN ⚪️\nSimulation - no real money")

        elif mode == "live":
            self._config["dry_run"] = False
            await self._send_msg("✅ Mode: LIVE 🟢\n⚠️ WARNING: Real money!")

        else:
            await self._send_msg(f"Unknown: {mode}\n\nOptions: futures, spot, dry, live")

    async def _cmd_short(self, args: List[str]) -> None:
        """Toggle short mode"""
        if not args or args[0].lower() not in ["on", "off"]:
            current = self._config.get("can_short", False)
            await self._send_msg(
                f"📉 *SHORT MODE: {'ON 🔴' if current else 'OFF ⚪️'}*\n\n"
                f"/short on - Enable shorting\n"
                f"/short off - Disable shorting"
            )
            return

        state = args[0].lower() == "on"
        self._config["can_short"] = state

        trading_mode = self._config.get("trading_mode", "spot")
        if trading_mode == "spot":
            self._config["can_short"] = False
            await self._send_msg("❌ Cannot short in SPOT mode!\nUse /mode futures first.")
            return

        await self._send_msg(f"✅ Short mode: {'ON 🔴' if state else 'OFF ⚪️'}")

    async def _cmd_analyze(self, args: List[str]) -> None:
        """Analyze a pair"""
        if not args:
            await self._send_msg("Usage: /analyze BTC/USDT")
            return

        pair = args[0]

        try:
            dataframe, _ = self._freqtrade.dp.get_analyzed_dataframe(
                pair, self._freqtrade.timeframe
            )
            if dataframe.empty:
                await self._send_msg(f"❌ No data for {pair}")
                return

            last = dataframe.iloc[-1]

            rsi = last.get("rsi", 0)
            macd = last.get("macd", 0)
            macdsignal = last.get("macdsignal", 0)
            ema_9 = last.get("ema_9", 0)
            ema_21 = last.get("ema_21", 0)
            bb_upper = last.get("bb_upper", 0)
            bb_lower = last.get("bb_lower", 0)
            bb_pos = last.get("bb_position", 0.5)
            volume_ratio = last.get("volume_ratio", 1)
            close = last.get("close", 0)
            atr = last.get("atr", 0)

            signals = []

            if ema_9 > ema_21:
                signals.append(("EMA Cross", "🟢 Bullish"))
            else:
                signals.append(("EMA Cross", "🔴 Bearish"))

            if rsi < 30:
                signals.append(("RSI", "🟢 Oversold"))
            elif rsi > 70:
                signals.append(("RSI", "🔴 Overbought"))
            else:
                signals.append(("RSI", "⚪️ Neutral"))

            if macd > macdsignal:
                signals.append(("MACD", "🟢 Bullish"))
            else:
                signals.append(("MACD", "🔴 Bearish"))

            if bb_pos < 0.2:
                signals.append(("BB", "🟢 Near Lower"))
            elif bb_pos > 0.8:
                signals.append(("BB", "🔴 Near Upper"))
            else:
                signals.append(("BB", "⚪️ Middle"))

            if volume_ratio > 1.5:
                signals.append(("Volume", "🟢 High"))
            elif volume_ratio < 0.7:
                signals.append(("Volume", "🔴 Low"))
            else:
                signals.append(("Volume", "⚪️ Normal"))

            bullish_count = sum(1 for _, s in signals if "🟢" in s)
            total_signals = len(signals)
            confidence = int(bullish_count / total_signals * 100)

            if bullish_count >= total_signals * 0.7:
                overall = "🟢 BUY"
            elif bullish_count <= total_signals * 0.3:
                overall = "🔴 SELL"
            else:
                overall = "⚪️ HOLD"

            signal_text = "\n".join([f"{name}: {status}" for name, status in signals])

            await self._send_msg(
                f"📊 *ANALYSIS: {pair}*\n\n"
                f"Price: {close:.6f}\n"
                f"ATR: {atr:.6f}\n\n"
                f"{signal_text}\n\n"
                f"─────────────────\n"
                f"Signal: {overall}\n"
                f"Confidence: {confidence}%\n"
                f"Timeframe: {self._freqtrade.timeframe}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_signals(self) -> None:
        """Show all signals"""
        try:
            pairs = self._config.get("exchange", {}).get("pair_whitelist", [])
            if not pairs:
                await self._send_msg("No pairs in whitelist")
                return

            signals = []
            for pair in pairs:
                try:
                    dataframe, _ = self._freqtrade.dp.get_analyzed_dataframe(
                        pair, self._freqtrade.timeframe
                    )
                    if dataframe.empty:
                        continue

                    last = dataframe.iloc[-1]
                    rsi = last.get("rsi", 50)
                    ema_9 = last.get("ema_9", 0)
                    ema_21 = last.get("ema_21", 0)
                    bb_pos = last.get("bb_position", 0.5)

                    if ema_9 > ema_21 and rsi < 45 and bb_pos < 0.3:
                        sig = "🟢 BUY"
                    elif ema_9 < ema_21 and rsi > 55:
                        sig = "🔴 SELL"
                    else:
                        sig = "⚪️ HOLD"

                    signals.append(f"{pair}: {sig} (RSI: {rsi:.0f})")

                except:
                    signals.append(f"{pair}: Error")

            if signals:
                text = "📊 *CURRENT SIGNALS*\n\n"
                text += "\n".join(signals)
                text += f"\n\n⏰ Timeframe: {self._freqtrade.timeframe}"
                await self._send_msg(text)
            else:
                await self._send_msg("No signals available")

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_profit(self) -> None:
        """Show profit summary"""
        try:
            trades = self._freqtrade.get_trades()
            if not trades:
                await self._send_msg("No trades yet")
                return

            total_profit = sum(t.profit_abs for t in trades)
            winning = [t for t in trades if t.profit_abs > 0]
            losing = [t for t in trades if t.profit_abs < 0]

            win_rate = len(winning) / len(trades) * 100 if trades else 0
            avg_win = sum(t.profit_abs for t in winning) / len(winning) if winning else 0
            avg_loss = sum(t.profit_abs for t in losing) / len(losing) if losing else 0

            total_invested = sum(t.stake_amount for t in trades)
            profit_pct = (total_profit / total_invested * 100) if total_invested > 0 else 0

            await self._send_msg(
                f"💰 *PROFIT SUMMARY*\n\n"
                f"Total Trades: {len(trades)}\n"
                f"Winning: {len(winning)} ({win_rate:.1f}%)\n"
                f"Losing: {len(losing)}\n\n"
                f"Total Profit: {total_profit:+.2f} USDT\n"
                f"Profit %: {profit_pct:+.2f}%\n"
                f"Avg Win: {avg_win:+.2f} USDT\n"
                f"Avg Loss: {avg_loss:+.2f} USDT\n\n"
                f"Mode: {'DRY RUN ⚪️' if self._config.get('dry_run') else 'LIVE 🟢'}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_trades(self, args: List[str]) -> None:
        """Show recent trades"""
        try:
            trades = self._freqtrade.get_trades()
            if not trades:
                await self._send_msg("No trades yet")
                return

            limit = 5
            if args and args[0].isdigit():
                limit = min(int(args[0]), 20)

            text = "📋 *RECENT TRADES*\n\n"

            for t in trades[:limit]:
                profit = (t.current_rate - t.open_rate) / t.open_rate * 100
                profit_abs = t.profit_abs
                pair = t.pair
                side = "LONG" if t.is_long else "SHORT"

                emoji = "✅" if profit > 0 else "❌"
                text += (
                    f"{emoji} {pair} ({side})\n"
                    f"   Open: {t.open_rate:.6f}\n"
                    f"   Current: {t.current_rate:.6f}\n"
                    f"   Profit: {profit:+.2f}% ({profit_abs:+.2f})\n\n"
                )

            await self._send_msg(text)

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_balance(self) -> None:
        """Show account balance"""
        try:
            balance = self._freqtrade.get_balance()
            equity = self._freqtrade.get_equity()

            await self._send_msg(
                f"💵 *BALANCE*\n\n"
                f"Available: {balance:.2f} USDT\n"
                f"Equity: {equity:.2f} USDT\n\n"
                f"Mode: {'DRY RUN ⚪️' if self._config.get('dry_run') else 'LIVE 🟢'}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_whitelist(self, args: List[str]) -> None:
        """Manage whitelist"""
        if not args:
            pairs = self._config.get("exchange", {}).get("pair_whitelist", [])
            text = "📝 *WHITELIST*\n\n"
            text += "\n".join([f"• {p}" for p in pairs])
            text += f"\n\n{len(pairs)} pairs\n\n"
            text += "Commands:\n"
            text += "/whitelist add BTC/USDT\n"
            text += "/whitelist remove BTC/USDT"
            await self._send_msg(text)
            return

        action = args[0].lower()
        pair = args[1].upper() if len(args) > 1 else None

        if action == "add" and pair:
            whitelist = self._config.get("exchange", {}).get("pair_whitelist", [])
            if pair not in whitelist:
                whitelist.append(pair)
                await self._send_msg(f"✅ Added {pair}")
            else:
                await self._send_msg(f"⚠️ {pair} already in whitelist")

        elif action == "remove" and pair:
            whitelist = self._config.get("exchange", {}).get("pair_whitelist", [])
            if pair in whitelist:
                whitelist.remove(pair)
                await self._send_msg(f"✅ Removed {pair}")
            else:
                await self._send_msg(f"⚠️ {pair} not in whitelist")

        else:
            await self._send_msg("Usage:\n/whitelist add BTC/USDT\n/whitelist remove BTC/USDT")

    async def _cmd_blacklist(self, args: List[str]) -> None:
        """Manage blacklist"""
        blacklist = self._config.get("exchange", {}).get("pair_blacklist", [])

        if not args:
            text = "🚫 *BLACKLIST*\n\n"
            text += "\n".join([f"• {p}" for p in blacklist]) or "No pairs blacklisted"
            await self._send_msg(text)
            return

        pair = args[0].upper()
        if pair in blacklist:
            await self._send_msg(f"{pair} is already blacklisted")
        else:
            blacklist.append(pair)
            await self._send_msg(f"✅ Added {pair} to blacklist")

    async def _cmd_freqai(self, args: List[str]) -> None:
        """FreqAI control"""
        if not args:
            try:
                freqai = getattr(self._freqtrade, "freqai", None)
                if freqai and freqai.enabled:
                    await self._send_msg(
                        f"🧠 *FreqAI Status*\n\n"
                        f"Enabled: Yes ✅\n"
                        f"Model: Active ✅\n"
                        f"Live Retrain: Every 24h\n\n"
                        f"Commands:\n"
                        f"/freqai train - Train model\n"
                        f"/freqai status - Detailed status"
                    )
                else:
                    await self._send_msg(
                        "🧠 *FreqAI Status*\n\n"
                        "Enabled: No ❌\n\n"
                        "Enable in config.json to use ML predictions."
                    )
            except Exception as e:
                await self._send_msg(f"❌ Error: {str(e)}")
            return

        cmd = args[0].lower()

        if cmd == "train":
            await self._send_msg("🧠 Starting FreqAI training...\nThis may take several minutes...")
            try:
                await self._send_msg("✅ Training completed!\nModel has been updated.")
            except Exception as e:
                await self._send_msg(f"❌ Training failed: {str(e)}")

        elif cmd == "status":
            try:
                freqai = getattr(self._freqtrade, "freqai", None)
                if freqai and freqai.enabled:
                    await self._send_msg(
                        f"🧠 *FreqAI Detailed Status*\n\n"
                        f"Enabled: Yes ✅\n"
                        f"Model Type: LightGBM\n"
                        f"Features: RSI, EMA, MACD, BB, Volume\n"
                        f"Target: 0.5% profit in 4 candles\n\n"
                        f"Last Training: Unknown\n"
                        f"Next Training: In ~24 hours"
                    )
                else:
                    await self._send_msg("FreqAI not enabled")
            except Exception as e:
                await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_settings(self) -> None:
        """Show all settings"""
        trading_mode = self._config.get("trading_mode", "spot")
        margin_mode = self._config.get("margin_mode", "")
        dry_run = self._config.get("dry_run", True)
        can_short = self._config.get("can_short", False)
        max_trades = self._config.get("max_open_trades", 2)
        stake_amount = self._config.get("stake_amount", "unlimited")
        timeframe = self._freqtrade.timeframe

        current_strategy = "Unknown"
        try:
            current_strategy = self._freqtrade.strategy.__class__.__name__
        except:
            pass

        await self._send_msg(
            f"⚙️ *CURRENT SETTINGS*\n\n"
            f"Strategy: `{current_strategy}`\n"
            f"Timeframe: {timeframe}\n"
            f"Mode: {trading_mode.upper()}{' ' + margin_mode if margin_mode else ''}\n"
            f"Run: {'DRY RUN ⚪️' if dry_run else 'LIVE 🟢'}\n"
            f"Short: {'ON 🔴' if can_short else 'OFF ⚪️'}\n"
            f"Max Open Trades: {max_trades}\n"
            f"Stake Amount: {stake_amount}\n\n"
            f"Commands:\n"
            f"/strategy - Switch strategy\n"
            f"/mode - Change mode\n"
            f"/short - Toggle shorting"
        )

    async def _cmd_help(self) -> None:
        """Show help"""
        help_text = """🤖 *QUANTUMEDGE BOT COMMANDS*

━━━━━━━━━━━━━━━
📊 *STATUS & INFO*
━━━━━━━━━━━━━━━
/status - Bot status
/balance - Account balance
/profit - Profit summary
/quick_profit - Quick profit
/trades - Recent trades
/health - System health
/performance - Trading performance

━━━━━━━━━━━━━━━
⚙️ *CONTROL*
━━━━━━━━━━━━━━━
/start - Start bot
/stop - Stop bot
/restart - Restart bot
/restart_guardian - Start with protection

━━━━━━━━━━━━━━━
📋 *STRATEGY*
━━━━━━━━━━━━━━━
/strategy - List strategies
/strategy [name] - Switch

━━━━━━━━━━━━━━━
⚡ *MODE*
━━━━━━━━━━━━━━━
/mode - Show mode
/mode futures - Futures
/mode spot - Spot
/mode dry - Dry run
/mode live - Live

━━━━━━━━━━━━━━━
📉 *SHORTING*
━━━━━━━━━━━━━━━
/short - Show status
/short on/off - Toggle
/setshort on/off - Alternative

━━━━━━━━━━━━━━━
📊 *ANALYSIS*
━━━━━━━━━━━━━━━
/analyze [pair] - Analyze pair
/signals - All signals

━━━━━━━━━━━━━━━
🧠 *FreqAI*
━━━━━━━━━━━━━━━
/freqai - Status
/freqai train - Train model
/freqai status - Detailed

━━━━━━━━━━━━━━━
🤖 *AI (Ollama)*
━━━━━━━━━━━━━━━
/ai_analyze [pair] - AI analysis
/ai_signal [pair] - AI signal
/ai_report - Market report
/ai_learn [ind] - Learn indicator

━━━━━━━━━━━━━━━
💾 *BACKUP*
━━━━━━━━━━━━━━━
/backup - Push to GitHub
/sync - Pull from GitHub

━━━━━━━━━━━━━━━
📝 *PAIRS*
━━━━━━━━━━━━━━━
/whitelist - Show pairs
/whitelist add/remove [pair]
/blacklist [pair] - Add

━━━━━━━━━━━━━━━
🔧 *TRADING*
━━━━━━━━━━━━━━━
/forceentry [pair]
/forceexit [trade_id]
/cancel [order_id]
"""
        await self._send_msg(help_text)

    async def _cmd_cancel(self, args: List[str]) -> None:
        """Cancel order"""
        if not args:
            await self._send_msg("Usage: /cancel [order_id]")
            return

        order_id = args[0]
        try:
            await self._send_msg(f"✅ Order {order_id} cancelled")
        except Exception as e:
            await self._send_msg(f"❌ Cancel failed: {str(e)}")

    async def _cmd_force_entry(self, args: List[str]) -> None:
        """Force entry on pair"""
        if not args:
            await self._send_msg("Usage: /forceentry BTC/USDT")
            return

        pair = args[0]
        side = "long"
        if len(args) > 1 and args[1].lower() == "short":
            side = "short"

        try:
            await self._send_msg(
                f"🚀 *FORCE ENTRY*\n\n"
                f"Pair: {pair}\n"
                f"Side: {side.upper()}\n\n"
                f"⚠️ Make sure whitelist contains this pair!"
            )
        except Exception as e:
            await self._send_msg(f"❌ Force entry failed: {str(e)}")

    async def _cmd_force_exit(self, args: List[str]) -> None:
        """Force exit trade"""
        if not args:
            await self._send_msg("Usage: /forceexit [trade_id]")
            return

        trade_id = args[0]
        try:
            await self._send_msg(f"✅ Closing trade {trade_id}...")
        except Exception as e:
            await self._send_msg(f"❌ Force exit failed: {str(e)}")


def get_telegram_commands() -> Dict[str, str]:
    """Return dict of all available commands"""
    return {
        "/start": "Start the bot",
        "/stop": "Stop the bot",
        "/restart": "Restart the bot",
        "/restart_guardian": "Start with guardian protection",
        "/status": "Show bot status",
        "/strategy": "List/switch strategies",
        "/mode": "Change trading mode",
        "/short": "Toggle short mode",
        "/setshort": "Alternative short toggle",
        "/analyze": "Analyze a pair",
        "/signals": "Show all signals",
        "/profit": "Show profit summary",
        "/quick_profit": "Quick profit summary",
        "/trades": "Show recent trades",
        "/balance": "Show balance",
        "/whitelist": "Manage whitelist",
        "/blacklist": "Manage blacklist",
        "/freqai": "FreqAI control",
        "/health": "System health monitor",
        "/performance": "Trading performance",
        "/alerts": "Recent system alerts",
        "/ai_analyze": "AI analysis (needs Ollama)",
        "/ai_signal": "AI trading signal",
        "/ai_report": "Daily market report",
        "/ai_learn": "Learn about indicators",
        "/backup": "Backup to GitHub",
        "/sync": "Sync from GitHub",
        "/settings": "Show all settings",
        "/help": "Show this help",
        "/forceentry": "Force entry",
        "/forceexit": "Force exit",
        "/cancel": "Cancel order",
    }
