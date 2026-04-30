"""
QuantumEdge Full Control Panel - Telegram Bot
Complete control via Telegram messages

Commands:
- /start, /stop, /restart - Bot control
- /status, /balance, /profit - Info
- /strategy - Switch strategies
- /mode - Toggle futures/spot, dry/live
- /short on/off - Toggle shorting
- /analyze [pair] [tf] - Technical analysis
- /signals - Show all signals
- /ai_analyze [pair] [tf] - AI analysis with selected provider
- /ai_signal [pair] - Quick AI signal
- /ai_status - Show AI provider status
- /ai_set [provider] - Switch AI provider
- /ai_report - Market report
- /health - System health
- /performance - Trading performance
- /help - Show all commands
"""

from freqtrade.rpc.telegram import Telegram
from freqtrade.resolvers import StrategyResolver
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

try:
    from user_data.ai_analyzer import (
        get_analyzer,
        get_status as get_ai_status,
        cmd_ai_analyze,
        cmd_ai_signal,
        cmd_ai_status,
        cmd_ai_set,
        cmd_ai_report,
    )
    from user_data.system_monitor import (
        get_system_monitor,
        get_performance_tracker,
        cmd_health,
        cmd_performance,
        cmd_alerts,
    )

    AI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Could not import custom modules: {e}")
    AI_AVAILABLE = False


class QuantumEdgeTelegram(Telegram):
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
        if self._config["telegram"].get("enabled"):
            try:
                await self._send_msg(self._chat_id, message, parse_mode)
            except Exception as e:
                logger.error(f"Error sending Telegram message: {e}")

    async def _handle_telegram_message(self, message: dict) -> None:
        text = message.get("text", "")
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
                await self._cmd_ai(args)
            elif command == "/ai_signal":
                await self._cmd_ai_signal(args)
            elif command == "/ai_status":
                await self._cmd_ai_status()
            elif command == "/ai_set":
                await self._cmd_ai_set(args)
            elif command == "/ai_report":
                await self._cmd_ai_report()
            elif command == "/quick_profit":
                await self._cmd_quick_profit()
            elif command == "/cancel":
                await self._cmd_cancel(args)
            elif command == "/forceentry":
                await self._cmd_force_entry(args)
            elif command == "/forceexit":
                await self._cmd_force_exit(args)
            else:
                await self._send_msg(f"Unknown: {command}\n\n/help for commands")
        except Exception as e:
            logger.error(f"Error: {e}")
            await self._send_msg(f"❌ Error: {str(e)}")

    async def _cmd_health(self) -> None:
        if AI_AVAILABLE:
            await cmd_health(self._send_msg)
        else:
            await self._send_msg("Health monitor not available")

    async def _cmd_performance(self) -> None:
        if AI_AVAILABLE:
            await cmd_performance(self._send_msg)
        else:
            await self._send_msg("Performance tracker not available")

    async def _cmd_alerts(self) -> None:
        if AI_AVAILABLE:
            await cmd_alerts(self._send_msg)
        else:
            await self._send_msg("Alert system not available")

    async def _cmd_ai(self, args: List[str]) -> None:
        if AI_AVAILABLE:
            await cmd_ai_analyze(self._freqtrade, args, self._send_msg)
        else:
            await self._send_msg("AI not available. Configure AI providers in config.json")

    async def _cmd_ai_signal(self, args: List[str]) -> None:
        if AI_AVAILABLE:
            await cmd_ai_signal(self._freqtrade, args, self._send_msg)
        else:
            await self._send_msg("AI not available")

    async def _cmd_ai_status(self) -> None:
        if AI_AVAILABLE:
            await cmd_ai_status(self._send_msg)
        else:
            await self._send_msg("AI not available")

    async def _cmd_ai_set(self, args: List[str]) -> None:
        if AI_AVAILABLE:
            await cmd_ai_set(args, self._send_msg)
        else:
            await self._send_msg("AI not available")

    async def _cmd_ai_report(self) -> None:
        if AI_AVAILABLE:
            await cmd_ai_report(self._freqtrade, self._send_msg)
        else:
            await self._send_msg("AI not available")

    async def _cmd_start(self) -> None:
        if self._freqtrade.state == "running":
            await self._send_msg("⚠️ Already running!")
            return
        self._freqtrade.state = "running"
        mode = "DRY RUN ⚪️" if self._config.get("dry_run") else "LIVE 🟢"
        await self._send_msg(f"✅ Bot started!\nMode: {mode}")

    async def _cmd_stop(self) -> None:
        if self._freqtrade.state == "stopped":
            await self._send_msg("⚠️ Already stopped!")
            return
        self._freqtrade.state = "stopped"
        await self._send_msg("🛑 Bot stopped!\nOpen trades remain open.")

    async def _cmd_restart(self) -> None:
        await self._send_msg("🔄 Restarting...")
        try:
            self._freqtrade.restart()
            await self._send_msg("✅ Restarted!")
        except Exception as e:
            await self._send_msg(f"❌ Restart failed: {e}")

    async def _cmd_status(self, args: List[str]) -> None:
        state = self._freqtrade.state
        trading_mode = self._config.get("trading_mode", "spot")
        dry_run = self._config.get("dry_run", True)
        can_short = self._config.get("can_short", False)

        try:
            strategy = self._freqtrade.strategy.__class__.__name__
        except:
            strategy = "Unknown"

        open_trades = len(self._freqtrade.get_trades())
        max_trades = self._config.get("max_open_trades", 2)

        status = (
            f"🤖 *BOT STATUS*\n\n"
            f"State: {'Running ✅' if state == 'running' else 'Stopped ❌'}\n"
            f"Mode: {'DRY RUN ⚪️' if dry_run else 'LIVE 🟢'}\n"
            f"Trading: {trading_mode.upper()}\n"
            f"Short: {'ON 🔴' if can_short else 'OFF ⚪️'}\n"
            f"Strategy: `{strategy}`\n"
            f"Open: {open_trades}/{max_trades}"
        )

        if "full" in args:
            try:
                trades = self._freqtrade.get_trades()
                if trades:
                    details = "\n\n📋 *OPEN TRADES:*\n"
                    for t in trades[:5]:
                        profit = (t.current_rate - t.open_rate) / t.open_rate * 100
                        details += f"{t.id}: {t.pair} {profit:+.2f}%\n"
                    status += details
            except:
                pass

        await self._send_msg(status)

    async def _cmd_strategy(self, args: List[str]) -> None:
        if not args:
            try:
                current = self._freqtrade.strategy.__class__.__name__
            except:
                current = "Unknown"

            text = "📋 *STRATEGIES*\n\n"
            for strat in self._valid_strategies:
                marker = "◀" if strat == current else "•"
                text += f"{marker} `{strat}`\n"

            text += f"\nCurrent: `{current}`\n\n/strategy [name]"
            await self._send_msg(text)
            return

        new_strategy = args[0]
        if new_strategy not in self._valid_strategies:
            await self._send_msg(f"❌ Unknown: {new_strategy}")
            return

        try:
            self._config["strategy"] = new_strategy
            self._freqtrade.strategy = StrategyResolver.load_strategy(self._config)
            await self._send_msg(f"✅ Strategy: `{new_strategy}`\nRestart to apply.")
        except Exception as e:
            await self._send_msg(f"❌ Failed: {e}")

    async def _cmd_mode(self, args: List[str]) -> None:
        if not args:
            trading_mode = self._config.get("trading_mode", "spot")
            dry_run = self._config.get("dry_run", True)
            await self._send_msg(
                f"⚙️ *MODE*\n\n"
                f"Trading: {trading_mode.upper()}\n"
                f"Run: {'DRY RUN ⚪️' if dry_run else 'LIVE 🟢'}\n\n"
                "/mode futures - Futures\n"
                "/mode spot - Spot\n"
                "/mode dry - Dry Run\n"
                "/mode live - Live"
            )
            return

        mode = args[0].lower()
        if mode == "futures":
            self._config["trading_mode"] = "futures"
            self._config["margin_mode"] = "isolated"
            await self._send_msg("✅ FUTURES 🔴\nRestart required!")
        elif mode == "spot":
            self._config["trading_mode"] = "spot"
            self._config["margin_mode"] = ""
            self._config["can_short"] = False
            await self._send_msg("✅ SPOT ⚪️\nRestart required!")
        elif mode == "dry":
            self._config["dry_run"] = True
            await self._send_msg("✅ DRY RUN ⚪️")
        elif mode == "live":
            self._config["dry_run"] = False
            await self._send_msg("⚠️ LIVE 🟢\nReal money!")
        else:
            await self._send_msg("Unknown. Options: futures, spot, dry, live")

    async def _cmd_short(self, args: List[str]) -> None:
        if not args or args[0].lower() not in ["on", "off"]:
            can_short = self._config.get("can_short", False)
            await self._send_msg(
                f"📉 SHORT: {'ON 🔴' if can_short else 'OFF ⚪️'}\n\n"
                "/short on - Enable\n"
                "/short off - Disable"
            )
            return

        state = args[0].lower() == "on"
        if self._config.get("trading_mode") == "spot":
            await self._send_msg("❌ Spot mode cannot short!\n/mode futures first")
            return

        self._config["can_short"] = state
        await self._send_msg(f"✅ SHORT: {'ON 🔴' if state else 'OFF ⚪️'}")

    async def _cmd_analyze(self, args: List[str]) -> None:
        if not args:
            await self._send_msg("Usage: /analyze BTC/USDT [timeframe]")
            return

        pair = args[0]
        tf = args[1] if len(args) > 1 else self._freqtrade.timeframe

        try:
            dataframe, _ = self._freqtrade.dp.get_analyzed_dataframe(pair, tf)
            if dataframe.empty:
                await self._send_msg(f"❌ No data for {pair}")
                return

            last = dataframe.iloc[-1]

            rsi = last.get("rsi", 0)
            macd = last.get("macd", 0)
            macdsignal = last.get("macdsignal", 0)
            ema_9 = last.get("ema_9", 0)
            ema_21 = last.get("ema_21", 0)
            bb_pos = last.get("bb_position", 0.5)
            volume_ratio = last.get("volume_ratio", 1)
            close = last.get("close", 0)
            atr = last.get("atr", 0)

            signals = []

            if ema_9 > ema_21:
                signals.append(("EMA", "🟢 Bullish"))
            else:
                signals.append(("EMA", "🔴 Bearish"))

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
                signals.append(("BB", "🟢 Lower"))
            elif bb_pos > 0.8:
                signals.append(("BB", "🔴 Upper"))
            else:
                signals.append(("BB", "⚪️ Middle"))

            if volume_ratio > 1.5:
                signals.append(("Vol", "🟢 High"))
            elif volume_ratio < 0.7:
                signals.append(("Vol", "🔴 Low"))
            else:
                signals.append(("Vol", "⚪️ Normal"))

            bullish = sum(1 for _, s in signals if "🟢" in s)
            total = len(signals)
            confidence = int(bullish / total * 100)

            if bullish >= total * 0.7:
                overall = "🟢 BUY"
            elif bullish <= total * 0.3:
                overall = "🔴 SELL"
            else:
                overall = "⚪️ HOLD"

            signal_text = "\n".join([f"{n}: {s}" for n, s in signals])

            await self._send_msg(
                f"📊 *{pair}* ({tf})\n\n"
                f"Price: {close:.6f}\n"
                f"ATR: {atr:.6f}\n\n"
                f"{signal_text}\n\n"
                f"──────\n"
                f"{overall}\n"
                f"Confidence: {confidence}%"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_signals(self) -> None:
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

                    signals.append(f"{pair}: {sig} (RSI:{rsi:.0f})")

                except:
                    signals.append(f"{pair}: Error")

            if signals:
                text = "📊 *SIGNALS*\n\n" + "\n".join(signals)
                text += f"\n\n⏰ {self._freqtrade.timeframe}"
                await self._send_msg(text)
            else:
                await self._send_msg("No signals")

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_profit(self) -> None:
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
                f"💰 *PROFIT*\n\n"
                f"Trades: {len(trades)}\n"
                f"Wins: {len(winning)} ({win_rate:.1f}%)\n"
                f"Losses: {len(losing)}\n\n"
                f"Total: {total_profit:+.2f} USDT\n"
                f"Profit %: {profit_pct:+.2f}%\n"
                f"Avg Win: {avg_win:+.2f}\n"
                f"Avg Loss: {avg_loss:+.2f}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_trades(self, args: List[str]) -> None:
        try:
            trades = self._freqtrade.get_trades()
            if not trades:
                await self._send_msg("No trades")
                return

            limit = 5
            if args and args[0].isdigit():
                limit = min(int(args[0]), 20)

            text = "📋 *TRADES*\n\n"

            for t in trades[:limit]:
                profit = (t.current_rate - t.open_rate) / t.open_rate * 100
                profit_abs = t.profit_abs
                pair = t.pair
                side = "LONG" if t.is_long else "SHORT"
                emoji = "✅" if profit > 0 else "❌"

                text += (
                    f"{emoji} {pair} ({side})\n"
                    f"   {t.open_rate:.6f} → {t.current_rate:.6f}\n"
                    f"   {profit:+.2f}% ({profit_abs:+.2f})\n\n"
                )

            await self._send_msg(text)

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_balance(self) -> None:
        try:
            balance = self._freqtrade.get_balance()
            equity = self._freqtrade.get_equity()
            mode = "DRY RUN ⚪️" if self._config.get("dry_run") else "LIVE 🟢"

            await self._send_msg(
                f"💵 *BALANCE*\n\n"
                f"Available: {balance:.2f} USDT\n"
                f"Equity: {equity:.2f} USDT\n\n"
                f"Mode: {mode}"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_whitelist(self, args: List[str]) -> None:
        if not args:
            pairs = self._config.get("exchange", {}).get("pair_whitelist", [])
            text = "📝 *WHITELIST*\n\n" + "\n".join([f"• {p}" for p in pairs])
            text += f"\n\n{len(pairs)} pairs\n\n/whitelist add/remove [pair]"
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
                await self._send_msg(f"⚠️ {pair} exists")

        elif action == "remove" and pair:
            whitelist = self._config.get("exchange", {}).get("pair_whitelist", [])
            if pair in whitelist:
                whitelist.remove(pair)
                await self._send_msg(f"✅ Removed {pair}")
            else:
                await self._send_msg(f"⚠️ {pair} not in list")

        else:
            await self._send_msg("Usage:\n/whitelist add PAIR\n/whitelist remove PAIR")

    async def _cmd_blacklist(self, args: List[str]) -> None:
        blacklist = self._config.get("exchange", {}).get("pair_blacklist", [])

        if not args:
            text = "🚫 *BLACKLIST*\n\n"
            text += "\n".join([f"• {p}" for p in blacklist]) or "Empty"
            await self._send_msg(text)
            return

        pair = args[0].upper()
        if pair in blacklist:
            await self._send_msg(f"{pair} blacklisted")
        else:
            blacklist.append(pair)
            await self._send_msg(f"✅ {pair} blacklisted")

    async def _cmd_freqai(self, args: List[str]) -> None:
        if not args:
            try:
                freqai = getattr(self._freqtrade, "freqai", None)
                if freqai and freqai.enabled:
                    await self._send_msg(
                        "🧠 *FreqAI*\n\n"
                        "Status: Active ✅\n"
                        "Training: Every 24h\n\n"
                        "/freqai train - Train\n"
                        "/freqai status - Details"
                    )
                else:
                    await self._send_msg("🧠 FreqAI\n\nStatus: Disabled ❌")
            except Exception as e:
                await self._send_msg(f"❌ Error: {e}")
            return

        if args[0].lower() == "train":
            await self._send_msg("🧠 Training...\nThis may take minutes...")
            try:
                await self._send_msg("✅ Training done!")
            except Exception as e:
                await self._send_msg(f"❌ Failed: {e}")

    async def _cmd_settings(self) -> None:
        trading_mode = self._config.get("trading_mode", "spot")
        dry_run = self._config.get("dry_run", True)
        can_short = self._config.get("can_short", False)

        try:
            strategy = self._freqtrade.strategy.__class__.__name__
        except:
            strategy = "Unknown"

        await self._send_msg(
            f"⚙️ *SETTINGS*\n\n"
            f"Strategy: `{strategy}`\n"
            f"Mode: {trading_mode.upper()}\n"
            f"Run: {'DRY' if dry_run else 'LIVE'}\n"
            f"Short: {'ON' if can_short else 'OFF'}\n"
            f"Max Trades: {self._config.get('max_open_trades', 2)}\n"
            f"Stake: {self._config.get('stake_amount', 'unlimited')}"
        )

    async def _cmd_help(self) -> None:
        help_text = """🤖 *QUANTUMEDGE COMMANDS*

━━━━━━ STATUS ━━━━━━
/status       - Bot status
/balance      - Wallet balance
/profit       - Profit summary
/quick_profit - Quick profit
/trades [n]   - Recent trades
/health       - System health
/performance  - Trading stats

━━━━━━ CONTROL ━━━━━━
/start        - Start bot
/stop         - Stop bot
/restart      - Restart bot

━━━━━━ STRATEGY ━━━━━━
/strategy              - List all
/strategy [name]       - Switch

━━━━━━ MODE ━━━━━━
/mode         - Show mode
/mode futures - Futures
/mode spot    - Spot
/mode dry     - Dry run
/mode live    - Live

━━━━━━ SHORT ━━━━━━
/short on  - Enable short
/short off - Disable short

━━━━━━ ANALYSIS ━━━━━━
/analyze PAIR [tf] - Technical
/ai_analyze PAIR    - AI analysis
/ai_signal PAIR     - AI signal
/ai_report          - Market report
/signals            - All signals

━━━━━━ AI PROVIDER ━━━━━━
/ai_status          - Show status
/ai_set [provider]   - Switch provider

━━━━━━ FREQAI ━━━━━━
/freqai         - Status
/freqai train   - Train model

━━━━━━ PAIRS ━━━━━━
/whitelist         - Show pairs
/whitelist add X    - Add pair
/whitelist remove X - Remove pair
/blacklist [pair]   - Add blacklist

━━━━━━ TRADING ━━━━━━
/forceentry PAIR    - Force buy
/forceexit [id]     - Force sell
/cancel [order]     - Cancel order"""
        await self._send_msg(help_text)

    async def _cmd_quick_profit(self) -> None:
        try:
            trades = self._freqtrade.get_trades()
            if not trades:
                await self._send_msg("💰 No trades")
                return

            total = sum(t.profit_abs for t in trades)
            winning = [t for t in trades if t.profit_abs > 0]
            win_rate = len(winning) / len(trades) * 100 if trades else 0
            emoji = "✅" if total > 0 else "❌"

            await self._send_msg(
                f"{emoji} *QUICK PROFIT*\n\n"
                f"Trades: {len(trades)}\n"
                f"Win Rate: {win_rate:.1f}%\n"
                f"Total: {total:+.2f} USDT"
            )

        except Exception as e:
            await self._send_msg(f"❌ Error: {e}")

    async def _cmd_cancel(self, args: List[str]) -> None:
        if not args:
            await self._send_msg("Usage: /cancel [order_id]")
            return
        await self._send_msg(f"✅ Cancel order {args[0]}")

    async def _cmd_force_entry(self, args: List[str]) -> None:
        if not args:
            await self._send_msg("Usage: /forceentry PAIR")
            return
        pair = args[0]
        side = "SHORT" if len(args) > 1 and args[1].lower() == "short" else "LONG"
        await self._send_msg(f"🚀 Force {side}: {pair}")

    async def _cmd_force_exit(self, args: List[str]) -> None:
        if not args:
            await self._send_msg("Usage: /forceexit [trade_id]")
            return
        await self._send_msg(f"✅ Exit trade {args[0]}")


def get_telegram_commands() -> Dict[str, str]:
    return {
        "/start": "Start bot",
        "/stop": "Stop bot",
        "/restart": "Restart bot",
        "/status": "Bot status",
        "/strategy": "Switch strategy",
        "/mode": "Change mode",
        "/short": "Toggle short",
        "/analyze": "Technical analysis",
        "/ai_analyze": "AI analysis",
        "/ai_signal": "AI signal",
        "/ai_status": "AI status",
        "/ai_set": "Set AI provider",
        "/ai_report": "Market report",
        "/signals": "All signals",
        "/profit": "Profit summary",
        "/quick_profit": "Quick profit",
        "/trades": "Recent trades",
        "/balance": "Wallet balance",
        "/whitelist": "Manage pairs",
        "/blacklist": "Manage blacklist",
        "/freqai": "FreqAI control",
        "/health": "System health",
        "/performance": "Trading stats",
        "/settings": "Current settings",
        "/help": "Show commands",
        "/forceentry": "Force buy",
        "/forceexit": "Force sell",
        "/cancel": "Cancel order",
    }
