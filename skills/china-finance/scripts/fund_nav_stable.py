#!/usr/bin/env python3
"""基金净值查询 - 稳定版

使用多个备用接口，确保数据获取成功。
接口优先级：
1. 新浪财经 fundgz（稳定）
2. 东方财富 App API（备用）
"""

import requests
import json
import re
import argparse
import sys

def get_fund_nav(fund_code, source='sina'):
    """获取基金净值"""
    
    if source == 'sina':
        return get_from_sina(fund_code)
    elif source == 'eastmoney':
        return get_from_eastmoney(fund_code)
    else:
        return None

def get_from_sina(fund_code):
    """新浪财经接口"""
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        text = r.text
        if text.startswith('jsonpgz(') and text.endswith(');'):
            data = json.loads(text[8:-2])
            return {
                'source': '新浪财经',
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'nav': float(data.get('gsz', 0)),  # 估算净值
                'nav_change': float(data.get('gszzl', 0)),  # 估算涨跌
                'dwjz': float(data.get('dwjz', 0)),  # 单位净值
                'date': data.get('gzrq'),
            }
        return None
    except Exception as e:
        print(f"  新浪接口失败: {e}")
        return None

def get_from_eastmoney(fund_code):
    """东方财富 App 接口"""
    try:
        url = "https://fundapp.eastmoney.com/f10/AppDataProxy.aspx"
        data = {'rcode': fund_code, 'AppName': 'VALU', 'type': 'SY'}
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        r = requests.post(url, data=data, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        
        # 解析返回数据
        text = r.text
        # 格式可能是: var apidata=[{...}];
        match = re.search(r'var apidata=\[({[^}]+})\]', text)
        if match:
            data = json.loads(match.group(1))
            return {
                'source': '东方财富',
                'code': fund_code,
                'name': data.get('name', ''),
                'nav': float(data.get('nav', 0)),
                'nav_change': float(data.get('change', 0)),
                'date': data.get('date', ''),
            }
        return None
    except Exception as e:
        print(f"  东方财富接口失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="基金净值查询 - 多接口版本")
    parser.add_argument("--code", required=True, help="基金代码，如: 017193")
    parser.add_argument("--source", default="sina", choices=["sina", "eastmoney"],
                       help="数据源: sina(默认) 或 eastmoney")
    
    args = parser.parse_args()
    
    print(f"查询基金: {args.code}")
    print(f"数据源: {args.source}")
    print("-" * 50)
    
    result = get_fund_nav(args.code, args.source)
    
    if result:
        print(f"基金名称: {result['name']}")
        print(f"基金代码: {result['code']}")
        print(f"数据来源: {result['source']}")
        if result.get('nav'):
            print(f"估算净值: {result['nav']:.4f}")
        if result.get('dwjz'):
            print(f"单位净值: {result['dwjz']:.4f}")
        if result.get('nav_change'):
            print(f"日增长率: {result['nav_change']:+.2f}%")
        if result.get('date'):
            print(f"估算时间: {result['date']}")
    else:
        print("获取数据失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
