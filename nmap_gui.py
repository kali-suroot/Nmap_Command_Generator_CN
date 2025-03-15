#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nmap命令生成器 v1.0 - 单文件版
License:  CC BY-NC-SA License
"""

import tkinter as tk
from tkinter import ttk

def generate_nmap_command(params):
    """生成Nmap命令的核心函数"""
    command = ["nmap"]
    
    # 扫描类型处理
    scan_types = {
        "SYN扫描（快速）": "-sS",
        "全连接扫描": "-sT",
        "UDP扫描": "-sU"
    }
    command.append(scan_types.get(params["scan_type"], "-sS"))
    
    # 端口范围处理
    if params["port_range"] == "全端口 (1-65535)":
        command.append("-p-")
    elif params["port_range"] == "自定义..." and params["custom_ports"].strip():
        command.append(f"-p {params['custom_ports'].strip()}")
    
    # 高级选项处理
    if params["skip_ping"]: command.append("-Pn")
    if params["service_version"]: command.append("-sV")
    if params["aggressive"]: command.append("-A")
    
    # 加速级别处理
    timing_map = {
        "T0 (最慢)": "-T0", "T1": "-T1", "T2": "-T2",
        "T3 (默认)": "-T3", "T4": "-T4", "T5 (最快)": "-T5"
    }
    command.append(timing_map.get(params["timing"], "-T3"))
    
    # 目标处理和sudo权限
    command.append(params["target"].strip())
    if params["scan_type"] == "SYN扫描（快速）":
        command.insert(0, "sudo")
    
    return " ".join(command)

class NmapGeneratorApp:
    """主应用程序GUI"""
    def __init__(self, root):
        self.root = root
        self.root.title("Nmap命令生成器 v1.0")
        self.root.geometry("680x520")
        self._setup_ui()
    
    def _setup_ui(self):
        """界面布局"""
        # 目标输入
        ttk.Label(self.root, text="目标IP/域名：").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.target_entry = ttk.Entry(self.root, width=30)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # 扫描类型选择
        ttk.Label(self.root, text="扫描类型：").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.scan_type = ttk.Combobox(self.root, values=["SYN扫描（快速）", "全连接扫描", "UDP扫描"], state="readonly")
        self.scan_type.current(0)
        self.scan_type.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # 端口范围配置
        ttk.Label(self.root, text="端口范围：").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.port_range = ttk.Combobox(self.root, values=["常用端口 (默认)", "全端口 (1-65535)", "自定义..."])
        self.port_range.current(0)
        self.port_range.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.port_range.bind("<<ComboboxSelected>>", self._toggle_custom_port)
        self.custom_port_entry = ttk.Entry(self.root, width=20, state="disabled")
        self.custom_port_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # 高级选项
        options_frame = ttk.LabelFrame(self.root, text="高级选项")
        options_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.skip_ping = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="跳过Ping检测 (-Pn)", variable=self.skip_ping).grid(row=0, column=0, sticky="w")
        self.service_version = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="服务版本探测 (-sV)", variable=self.service_version).grid(row=0, column=1, sticky="w")
        self.aggressive = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="激进模式 (-A)", variable=self.aggressive).grid(row=0, column=2, sticky="w")

        # 加速级别
        ttk.Label(options_frame, text="加速级别：").grid(row=1, column=0, sticky="w")
        self.timing = ttk.Combobox(options_frame, values=["T0 (最慢)", "T1", "T2", "T3 (默认)", "T4", "T5 (最快)"], state="readonly")
        self.timing.current(3)
        self.timing.grid(row=1, column=1, sticky="ew")

        # 命令显示区
        ttk.Label(self.root, text="生成命令：").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.command_text = tk.Text(self.root, height=6, wrap="word", font=("Consolas", 10))
        self.command_text.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        
        # 生成按钮
        ttk.Button(self.root, text="生成命令", command=self._update_command).grid(row=6, column=0, columnspan=3, pady=10)

        # 布局配置
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(5, weight=1)

    def _toggle_custom_port(self, event):
        """切换自定义端口输入状态"""
        if self.port_range.get() == "自定义...":
            self.custom_port_entry.config(state="normal")
        else:
            self.custom_port_entry.config(state="disabled")
            self.custom_port_entry.delete(0, tk.END)

    def _update_command(self):
        """更新命令显示"""
        params = {
            "target": self.target_entry.get(),
            "scan_type": self.scan_type.get(),
            "port_range": self.port_range.get(),
            "custom_ports": self.custom_port_entry.get(),
            "skip_ping": self.skip_ping.get(),
            "service_version": self.service_version.get(),
            "aggressive": self.aggressive.get(),
            "timing": self.timing.get()
        }
        command = generate_nmap_command(params)
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(tk.END, command)

if __name__ == "__main__":
    root = tk.Tk()
    app = NmapGeneratorApp(root)
    root.mainloop()

"""
命令显示区加字体
 self.command_text = tk.Text(self.root, height=6, wrap="word", font=("Consolas", 10))
"""
