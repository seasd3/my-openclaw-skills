#!/usr/bin/env python3
"""基金净值查询 - 使用AKShare"""

import akshare as ak
import argparse
import sys

def get_fund_nav(fund_code):
    """获取基金净值"""
    try:
        print(f"=" * 60)
        print(f"基金净值查询 - {fund_code}")
        print(f"=" * 60)
        print()
        
        # 获取基金信息
        df = ak.fund_em_open_fund_info(fund=fund_code, indicator="单位净值走势")
        
        if df.empty:
            print(f"未找到基金 {fund_code} 的数据")
            return
        
        # 最新净值
        latest = df.iloc[-1]
        print(f"【最新净值】")
        print(f"日期: {latest['净值日期']}")
        print(f"单位净值: {latest['单位净值']}")
        if '日增长率' in latest:
            print(f"日增长率: {latest['日增长率']}")
        
        print()
        print(f"【近期走势】")
        # 显示最近10天
        recent = df.tail(10)
        for _, row in recent.iterrows():
            print(f"{row['净值日期']} | {row['单位净值']}")
        
        print()
        print(f"=" * 60)
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        print("提示: 请检查基金代码是否正确")

def main():
    parser = argparse.ArgumentParser(description="查询基金净值")
    parser.add_argument("--code", required=True, help="基金代码，如: 000001")
    
    args = parser.parse_args()
    get_fund_nav(args.code)

if __name__ == "__main__":
    main()
