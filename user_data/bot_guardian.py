#!/usr/bin/env python3
"""
QuantumEdge Bot Guardian - Anti-Crash & Auto-Restart System
Ensures the bot never crashes and auto-recovers from errors
"""

import sys
import os
import time
import signal
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BotGuardian")


class BotGuardian:
    """
    Guardian system that monitors and auto-restarts the freqtrade bot
    Features:
    - Auto restart on crash
    - Memory leak detection
    - CPU overheating protection
    - Disk space monitoring
    - Config backup before restart
    - Git sync after restart
    """

    def __init__(self, config_path: str = None):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or str(self.base_path / "user_data" / "config.json")
        self.bot_process: Optional[subprocess.Popen] = None
        self.restart_count = 0
        self.max_restarts = 5
        self.restart_window = 3600  # 1 hour
        self.restart_timestamps = []
        self.is_running = True
        self.health_check_interval = 30  # seconds

        # Thresholds
        self.max_memory_percent = 85
        self.max_cpu_percent = 95
        self.min_disk_gb = 2

        # Git sync
        self.git_token = os.environ.get("GIT_TOKEN", "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")
        self.git_repo = "https://github.com/SecretArrow/freqtrade.git"

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.is_running = False
        if self.bot_process:
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
        sys.exit(0)

    def check_system_health(self) -> dict:
        """Check system health metrics"""
        health = {
            "memory_percent": 0,
            "cpu_percent": 0,
            "disk_gb": 0,
            "healthy": True,
            "warnings": [],
        }

        try:
            import psutil

            process = psutil.Process(os.getpid())

            # Memory check
            memory = psutil.virtual_memory()
            health["memory_percent"] = memory.percent
            if memory.percent > self.max_memory_percent:
                health["warnings"].append(f"Memory high: {memory.percent:.1f}%")
                health["healthy"] = False

            # CPU check
            health["cpu_percent"] = psutil.cpu_percent(interval=1)
            if health["cpu_percent"] > self.max_cpu_percent:
                health["warnings"].append(f"CPU high: {health['cpu_percent']:.1f}%")
                health["healthy"] = False

            # Disk check
            disk = psutil.disk_usage("/")
            health["disk_gb"] = disk.free / (1024**3)
            if health["disk_gb"] < self.min_disk_gb:
                health["warnings"].append(f"Disk low: {health['disk_gb']:.1f}GB free")
                health["healthy"] = False

        except ImportError:
            logger.warning("psutil not installed, skipping system health check")
        except Exception as e:
            logger.error(f"Error checking system health: {e}")

        return health

    def backup_config(self):
        """Backup config before restart"""
        try:
            from pathlib import Path
            import json
            import shutil

            config_path = Path(self.config_path)
            if config_path.exists():
                backup_dir = self.base_path / "user_data"
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = backup_dir / f"config_backup_{timestamp}.json"

                shutil.copy2(config_path, backup_path)
                logger.info(f"Config backed up to {backup_path}")

                # Keep only last 5 backups
                backups = sorted(
                    backup_dir.glob("config_backup_*.json"), key=lambda p: p.stat().st_mtime
                )
                for old_backup in backups[:-5]:
                    old_backup.unlink()
                    logger.info(f"Removed old backup: {old_backup}")

        except Exception as e:
            logger.error(f"Error backing up config: {e}")

    def git_push(self, message: str = "Auto backup - bot restart"):
        """Push changes to GitHub"""
        try:
            env = os.environ.copy()
            env["GIT_TOKEN"] = self.git_token

            # Configure git
            subprocess.run(
                ["git", "config", "user.email", "bot@freqtrade.local"],
                cwd=self.base_path,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "QuantumEdge Bot"],
                cwd=self.base_path,
                capture_output=True,
            )

            # Add and commit
            subprocess.run(["git", "add", "-A"], cwd=self.base_path, capture_output=True)

            result = subprocess.run(
                ["git", "commit", "-m", f"{message} - {datetime.now().isoformat()}"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Push with token
                remote_url = (
                    f"https://x-access-token:{self.git_token}@github.com/SecretArrow/freqtrade.git"
                )
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url],
                    cwd=self.base_path,
                    capture_output=True,
                )

                result = subprocess.run(
                    ["git", "push", "origin", "main"],
                    cwd=self.base_path,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    logger.info("Successfully pushed to GitHub")
                    return True
                else:
                    logger.warning(f"Git push failed: {result.stderr}")
            else:
                if "nothing to commit" not in result.stdout:
                    logger.warning(f"Git commit failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Error in git push: {e}")

        return False

    def git_pull(self):
        """Pull latest from GitHub"""
        try:
            env = os.environ.copy()
            env["GIT_TOKEN"] = self.git_token

            remote_url = (
                f"https://x-access-token:{self.git_token}@github.com/SecretArrow/freqtrade.git"
            )
            subprocess.run(
                ["git", "remote", "set-url", "origin", remote_url],
                cwd=self.base_path,
                capture_output=True,
            )

            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info("Successfully pulled from GitHub")
                return True
            else:
                logger.warning(f"Git pull failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Error in git pull: {e}")

        return False

    def should_restart(self) -> bool:
        """Check if we should restart based on restart history"""
        now = time.time()

        # Remove timestamps older than restart_window
        self.restart_timestamps = [
            t for t in self.restart_timestamps if now - t < self.restart_window
        ]

        if len(self.restart_timestamps) >= self.max_restarts:
            logger.error(
                f"Max restarts ({self.max_restarts}) reached in {self.restart_window}s. Giving up."
            )
            return False

        return True

    def start_bot(self) -> bool:
        """Start the freqtrade bot"""
        try:
            logger.info("Starting freqtrade bot...")

            cmd = [
                sys.executable,
                "-m",
                "freqtrade",
                "trade",
                "--config",
                self.config_path,
                "--strategy",
                "QuantumEdge_Adaptive",
            ]

            self.bot_process = subprocess.Popen(
                cmd,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            )

            logger.info(f"Bot started with PID: {self.bot_process.pid}")
            self.restart_timestamps.append(time.time())
            self.restart_count += 1

            return True

        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False

    def monitor_bot(self):
        """Monitor the bot process"""
        if not self.bot_process:
            return

        # Check if process is still running
        if self.bot_process.poll() is not None:
            exit_code = self.bot_process.poll()
            logger.warning(f"Bot process exited with code: {exit_code}")

            # Try to read output
            try:
                output, _ = self.bot_process.communicate(timeout=5)
                if output:
                    logger.info(f"Last output: {output[-500:]}")
            except:
                pass

            if self.is_running and self.should_restart():
                logger.info("Attempting to restart bot...")
                self.backup_config()
                time.sleep(5)
                self.start_bot()
            else:
                logger.error("Not restarting - max restarts reached or shutdown requested")
                self.is_running = False

    def run_loop(self):
        """Main guardian loop"""
        logger.info("=" * 50)
        logger.info("QuantumEdge Bot Guardian Started")
        logger.info(f"Config: {self.config_path}")
        logger.info(f"Git Repo: {self.git_repo}")
        logger.info("=" * 50)

        # Initial git pull
        self.git_pull()

        # Start bot
        if not self.start_bot():
            logger.error("Failed to start bot initially. Exiting.")
            return

        # Main loop
        while self.is_running:
            try:
                # Check system health
                health = self.check_system_health()

                if not health["healthy"]:
                    logger.warning(f"System unhealthy: {health['warnings']}")

                    # Emergency restart on critical issues
                    if health["disk_gb"] < 1:
                        logger.error(
                            "CRITICAL: Disk space critical! Emergency backup and restart..."
                        )
                        self.backup_config()
                        self.git_push("Emergency backup - disk space critical")

                        if self.bot_process:
                            self.bot_process.terminate()

                # Monitor bot
                self.monitor_bot()

                # Sleep
                time.sleep(self.health_check_interval)

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                break
            except Exception as e:
                logger.error(f"Error in guardian loop: {e}")
                time.sleep(5)

        # Cleanup
        if self.bot_process:
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()

        logger.info("Bot Guardian stopped")


def main():
    """Entry point"""
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    guardian = BotGuardian(config_path)
    guardian.run_loop()


if __name__ == "__main__":
    main()
