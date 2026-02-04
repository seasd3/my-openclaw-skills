#!/usr/bin/env python3
"""股票历史数据查询 - 使用Baostock"""

import baostock as bs
import pandas as pd
import argparse
from datetime import datetime, timedelta

def get_stock_history(code, days=30):
    """获取股票历史数据"""
    try:
        print(f"=" * 60)
        print(f"历史行情 - {code} (最近{days}天)")
        print(f"=" * 60)
        print()
        
        # 登录
        lg = bs.login()
        if lg.error_code != '0':
            print(f"登录失败: {lg.error_msg}")
            return
        
        # 计算日期
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # 转换股票代码格式
        if code.startswith('6'):
            bs_code = f"sh.{code}"
        else:
            bs_code = f"sz.{code}"
        
        # 查询数据
        rs = bs.query_history_k_data_plus(bs_code,
            "date,code,open,high,low,close,preclose,volume,amount,turn",
            start_date=start_str, end_date=end_str,
            frequency="d", adjustflag="3")
        
        if rs.error_code != '0':
            print(f"查询失败: {rs.error_msg}")
            bs.logout()
            return
        
        # 打印数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if not data_list:
            print("未获取到数据")
            bs.logout()
            return
        
        result = pd.DataFrame(data_list, columns=rs.fields)
        
        print(f"{'日期':<12} {'开盘':<8} {'最高':<8} {'最低':<8} {'收盘':<8} {'涨跌':<8}")
        print("-" * 60)
        
        for _, row in result.iterrows():
            try:
                open_p = float(row['open'])
                close_p = float(row['close'])
                change = close_p - open_p
                print(f"{row['date']:<12} {open_p:<8.2f} {float(row['high']):<8.2f} "
                      f"{float(row['low']):<8.2f} {close_p:<8.2f} {change:<+8.2f}")
            except:
                continue
        
        print()
        print(f"=" * 60)
        
        bs.logout()
        
    except Exception as e:
        print(f"获取数据失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="查询股票历史数据")
    parser.add_argument("--code", required=True, help="股票代码，如: 000001")
    parser.add_argument("--days", type=int, default=30, help="天数，默认30天")
    
    args = parser.parse_args()
    get_stock_history(args.code, args.days)

if __name__ == "__main__":
    main()
