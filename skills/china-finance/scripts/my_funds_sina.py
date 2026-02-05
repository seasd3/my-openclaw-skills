#!/usr/bin/env python3
"""持仓基金分析 - 使用新浪财经接口（备用方案）

当 AKShare 不稳定时，使用新浪财经 API 获取基金净值。
"""

import requests
import json
import time

# 你的基金持仓
MY_FUNDS = {
    "017193": "天弘工业有色金属指数C",
    "161028": "富国中证新能源汽车指数A",
    "008888": "华夏国证半导体芯片ETF联接C",
    "398051": "中海环保新能源混合",
    "003834": "华夏能源革新股票A"
}

def get_fund_nav_sina(fund_code):
    """获取基金净值（新浪财经）"""
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
        
        text = response.text
        if text.startswith('jsonpgz(') and text.endswith(');'):
            data = json.loads(text[8:-2])
            return {
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'nav': float(data.get('gsz', 0)),
                'nav_change': float(data.get('gszzl', 0)),
                'date': data.get('gzrq'),
            }
        return None
        
    except Exception as e:
        print(f"  获取 {fund_code} 失败: {e}")
        return None

def main():
    print("=" * 70)
    print("我的基金持仓分析 (新浪财经接口)")
    print("=" * 70)
    print()
    
    results = []
    
    for code, name in MY_FUNDS.items():
        result = get_fund_nav_sina(code)
        if result:
            results.append(result)
            print(f"【{name}】")
            print(f"  净值: {result['nav']:.4f}")
            print(f"  日涨跌: {result['nav_change']:+.2f}%")
            print(f"  时间: {result['date']}")
            print()
        else:
            print(f"【{name}】")
            print(f"  获取失败")
            print()
        time.sleep(0.5)  # 避免请求过快
    
    if results:
        avg_change = sum(r['nav_change'] for r in results) / len(results)
        print("=" * 70)
        print(f"平均日涨跌幅: {avg_change:+.2f}%")
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
