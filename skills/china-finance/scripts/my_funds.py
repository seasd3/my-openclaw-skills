#!/usr/bin/env python3
"""持仓基金分析 - 分析你的基金组合"""

import akshare as ak
import sys

# 你的基金持仓
MY_FUNDS = {
    "017193": "天弘工业有色金属指数C",
    "161028": "富国中证新能源汽车指数A",
    "008888": "华夏国证半导体芯片ETF联接C",
    "398051": "中海环保新能源混合",
    "003834": "华夏能源革新股票A"
}

def analyze_fund(fund_code, fund_name):
    """分析单只基金"""
    try:
        # 获取基金净值
        df = ak.fund_em_open_fund_info(fund=fund_code, indicator="单位净值走势")
        
        if df.empty:
            return None
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        nav = float(latest['单位净值'])
        prev_nav = float(prev['单位净值'])
        change = nav - prev_nav
        change_pct = (change / prev_nav) * 100
        
        # 近7天
        week_df = df.tail(7)
        week_start = float(week_df.iloc[0]['单位净值'])
        week_change_pct = (nav - week_start) / week_start * 100
        
        return {
            'name': fund_name,
            'nav': nav,
            'change': change,
            'change_pct': change_pct,
            'week_change_pct': week_change_pct,
            'date': latest['净值日期']
        }
        
    except Exception as e:
        print(f"获取 {fund_code} 数据失败: {e}")
        return None

def main():
    print("=" * 70)
    print("我的基金持仓分析")
    print("=" * 70)
    print()
    
    total_change_pct = 0
    results = []
    
    print("【今日净值变动】")
    print(f"{'基金名称':<20} {'净值':<8} {'日涨跌':<10} {'周涨跌':<10}")
    print("-" * 70)
    
    for code, name in MY_FUNDS.items():
        result = analyze_fund(code, name)
        if result:
            results.append(result)
            print(f"{result['name']:<20} {result['nav']:<8.4f} "
                  f"{result['change_pct']:<+9.2f}% {result['week_change_pct']:<+9.2f}%")
            total_change_pct += result['change_pct']
    
    print()
    print("=" * 70)
    print(f"平均日涨跌幅: {total_change_pct/len(results):+.2f}%")
    print("=" * 70)
    print()
    
    print("【板块分析】")
    print("有色金属: 关注铜价走势和美元指数")
    print("新能源车: 关注销量数据和政策变化")
    print("半导体:   关注国产替代进展和库存周期")
    print("新能源:   关注光伏价格企稳和风电装机")
    print("能源革新: 关注储能需求和电网投资")
    print()
    
    print("【投资建议】")
    print("1. 短期关注两会政策对新能源和科技板块的影响")
    print("2. 有色金属受益于美元走弱，可持有")
    print("3. 半导体需等待库存周期拐点")
    print("4. 设置止盈止损: -15%止损 / +20%止盈")

if __name__ == "__main__":
    main()
