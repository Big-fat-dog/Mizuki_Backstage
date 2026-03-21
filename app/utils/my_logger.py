import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
LOG_DIR=Path("logs")
LOG_DIR.mkdir(exist_ok=True)
import colorlog

def setup_logger(name: str = "app") -> logging.Logger:
    """
    配置并返回一个 logger 实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 全局最低级别

    # 如果已经配置过 handler，直接返回（防止重复添加）
    if logger.handlers:
        return logger

    # --- 1. 定义格式 ---
    # 时间 | 级别 | 文件名:行号 | 消息
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(log_format, datefmt=date_format)

    # --- 2. 控制台处理器 (带颜色) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # 控制台可以看详细点

    # 尝试引入 colorlog 让控制台有颜色 (如果没有安装，就退化到普通文本)
    try:
        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt=date_format,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(color_formatter)
    except ImportError:
        # 没装 colorlog 就用普通格式
        console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # --- 3. 文件处理器 (按天切割) ---
    # 文件名：logs/app.log
    # 备份文件名：logs/app.log
    file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / f"{name}.log",
        when="midnight",  # 每天午夜切割
        interval=1,
        backupCount=7,  # 只保留最近 7 天的日志
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)  # 文件里只存 INFO 及以上
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# 创建一个默认的全局 logger
logger = setup_logger()