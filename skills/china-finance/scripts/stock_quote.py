#!/usr/bin/env python3
"""A股实时行情查询 - 使用AKShare"""

import akshare as ak
import sys

def get_a_stock_spot():
    """获取A股实时行情"""
    try:
        print("=" * 60)
        print("A股实时行情 (数据来源: 东方财富)")
        print("=" * 60)
        print()
        
        # 获取实时行情
        df = ak.stock_zh_a_spot_em()
        
        # 显示涨跌幅前10
        print("【涨幅榜 TOP 10】")
        top_gainers = df.nlargest(10, '涨跌幅')[['名称', '最新价', '涨跌幅', '成交量']]
        for idx, row in top_gainers.iterrows():
            print(f"{row['名称']:8} {row['最新价']:8.2f} {row['涨跌幅']:+.2f}%")
        
        print()
        print("【跌幅榜 TOP 10】")
        top_losers = df.nsmallest(10, '涨跌幅')[['名称', '最新价', '涨跌幅', '成交量']]
        for idx, row in top_losers.iterrows():
            print(f"{row['名称']:8} {row['最新价']:8.2f} {row['涨跌幅']:+.2f}%")
        
        print()
        print("【主要指数】")
        # 上证指数
        sh_df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date="20260204", end_date="20260204")
        if not sh_df.empty:
            row = sh_df.iloc[0]
            change_pct = (row['收盘'] - row['开盘']) / row['开盘'] * 100
            print(f"上证指数: {row['收盘']:.2f} ({change_pct:+.2f}%)")
        
        # 深证成指
        sz_df = ak.index_zh_a_hist(symbol="399001", period="daily", start_date="20260204", end_date="20260204")
        if not sz_df.empty:
            row = sz_df.iloc[0]
            change_pct = (row['收盘'] - row['开盘']) / row['开盘'] * 100
            print(f"深证成指: {row['收盘']:.2f} ({change_pct:+.2f}%)")
        
        # 创业板指
        cy_df = ak.index_zh_a_hist(symbol="399006", period="daily", start_date="20260204", end_date="20260204")
        if not cy_df.empty:
            row = cy_df.iloc[0]
            change_pct = (row['收盘'] - row['开盘']) / row['开盘'] * 100
            print(f"创业板指: {row['收盘']:.2f} ({change_pct:+.2f}%)")
        
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        print("提示: 请检查网络连接或非交易时间")

if __name__ == "__main__":
    get_a_stock_spot()
