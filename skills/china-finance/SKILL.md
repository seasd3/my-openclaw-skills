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
- 🏦 基金净值查询 (AKShare + 新浪财经备用)
- 📉 历史K线数据 (Baostock)
- 🔄 资金流向 (AKShare)

## 使用方法

### A股实时行情
```bash
python scripts/stock_quote.py
```

### 基金净值查询
```bash
# AKShare 接口（默认）
python scripts/fund_nav.py --code 017193

# 新浪财经接口（备用，更稳定）
python scripts/fund_nav_sina.py --code 017193
```

### 持仓基金分析
```bash
# AKShare 接口
python scripts/my_funds.py

# 新浪财经接口（推荐，备用方案）
python scripts/my_funds_sina.py
```

### 指数行情
```bash
python scripts/index_quote.py
```

### 历史数据
```bash
python scripts/history.py --code 000001 --days 30
```

## 数据源

| 接口 | 用途 | 特点 |
|------|------|------|
| **AKShare** | 实时行情、基金数据 | 数据丰富，偶有延迟 |
| **新浪财经** | 基金净值（备用） | 更稳定，完全免费 |
| **Baostock** | 历史K线 | 数据完整，更新及时 |

## 备用方案

当 AKShare 不稳定时，使用新浪财经接口：

```bash
# 查询单只基金
python scripts/fund_nav_sina.py --code 017193

# 批量分析持仓
python scripts/my_funds_sina.py
```

## 注意

- 数据仅供学习参考，不构成投资建议
- 新浪财经接口无需 API Key，完全免费
- 建议两个接口交替使用，确保数据获取成功
