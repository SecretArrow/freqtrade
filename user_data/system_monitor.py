"""
QuantumEdge System Monitor - Health & Performance Monitoring
Features:
- CPU, RAM, Disk monitoring
- Bot performance tracking
- Trading statistics
- Auto alerts on issues
"""

import os
import psutil
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger("SystemMonitor")


class SystemMonitor:
    """
    Monitor system resources and bot performance
    Send alerts via Telegram when issues detected
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.alerts: List[Dict] = []
        self.max_alerts = 100

        # Thresholds
        self.memory_threshold = 80  # %
        self.cpu_threshold = 90  # %
        self.disk_threshold = 85  # %
        self.trade_loss_threshold = -5  # %

        # Alert cooldowns
        self.alert_cooldowns: Dict[str, datetime] = {}
        self.alert_cooldown_minutes = 60

    def get_system_stats(self) -> Dict[str, Any]:
        """Get current system statistics"""
        try:
            # Memory
            memory = psutil.virtual_memory()

            # CPU
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_avg = sum(cpu_percent) / len(cpu_percent)

            # Disk
            disk = psutil.disk_usage("/")

            # Network
            net = psutil.net_io_counters()

            # Process info
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / (1024 * 1024)  # MB

            return {
                "memory": {
                    "total_gb": memory.total / (1024**3),
                    "available_gb": memory.available / (1024**3),
                    "used_gb": memory.used / (1024**3),
                    "percent": memory.percent,
                },
                "cpu": {
                    "count": psutil.cpu_count(),
                    "percent_avg": cpu_avg,
                    "percent_per_core": cpu_percent,
                },
                "disk": {
                    "total_gb": disk.total / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "percent": disk.percent,
                },
                "network": {"bytes_sent": net.bytes_sent, "bytes_recv": net.bytes_recv},
                "process": {
                    "memory_mb": process_memory,
                    "threads": process.num_threads(),
                    "cpu_percent": process.cpu_percent(interval=0.1),
                },
                "uptime": (datetime.now() - self.start_time).total_seconds(),
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}

    def check_alerts(self) -> List[str]:
        """Check for alert conditions"""
        alerts = []
        stats = self.get_system_stats()

        if not stats:
            return alerts

        # Memory check
        mem_pct = stats.get("memory", {}).get("percent", 0)
        if mem_pct > self.memory_threshold:
            alert_key = "memory_high"
            if self._can_send_alert(alert_key):
                alerts.append(f"⚠️ Memory usage HIGH: {mem_pct:.1f}%")
                self._record_alert(alert_key, alerts[-1])

        # CPU check
        cpu_pct = stats.get("cpu", {}).get("percent_avg", 0)
        if cpu_pct > self.cpu_threshold:
            alert_key = "cpu_high"
            if self._can_send_alert(alert_key):
                alerts.append(f"⚠️ CPU usage HIGH: {cpu_pct:.1f}%")
                self._record_alert(alert_key, alerts[-1])

        # Disk check
        disk_pct = stats.get("disk", {}).get("percent", 0)
        disk_free = stats.get("disk", {}).get("free_gb", 0)
        if disk_pct > self.disk_threshold:
            alert_key = "disk_high"
            if self._can_send_alert(alert_key):
                alerts.append(f"⚠️ Disk usage HIGH: {disk_pct:.1f}% ({disk_free:.1f}GB free)")
                self._record_alert(alert_key, alerts[-1])

        if disk_free < 2:
            alert_key = "disk_critical"
            if self._can_send_alert(alert_key):
                alerts.append(f"🚨 CRITICAL: Disk space very low ({disk_free:.1f}GB)")
                self._record_alert(alert_key, alerts[-1])

        return alerts

    def _can_send_alert(self, key: str) -> bool:
        """Check if alert can be sent (cooldown)"""
        if key not in self.alert_cooldowns:
            return True

        last_alert = self.alert_cooldowns[key]
        if datetime.now() - last_alert > timedelta(minutes=self.alert_cooldown_minutes):
            return True

        return False

    def _record_alert(self, key: str, message: str):
        """Record an alert"""
        self.alert_cooldowns[key] = datetime.now()
        self.alerts.append({"time": datetime.now(), "key": key, "message": message})

        # Keep only recent alerts
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts :]

    def format_health_report(self, stats: Dict = None) -> str:
        """Format system health report for Telegram"""
        if stats is None:
            stats = self.get_system_stats()

        if not stats:
            return "❌ Could not get system stats"

        uptime = stats.get("uptime", 0)
        hours, remainder = divmod(int(uptime), 3600)
        minutes, _ = divmod(remainder, 60)

        # Memory bar
        mem_pct = stats.get("memory", {}).get("percent", 0)
        mem_bar = self._make_bar(mem_pct)

        # CPU bar
        cpu_pct = stats.get("cpu", {}).get("percent_avg", 0)
        cpu_bar = self._make_bar(cpu_pct)

        # Disk bar
        disk_pct = stats.get("disk", {}).get("percent", 0)
        disk_bar = self._make_bar(disk_pct)

        report = f"""🔧 *SYSTEM HEALTH*

⏱️ Uptime: {hours}h {minutes}m
🧠 Memory: {mem_bar} {mem_pct:.1f}%
💻 CPU: {cpu_bar} {cpu_pct:.1f}%
💾 Disk: {disk_bar} {disk_pct:.1f}%

📊 *PROCESS INFO*
Memory: {stats.get("process", {}).get("memory_mb", 0):.1f} MB
Threads: {stats.get("process", {}).get("threads", 0)}

🖥️ *SYSTEM*
CPU Cores: {stats.get("cpu", {}).get("count", 0)}
Total RAM: {stats.get("memory", {}).get("total_gb", 0):.1f} GB
Total Disk: {stats.get("disk", {}).get("total_gb", 0):.1f} GB
Free Disk: {stats.get("disk", {}).get("free_gb", 0):.1f} GB"""

        # Add recent alerts
        recent_alerts = [a for a in self.alerts if datetime.now() - a["time"] < timedelta(hours=1)]

        if recent_alerts:
            report += f"\n\n🚨 *RECENT ALERTS* ({len(recent_alerts)})"
            for alert in recent_alerts[-3:]:
                time_str = alert["time"].strftime("%H:%M")
                report += f"\n{time_str}: {alert['message']}"

        return report

    def _make_bar(self, percent: float, length: int = 10) -> str:
        """Make a visual bar"""
        filled = int(percent / 10)
        empty = length - filled

        if percent < 50:
            color = "🟢"
        elif percent < 80:
            color = "🟡"
        else:
            color = "🔴"

        return f"{color}{'█' * filled}{'░' * empty}"


class PerformanceTracker:
    """
    Track trading performance and generate reports
    """

    def __init__(self, trades_file: str = None):
        self.trades_file = trades_file or str(
            Path(__file__).parent / "user_data" / "backtest_results"
        )
        self.trades: List[Dict] = []

    def add_trade(self, trade: Dict):
        """Add a trade to tracking"""
        self.trades.append({"timestamp": datetime.now(), **trade})

    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.trades:
            return {
                "total_trades": 0,
                "win_rate": 0,
                "profit_total": 0,
                "avg_win": 0,
                "avg_loss": 0,
            }

        winning = [t for t in self.trades if t.get("profit_percent", 0) > 0]
        losing = [t for t in self.trades if t.get("profit_percent", 0) < 0]

        return {
            "total_trades": len(self.trades),
            "winning": len(winning),
            "losing": len(losing),
            "win_rate": len(winning) / len(self.trades) * 100 if self.trades else 0,
            "profit_total": sum(t.get("profit_percent", 0) for t in self.trades),
            "avg_win": sum(t.get("profit_percent", 0) for t in winning) / len(winning)
            if winning
            else 0,
            "avg_loss": sum(t.get("profit_percent", 0) for t in losing) / len(losing)
            if losing
            else 0,
            "best_trade": max((t.get("profit_percent", 0) for t in self.trades), default=0),
            "worst_trade": min((t.get("profit_percent", 0) for t in self.trades), default=0),
        }

    def format_performance_report(self) -> str:
        """Format performance report for Telegram"""
        summary = self.get_summary()

        if summary["total_trades"] == 0:
            return "📊 *PERFORMANCE*\n\nNo trades yet"

        # Win rate bar
        win_rate = summary["win_rate"]
        win_bar = self._make_bar(win_rate / 10, "🟢", "🔴")

        report = f"""📊 *PERFORMANCE REPORT*

📈 *Win Rate:*
{win_bar} {win_rate:.1f}%

📋 *Trade Stats:*
Total: {summary["total_trades"]}
Wins: {summary["winning"]} ✅
Losses: {summary["losing"]} ❌

💰 *Profit:*
Total: {summary["profit_total"]:+.2f}%
Avg Win: {summary["avg_win"]:+.2f}%
Avg Loss: {summary["avg_loss"]:+.2f}%

🏆 *Best:* {summary["best_trade"]:+.2f}%
💔 *Worst:* {summary["worst_trade"]:+.2f}%"""

        return report

    def _make_bar(self, percent: float, color_pos: str = "🟢", color_neg: str = "🔴") -> str:
        """Make a visual bar"""
        filled = int(percent / 10)
        empty = 10 - filled
        return f"{'█' * filled}{'░' * empty}"


# Singleton instances
_system_monitor: Optional[SystemMonitor] = None
_performance_tracker: Optional[PerformanceTracker] = None


def get_system_monitor() -> SystemMonitor:
    global _system_monitor
    if _system_monitor is None:
        _system_monitor = SystemMonitor()
    return _system_monitor


def get_performance_tracker() -> PerformanceTracker:
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker


# Telegram handlers
async def cmd_health(send_msg) -> None:
    """Handle /health command"""
    monitor = get_system_monitor()
    stats = monitor.get_system_stats()
    alerts = monitor.check_alerts()

    report = monitor.format_health_report(stats)

    if alerts:
        report += "\n\n" + "\n".join(alerts)

    await send_msg(report)


async def cmd_performance(send_msg) -> None:
    """Handle /performance command"""
    tracker = get_performance_tracker()
    await send_msg(tracker.format_performance_report())


async def cmd_alerts(send_msg) -> None:
    """Handle /alerts command"""
    monitor = get_system_monitor()

    if not monitor.alerts:
        await send_msg("✅ *No recent alerts*")
        return

    recent = [a for a in monitor.alerts if datetime.now() - a["time"] < timedelta(hours=24)]

    if not recent:
        await send_msg("✅ *No alerts in last 24h*")
        return

    text = f"🚨 *ALERTS ({len(recent)} in 24h)*\n\n"
    for alert in recent[-10:]:
        time_str = alert["time"].strftime("%m-%d %H:%M")
        text += f"{time_str}\n{alert['message']}\n\n"

    await send_msg(text)


if __name__ == "__main__":
    # Test
    monitor = SystemMonitor()
    print(monitor.format_health_report())
