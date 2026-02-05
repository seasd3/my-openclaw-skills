---
name: china-finance
description: 国内股市基金理财数据查询工具，使用AKShare和Baostock免费接口获取A股、基金、指数实时行情和历史数据。
metadata:
  emoji: 📈
  requires:
    python_packages: ["akshare", "baostock", "pandas", "requests"]
---

# China Finance

国内金融数据查询工具，完全免费，无需注册。

## 功能

- 📊 A股实时行情 (AKShare)
- 📈 指数行情（上证、深证、创业板）(AKShare)
- 🏦 基金净值查询 (新浪财经 + 东方财富)
- 📉 历史K线数据 (Baostock)
- 🔄 资金流向 (AKShare)

## 使用方法

### 基金净值查询（推荐稳定版）

```bash
# 稳定版 - 新浪财经接口（推荐）
python scripts/my_funds_stable.py
python scripts/fund_nav_stable.py --code 017193

# 新浪财经接口
python scripts/fund_nav_sina.py --code 017193
python scripts/my_funds_sina.py

# 天天基金网接口
python scripts/fund_nav_eastmoney.py --code 017193

# AKShare 接口（可能不稳定）
python scripts/fund_nav.py --code 017193
python scripts/my_funds.py
```

### A股实时行情
```bash
python scripts/stock_quote.py
```

### 指数行情
```bash
python scripts/index_quote.py
```

### 历史数据
```bash
python scripts/history.py --code 000001 --days 30
```

## 数据源对比

| 接口 | 稳定性 | 实时性 | 推荐场景 |
|------|--------|--------|---------|
| **新浪财经** | ✅ 高 | ✅ 高 | **首选** |
| 天天基金网 | ⚠️ 中 | ✅ 高 | 备用 |
| AKShare | ⚠️ 不稳 | ⚠️ 有时延迟 | 备用 |

## 脚本说明

| 脚本 | 接口 | 特点 |
|------|------|------|
| `my_funds_stable.py` | 新浪财经 | **推荐，稳定** |
| `fund_nav_stable.py` | 新浪财经 | 单只基金查询 |
| `my_funds_sina.py` | 新浪财经 | 备用 |
| `fund_nav_sina.py` | 新浪财经 | 单只基金查询 |
| `my_funds.py` | AKShare | 可能不稳定 |
| `fund_nav.py` | AKShare | 可能不稳定 |

## 注意

- 数据仅供学习参考，不构成投资建议
- 基金净值分为**估算净值**（盘中）和**真实净值**（21:00 后）
- 建议以支付宝/天天基金网页数据为准
