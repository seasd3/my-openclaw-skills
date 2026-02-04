---
name: china-finance
description: 国内股市基金理财数据查询工具，使用AKShare和Baostock免费接口获取A股、基金、指数实时行情和历史数据。
metadata:
  emoji: 📈
  requires:
    python_packages: ["akshare", "baostock", "pandas"]
---

# China Finance

国内金融数据查询工具，完全免费，无需注册。

## 功能

- 📊 A股实时行情
- 📈 指数行情（上证、深证、创业板）
- 🏦 基金净值查询
- 📉 历史K线数据
- 🔄 资金流向

## 使用方法

```bash
# A股实时行情
python scripts/stock_quote.py

# 基金净值
python scripts/fund_nav.py --code 000001

# 指数行情
python scripts/index_quote.py

# 历史数据
python scripts/history.py --code 000001 --days 30
```

## 数据源

- **AKShare**: 实时行情、基金数据
- **Baostock**: 历史数据、财务数据

## 注意

数据仅供学习参考，不构成投资建议。
