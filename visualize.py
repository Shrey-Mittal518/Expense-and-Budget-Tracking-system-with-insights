# visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = "family_expenses_10000.csv"
CHARTS_DIR = "charts"

# Create charts directory if it doesn't exist
if not os.path.exists(CHARTS_DIR):
    os.makedirs(CHARTS_DIR)

def pie_chart_member(member, family_id):
    """Create pie chart for a specific member's spending by category"""
    df = pd.read_csv(DATA_FILE)
    df = df[(df['Member'] == member) & (df['Family_ID'] == family_id)]
    
    if df.empty:
        # Create empty chart
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', fontsize=16, color='gray')
        plt.axis('off')
        plt.savefig(f'{CHARTS_DIR}/pie_{member}_{family_id}.png', bbox_inches='tight')
        plt.close()
        return
    
    category_spending = df.groupby('Category')['Amount'].sum()
    
    plt.figure(figsize=(8, 6))
    plt.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'{member} Spending by Category')
    plt.savefig(f'{CHARTS_DIR}/pie_{member}_{family_id}.png', bbox_inches='tight')
    plt.close()

def bar_chart_family_members(family_id):
    """Create bar chart showing spending of all members within the same family"""
    df = pd.read_csv(DATA_FILE)
    df = df[df['Family_ID'] == family_id]
    
    if df.empty:
        # Create empty chart
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'No data available for this family', 
                ha='center', va='center', fontsize=16, color='gray')
        plt.axis('off')
        plt.savefig(f'{CHARTS_DIR}/bar_family_members_{family_id}.png', bbox_inches='tight', dpi=100)
        plt.close()
        return
    
    # Get total spending per member in this family
    member_spending = df.groupby('Member')['Amount'].sum().sort_values(ascending=False)
    
    # Create gradient colors
    colors = plt.cm.viridis(range(len(member_spending)))
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(member_spending)), member_spending.values, color=colors)
    
    plt.xticks(range(len(member_spending)), member_spending.index, rotation=45, ha='right')
    plt.xlabel('Family Member', fontsize=12, fontweight='bold')
    plt.ylabel('Total Spending (₹)', fontsize=12, fontweight='bold')
    plt.title(f'Family {family_id} - Member-wise Spending', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on top of bars
    for i, (member, val) in enumerate(member_spending.items()):
        plt.text(i, val, f'₹{val:,.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/bar_family_members_{family_id}.png', bbox_inches='tight', dpi=100)
    plt.close()

def bar_chart_category_member_comparison(user, family_id):
    """Create bar chart comparing spending by category across members IN THE SAME FAMILY"""
    df = pd.read_csv(DATA_FILE)
    
    # Filter only for the current family
    df = df[df['Family_ID'] == family_id]
    
    if df.empty:
        # Create empty chart if no data
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', fontsize=16, color='gray')
        plt.axis('off')
        plt.savefig(f'{CHARTS_DIR}/bar_category_member_{family_id}.png', bbox_inches='tight', dpi=100)
        plt.close()
        return
    
    # Get all members in this family
    members = df['Member'].unique()
    
    if len(members) == 0:
        # Create empty chart if no members
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'No family members found', 
                ha='center', va='center', fontsize=16, color='gray')
        plt.axis('off')
        plt.savefig(f'{CHARTS_DIR}/bar_category_member_{family_id}.png', bbox_inches='tight', dpi=100)
        plt.close()
        return
    
    # Pivot table for comparison - only family members
    pivot_data = df.pivot_table(values='Amount', index='Category', 
                                 columns='Member', aggfunc='sum', fill_value=0)
    
    # Reorder columns to put current user first if they exist
    if user in pivot_data.columns:
        cols = [user] + [col for col in pivot_data.columns if col != user]
        pivot_data = pivot_data[cols]
    
    plt.figure(figsize=(14, 7))
    ax = pivot_data.plot(kind='bar', ax=plt.gca(), width=0.8, colormap='Set2')
    
    plt.xlabel('Category', fontsize=12, fontweight='bold')
    plt.ylabel('Spending (₹)', fontsize=12, fontweight='bold')
    plt.title(f'Category-wise Spending - Family {family_id} Members', fontsize=14, fontweight='bold')
    plt.legend(title='Family Member', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/bar_category_member_{family_id}.png', bbox_inches='tight', dpi=100)
    plt.close()
