# China Finance 📈

国内股市基金理财数据查询工具，完全免费，无需注册。

## 功能特点

- ✅ **完全免费** - 使用 AKShare 和 Baostock 开源接口
- ✅ **无需注册** - 安装即用，无需 API Key
- ✅ **数据全面** - A股、基金、指数、历史数据
- ✅ **实时更新** - 交易日实时行情

## 安装

```bash
# 安装依赖
pip install akshare baostock pandas

# 或运行
python setup.py
```

## 使用方法

### 1. A股实时行情
```bash
python scripts/stock_quote.py
```
显示：
- 涨幅榜 TOP 10
- 跌幅榜 TOP 10
- 主要指数行情

### 2. 基金净值查询
```bash
python scripts/fund_nav.py --code 000001
```

### 3. 指数行情
```bash
python scripts/index_quote.py
```
显示主要指数实时行情。

### 4. 历史数据
```bash
# 查询最近30天
python scripts/history.py --code 000001 --days 30
```

### 5. 我的持仓分析
```bash
python scripts/my_funds.py
```
自动分析你的基金组合（已预置你的5只基金）。

## 数据源

| 数据源 | 用途 | 特点 |
|--------|------|------|
| AKShare | 实时行情、基金数据 | 数据实时，来源于东方财富等 |
| Baostock | 历史数据 | 数据完整，更新T+1 |

## 注意

- 数据仅供学习参考，不构成投资建议
- 交易日 9:30-15:00 可获取实时数据
- 非交易时间可能返回空数据或历史数据

## 更新日志

- 2026-02-04: 初始版本，支持基本行情查询
