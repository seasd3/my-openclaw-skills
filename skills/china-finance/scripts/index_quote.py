#!/usr/bin/env python3
"""指数行情查询 - 使用AKShare"""

import akshare as ak
import sys

def get_index_quote():
    """获取主要指数行情"""
    try:
        print("=" * 60)
        print("A股主要指数行情")
        print("=" * 60)
        print()
        
        # 指数列表
        indices = [
            ("000001", "上证指数"),
            ("399001", "深证成指"),
            ("399006", "创业板指"),
            ("000016", "上证50"),
            ("000300", "沪深300"),
            ("000905", "中证500"),
        ]
        
        from datetime import datetime, timedelta
        today = datetime.now().strftime('%Y%m%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        
        print("【指数行情】")
        print(f"{'指数名称':<12} {'最新':<10} {'涨跌':<8} {'涨跌幅':<8}")
        print("-" * 60)
        
        for code, name in indices:
            try:
                df = ak.index_zh_a_hist(symbol=code, period="daily", 
                                       start_date=yesterday, end_date=today)
                if not df.empty:
                    latest = df.iloc[-1]
                    prev_close = latest['昨收'] if '昨收' in latest else latest['开盘']
                    close = latest['收盘']
                    change = close - prev_close
                    change_pct = (change / prev_close) * 100
                    print(f"{name:<12} {close:<10.2f} {change:<+8.2f} {change_pct:<+.2f}%")
            except:
                continue
        
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"获取数据失败: {e}")

if __name__ == "__main__":
    get_index_quote()
