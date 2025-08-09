#!/usr/bin/env python3
import subprocess
import os

def run(cmd):
    print(f"→ {cmd}")
    subprocess.run(cmd, shell=True, check=False)

print("🔄 Updating system...")
run("sudo apt update && sudo apt upgrade -y")

print("🧹 Cleaning up unused packages...")
run("sudo apt autoremove --purge -y")
run("sudo apt clean")

print("🗑️ Clearing memory caches...")
run("sudo sync")
run("echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null")

print("💾 Reducing swappiness...")
sysctl_conf = "/etc/sysctl.conf"
with open(sysctl_conf, "r") as f:
    config = f.read()
if "vm.swappiness" not in config:
    run('echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf > /dev/null')
run("sudo sysctl -p > /dev/null")

print("⚡ Trimming SSD (if present)...")
run("sudo fstrim -v /")

print("🎯 Setting CPU governor to performance...")
if subprocess.run("command -v cpufreq-set", shell=True).returncode != 0:
    run("sudo apt install cpufrequtils -y")
run("sudo cpufreq-set -r -g performance")

print("🚀 Installing & enabling preload...")
run("sudo apt install preload -y")
run("sudo systemctl enable preload --now")

print("✅ fastlinux complete!")
