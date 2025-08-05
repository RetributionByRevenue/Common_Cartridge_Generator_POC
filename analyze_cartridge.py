#!/usr/bin/env python3
"""
Analyze cartridge assignment content issue
"""

import sys
import os
sys.path.append('/home/q/Desktop/test_cartridge')

from cartridge_replicator import scan_cartridge
import pandas as pd

def analyze_assignment_components(cartridge_path, cartridge_name):
    """Analyze assignment-related components in a cartridge"""
    print(f"\n=== ANALYZING {cartridge_name.upper()} ===")
    
    df = scan_cartridge(cartridge_path)
    
    # Filter for assignment-related components
    assignment_types = ['assignment_content', 'assignment_settings', 'resource']
    assignment_df = df[df['type'].isin(assignment_types)]
    
    print(f"Found {len(assignment_df)} assignment-related components:")
    print(assignment_df['type'].value_counts())
    print()
    
    # Show assignment_content entries
    content_entries = df[df['type'] == 'assignment_content']
    if not content_entries.empty:
        print("ASSIGNMENT_CONTENT ENTRIES:")
        for idx, row in content_entries.iterrows():
            print(f"  File: {row['filename']}")
            print(f"  Title: {row['title']}")
            print(f"  Content preview: {row['xml_content'][:200]}...")
            print()
    else:
        print("NO assignment_content entries found!")
        print()
    
    # Show assignment_settings entries  
    settings_entries = df[df['type'] == 'assignment_settings']
    if not settings_entries.empty:
        print("ASSIGNMENT_SETTINGS ENTRIES:")
        for idx, row in settings_entries.iterrows():
            print(f"  File: {row['filename']}")
            print(f"  Identifier: {row['identifier']}")
            print(f"  Title: {row['title']}")
            print(f"  Content preview: {row['xml_content'][:300]}...")
            print()
    else:
        print("NO assignment_settings entries found!")
        print()
    
    # Show resource entries that might be assignments
    resource_entries = df[df['type'] == 'resource']
    assignment_resources = resource_entries[resource_entries['resource_type'].str.contains('assignment', na=False, case=False)]
    if not assignment_resources.empty:
        print("ASSIGNMENT RESOURCE ENTRIES:")
        for idx, row in assignment_resources.iterrows():
            print(f"  Identifier: {row['identifier']}")
            print(f"  Resource Type: {row['resource_type']}")
            print(f"  Href: {row['href']}")
            print(f"  Title: {row['title']}")
            print()
    else:
        print("NO assignment resource entries found!")
        print()

    # Show module items that reference assignments
    module_items = df[df['type'] == 'module_item']
    assignment_module_items = module_items[module_items['content_type'] == 'Assignment']
    if not assignment_module_items.empty:
        print("MODULE ITEMS REFERENCING ASSIGNMENTS:")
        for idx, row in assignment_module_items.iterrows():
            print(f"  Title: {row['title']}")
            print(f"  Identifier Ref: {row['identifierref']}")
            print(f"  Content Type: {row['content_type']}")
            print()
    else:
        print("NO module items referencing assignments found!")
        print()
    
    return df

def main():
    # Analyze working cartridge
    working_df = analyze_assignment_components(
        '/home/q/Desktop/test_cartridge/working_cartridge',
        'WORKING CARTRIDGE'
    )
    
    # Analyze generated test cartridge
    generated_df = analyze_assignment_components(
        '/home/q/Desktop/test_cartridge/generated_cartridge',
        'GENERATED TEST CARTRIDGE'
    )
    
    print("\n=== COMPARISON SUMMARY ===")
    
    # Compare counts
    working_assignment_content = len(working_df[working_df['type'] == 'assignment_content'])
    working_assignment_settings = len(working_df[working_df['type'] == 'assignment_settings'])
    
    generated_assignment_content = len(generated_df[generated_df['type'] == 'assignment_content'])
    generated_assignment_settings = len(generated_df[generated_df['type'] == 'assignment_settings'])
    
    print(f"Assignment Content - Working: {working_assignment_content}, Generated: {generated_assignment_content}")
    print(f"Assignment Settings - Working: {working_assignment_settings}, Generated: {generated_assignment_settings}")
    
    # Look for differences in file structure
    working_files = set(working_df[working_df['filename'].notna()]['filename'].tolist())
    generated_files = set(generated_df[generated_df['filename'].notna()]['filename'].tolist())
    
    print(f"\nFiles only in working cartridge: {working_files - generated_files}")
    print(f"Files only in generated cartridge: {generated_files - working_files}")
    
    # Save detailed analysis to HTML table
    print("\nGenerating detailed HTML analysis...")
    
    # Create combined analysis DataFrame
    analysis_data = []
    
    for cartridge_name, df in [('Working', working_df), ('Generated', generated_df)]:
        for _, row in df.iterrows():
            if row['type'] in ['assignment_content', 'assignment_settings', 'resource', 'module_item']:
                analysis_data.append({
                    'Cartridge': cartridge_name,
                    'Type': row['type'],
                    'Identifier': row['identifier'],
                    'Title': row['title'],
                    'Filename': row['filename'],
                    'Resource_Type': row.get('resource_type', ''),
                    'Content_Type': row.get('content_type', ''),
                    'Identifierref': row.get('identifierref', ''),
                    'Href': row.get('href', ''),
                    'Content_Preview': str(row['xml_content'])[:500] if pd.notna(row['xml_content']) else ''
                })
    
    analysis_df = pd.DataFrame(analysis_data)
    
    # Generate HTML table
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Assignment Content Analysis</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .working {{ background-color: #e8f5e8; }}
            .generated {{ background-color: #fff5e8; }}
            .content-preview {{ max-width: 400px; overflow: auto; font-family: monospace; font-size: 10px; }}
        </style>
    </head>
    <body>
        <h1>Assignment Content Analysis</h1>
        <h2>Comparison between Working and Generated Cartridges</h2>
        
        <h3>Summary</h3>
        <ul>
            <li>Working Cartridge - Assignment Content: {working_assignment_content}, Assignment Settings: {working_assignment_settings}</li>
            <li>Generated Cartridge - Assignment Content: {generated_assignment_content}, Assignment Settings: {generated_assignment_settings}</li>
        </ul>
        
        {analysis_df.to_html(escape=False, classes='analysis-table', table_id='analysis-table')}
    </body>
    </html>
    """
    
    with open('/home/q/Desktop/Common_Cartridge_Generator_POC/assignment_analysis.html', 'w') as f:
        f.write(html_content)
    
    print("Analysis saved to assignment_analysis.html")

if __name__ == "__main__":
    main()