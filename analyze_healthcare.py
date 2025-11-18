#!/usr/bin/env python3
"""
Healthcare Performance Analysis - Patient Satisfaction Score Study
Author: 22f3002460@ds.study.iitm.ac.in
Date: 2024
Purpose: Analyze quarterly patient satisfaction trends and provide actionable insights
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

def load_data():
    """Load and prepare the quarterly satisfaction data"""
    data = {
        'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
        'Satisfaction_Score': [1.06, 1.88, 3.49, 8.81]
    }
    return pd.DataFrame(data)

def calculate_metrics(df):
    """Calculate key performance metrics"""
    metrics = {
        'average': df['Satisfaction_Score'].mean(),
        'target': 4.5,
        'q1_score': df.loc[0, 'Satisfaction_Score'],
        'q4_score': df.loc[3, 'Satisfaction_Score'],
        'total_improvement': df.loc[3, 'Satisfaction_Score'] - df.loc[0, 'Satisfaction_Score']
    }
    metrics['gap_to_target'] = metrics['target'] - metrics['average']
    metrics['improvement_pct'] = (metrics['gap_to_target'] / metrics['average']) * 100
    return metrics

def analyze_growth(df):
    """Analyze quarter-over-quarter growth"""
    df['QoQ_Growth'] = df['Satisfaction_Score'].pct_change() * 100
    return df

def create_visualizations(df, metrics):
    """Generate comprehensive visualizations"""

    # Figure 1: Trend Analysis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    quarters = df['Quarter'].tolist()
    scores = df['Satisfaction_Score'].tolist()

    # Trend plot
    ax1.plot(quarters, scores, marker='o', linewidth=3, markersize=12, 
             color='#e74c3c', label='Actual Score')
    ax1.axhline(y=metrics['target'], color='#27ae60', linestyle='--', 
                linewidth=2, label=f"Industry Target ({metrics['target']})")
    ax1.axhline(y=metrics['average'], color='#f39c12', linestyle=':', 
                linewidth=2, label=f"2024 Average ({metrics['average']:.2f})")

    ax1.scatter([3], [metrics['q4_score']], s=400, c='gold', marker='*', 
                edgecolors='black', linewidths=2, zorder=5, label='Q4 Excellence')

    ax1.set_title('Patient Satisfaction Score - 2024 Quarterly Trend', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Satisfaction Score', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    for i, (q, s) in enumerate(zip(quarters, scores)):
        ax1.text(i, s + 0.3, f'{s:.2f}', ha='center', va='bottom', fontweight='bold')

    # Comparison plot
    categories = quarters + ['Average', 'Target']
    values = scores + [metrics['average'], metrics['target']]
    colors = ['#e74c3c', '#e67e22', '#f39c12', '#27ae60', '#3498db', '#2ecc71']

    bars = ax2.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)

    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                 f'{val:.2f}', ha='center', va='bottom', fontweight='bold')

    ax2.axhline(y=metrics['target'], color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_title('Performance Comparison', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Period', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Satisfaction Score', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('healthcare_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Figure 2: Growth Analysis
    fig, ax = plt.subplots(figsize=(10, 6))

    growth_rates = [0] + df['QoQ_Growth'].dropna().tolist()
    quarters_growth = ['Q1\n(Baseline)'] + [f'Q{i}' for i in range(2, 5)]

    bars = ax.bar(quarters_growth, growth_rates, 
                  color=['#95a5a6', '#3498db', '#9b59b6', '#27ae60'],
                  edgecolor='black', linewidth=2)

    for bar, rate in zip(bars, growth_rates):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + 3,
                    f'+{rate:.1f}%', ha='center', va='bottom', fontweight='bold')

    ax.set_title('Quarter-over-Quarter Growth Rate', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('growth_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

def print_report(df, metrics):
    """Print comprehensive analysis report"""
    print("="*70)
    print("HEALTHCARE PERFORMANCE ANALYSIS - 2024")
    print("Analyst: 22f3002460@ds.study.iitm.ac.in")
    print("="*70)

    print("\n📊 QUARTERLY DATA:")
    print(df.to_string(index=False))

    print(f"\n📈 KEY METRICS:")
    print(f"   Average Satisfaction Score: {metrics['average']:.2f}")
    print(f"   Industry Target: {metrics['target']:.2f}")
    print(f"   Gap to Target: {metrics['gap_to_target']:.2f} points")
    print(f"   Improvement Needed: {metrics['improvement_pct']:.1f}%")

    print(f"\n🎯 PERFORMANCE INSIGHTS:")
    print(f"   Q1 Starting Point: {metrics['q1_score']:.2f}")
    print(f"   Q4 Ending Point: {metrics['q4_score']:.2f}")
    print(f"   Total Improvement: {metrics['total_improvement']:.2f} points")
    print(f"   Growth Rate: {(metrics['total_improvement']/metrics['q1_score']*100):.1f}%")

    print(f"\n✅ STATUS:")
    if metrics['q4_score'] > metrics['target']:
        print(f"   Q4 EXCEEDS target by {metrics['q4_score'] - metrics['target']:.2f} points")
    print(f"   Strong upward trend observed throughout 2024")

    print("\n" + "="*70)

def main():
    """Main execution function"""
    # Load and analyze data
    df = load_data()
    df = analyze_growth(df)
    metrics = calculate_metrics(df)

    # Generate outputs
    print_report(df, metrics)
    create_visualizations(df, metrics)

    print("\n✓ Analysis complete!")
    print("✓ Visualizations saved: healthcare_analysis.png, growth_analysis.png")
    print("="*70)

if __name__ == "__main__":
    main()
