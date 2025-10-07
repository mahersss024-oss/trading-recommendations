import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime
import os
import random
import string
import json
from typing import Dict, List, Optional, Tuple

# ثوابت التطبيق
DB_NAME = 'trading_recommendations.db'

# دالة تحليل ملف التوصيات المحسنة والمصححة
def parse_recommendations_file(content: str) -> Dict:
    lines = content.split('\n')
    
    # استخراج تحليل السوق
    market_analysis = ""
    for i, line in enumerate(lines):
        if "حالة السوق" in line or "مؤشر RSI" in line or "قوة الاتجاه" in line:
            market_analysis += line + "\n"
    
    # البحث عن جدول الصفقات
    trades_data = []
    in_table = False
    table_header_found = False
    column_indices = {}
    
    # طباعة للتصحيح - عرض محتويات الملف
    print(f"محتوى الملف الذي تم تحليله: {len(lines)} سطر")
    
    # مسح أولي لتحديد جدول الصفقات
    for line_index, line in enumerate(lines):
        # طباعة كل سطر للتشخيص
        print(f"[فحص] سطر {line_index + 1}: {line}")
        
        # التحقق من بداية جدول الصفقات
        if "جدول الصفقات التفصيلي" in line or "جدول الصفقات المفصل" in line:
            in_table = True
            print(f"تم العثور على بداية جدول الصفقات في السطر {line_index + 1}")
            continue
        
        # البحث عن عناوين الأعمدة
        if in_table and not table_header_found and ("الرمز" in line and "السعر" in line and "التوصية" in line):
            table_header_found = True
            print(f"تم العثور على رؤوس الجدول في السطر {line_index + 1}: {line}")
            continue
        
        # التحقق مما إذا كنا في جدول الصفقات والسطر يحتوي على بيانات
        if in_table and table_header_found:
            # التحقق من نهاية الجدول
            if "تحليل المخاطر" in line or "====" in line or ("مخاطر" in line and "•" in line):
                print(f"تم العثور على نهاية الجدول في السطر {line_index + 1}")
                break
                
            # نتحقق ما إذا كان السطر يحتوي على بيانات صفقة
            if ('│' in line or '|' in line) and len(line.strip()) > 10:
                # تحقق إضافي: يجب أن تكون هناك أرقام في السطر (للسعر أو الثقة)
                has_numbers = any(c.isdigit() for c in line)
                if has_numbers:
                    print(f"سطر صفقة محتمل ({line_index + 1}): {line}")
                    
                    # تحليل سطر الصفقة
                    try:
                        # تحديد الفاصل المستخدم
                        separator = '│' if '│' in line else '|'
                        
                        # تقسيم السطر إلى أجزاء
                        parts = [part.strip() for part in line.split(separator) if part.strip()]
                        print(f"الأجزاء المستخرجة: {parts}")
                        
                        # تحقق من أن هناك أجزاء كافية للتحليل
                        if len(parts) >= 3:
                            symbol = parts[0]
                            
                            # تنظيف وتحويل السعر
                            price_str = parts[1].replace(',', '').replace('$', '')
                            try:
                                price = float(price_str)
                            except ValueError:
                                price = 0
                            
                            # تنظيف واستخراج التوصية
                            recommendation = parts[2]
                            if "🟢" in recommendation:
                                recommendation = "شراء"
                            elif "🔴" in recommendation:
                                recommendation = "بيع"
                            elif "شراء" in recommendation.lower():
                                recommendation = "شراء"
                            elif "بيع" in recommendation.lower():
                                recommendation = "بيع"
                            else:
                                recommendation = recommendation.strip()
                            
                            # استخراج البيانات الأخرى بأمان
                            def safe_extract(parts, index, default=0):
                                if index < len(parts):
                                    try:
                                        value = parts[index].replace(',', '').replace('$', '').replace('%', '')
                                        return float(value)
                                    except ValueError:
                                        return default
                                return default
                            
                            # استخراج باقي البيانات
                            confidence = safe_extract(parts, 3)
                            stop_loss = safe_extract(parts, 4)
                            target_profit = safe_extract(parts, 5)
                            risk_reward = safe_extract(parts, 6)
                            rsi = safe_extract(parts, 7)
                            macd = safe_extract(parts, 8)
                            
                            # استخراج الاتجاه (قد يكون نصًا)
                            trend = parts[9].strip() if len(parts) > 9 else ""
                            
                            # إنشاء كائن الصفقة
                            trade = {
                                'symbol': symbol,
                                'price': price,
                                'recommendation': recommendation,
                                'confidence': confidence,
                                'stop_loss': stop_loss,
                                'target_profit': target_profit,
                                'risk_reward_ratio': risk_reward,
                                'rsi': rsi,
                                'macd': macd,
                                'trend': trend
                            }
                            
                            # إضافة الصفقة للقائمة
                            trades_data.append(trade)
                            print(f"✅ تمت إضافة صفقة: {symbol} - {recommendation}")
                    
                    except Exception as e:
                        print(f"❌ خطأ في تحليل سطر الصفقة: {e}")
    
    # حساب الإحصائيات بعد المسح الكامل للملف
    total_symbols = len(trades_data)
    
    # استخدام الاسم العربي أو المسار .recommendation حسب الهيكل
    buy_count = 0
    sell_count = 0
    
    for trade in trades_data:
        if 'شراء' in str(trade.get('recommendation', '')).lower():
            buy_count += 1
        elif 'بيع' in str(trade.get('recommendation', '')).lower():
            sell_count += 1
    
    neutral_count = total_symbols - buy_count - sell_count
    
    # حساب المتوسطات
    confidence_sum = 0
    risk_reward_sum = 0
    
    for trade in trades_data:
        confidence_sum += float(trade.get('confidence', 0))
        risk_reward_sum += float(trade.get('risk_reward_ratio', 0))
    
    avg_confidence = confidence_sum / total_symbols if total_symbols > 0 else 0
    avg_risk_reward = risk_reward_sum / total_symbols if total_symbols > 0 else 0
    
    # طباعة ملخص النتائج للتشخيص
    print(f"===== ملخص التحليل =====")
    print(f"تم تحليل {total_symbols} رمز من الملف")
    print(f"توصيات الشراء: {buy_count}")
    print(f"توصيات البيع: {sell_count}")
    print(f"توصيات محايدة: {neutral_count}")
    print(f"متوسط الثقة: {avg_confidence:.1f}%")
    print(f"متوسط نسبة المخاطرة/المكافأة: {avg_risk_reward:.2f}")
    
    # بناء وإعادة قاموس النتائج
    result = {
        'market_analysis': market_analysis,
        'trades': trades_data,
        'stats': {
            'total_symbols': total_symbols,
            'buy_recommendations': buy_count,
            'sell_recommendations': sell_count,
            'neutral_recommendations': neutral_count,
            'avg_confidence': avg_confidence,
            'avg_risk_reward': avg_risk_reward
        }
    }
    
    # طباعة للتشخيص
    print(f"تحليل كامل للتقرير: {total_symbols} رمز, {len(trades_data)} صفقة")
    
    return result