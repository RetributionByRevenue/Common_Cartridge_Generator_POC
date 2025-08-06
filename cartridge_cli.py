#!/usr/bin/env python3
"""
Command Line Interface for Canvas Common Cartridge Generator
"""

import argparse
import sys
from pathlib import Path
import shutil
from cartridge_generator import CartridgeGenerator


def create_cartridge(args):
    """Create a new cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if cartridge_path.exists():
        print(f"Error: Directory '{args.cartridge_name}' already exists")
        return 1
    
    # Create generator
    generator = CartridgeGenerator(args.title, args.code)
    
    # Create base cartridge
    print(f"Creating cartridge: {args.cartridge_name}")
    generator.create_base_cartridge(args.cartridge_name)
    
    print(f"✓ Cartridge '{args.cartridge_name}' created successfully")
    print(f"  Title: {args.title}")
    print(f"  Code: {args.code}")
    print(f"  Components: {len(generator.df)}")
    
    return 0


def add_module(args):
    """Add a module to an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Add module
    print(f"Adding module '{args.title}' to cartridge '{args.cartridge_name}'")
    module_id = generator.add_module(args.title, position=args.position, published=args.published)
    
    print(f"✓ Module '{args.title}' added successfully")
    print(f"  Module ID: {module_id}")
    print(f"  Position: {args.position}")
    print(f"  Published: {args.published}")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_wiki(args):
    """Add a wiki page to a module in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Find module by title
    try:
        module_row = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == args.module)]
        if module_row.empty:
            print(f"Error: Module '{args.module}' not found in cartridge")
            print("Available modules:")
            modules = generator.df[generator.df["type"] == "module"]["title"].tolist()
            for module in modules:
                print(f"  - {module}")
            return 1
        
        module_id = module_row.iloc[0]["identifier"]
        
    except Exception as e:
        print(f"Error finding module: {e}")
        return 1
    
    # Add wiki page to module
    print(f"Adding wiki page '{args.title}' to module '{args.module}' in cartridge '{args.cartridge_name}'")
    generator.add_wiki_page_to_module(module_id, args.title, page_content=args.content, published=True, position=None)
    
    print(f"✓ Wiki page '{args.title}' added successfully")
    print(f"  Module: {args.module}")
    print(f"  Content length: {len(args.content)} characters")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_assignment(args):
    """Add an assignment to a module in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Find module by title
    try:
        module_row = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == args.module)]
        if module_row.empty:
            print(f"Error: Module '{args.module}' not found in cartridge")
            print("Available modules:")
            modules = generator.df[generator.df["type"] == "module"]["title"].tolist()
            for module in modules:
                print(f"  - {module}")
            return 1
        
        module_id = module_row.iloc[0]["identifier"]
        
    except Exception as e:
        print(f"Error finding module: {e}")
        return 1
    
    # Add assignment to module
    print(f"Adding assignment '{args.title}' to module '{args.module}' in cartridge '{args.cartridge_name}'")
    generator.add_assignment_to_module(module_id, args.title, assignment_content=args.content, points=args.points, published=True, position=None)
    
    print(f"✓ Assignment '{args.title}' added successfully")
    print(f"  Module: {args.module}")
    print(f"  Points: {args.points}")
    print(f"  Content length: {len(args.content)} characters")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_quiz(args):
    """Add a quiz to a module in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Find module by title
    try:
        module_row = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == args.module)]
        if module_row.empty:
            print(f"Error: Module '{args.module}' not found in cartridge")
            print("Available modules:")
            modules = generator.df[generator.df["type"] == "module"]["title"].tolist()
            for module in modules:
                print(f"  - {module}")
            return 1
        
        module_id = module_row.iloc[0]["identifier"]
        
    except Exception as e:
        print(f"Error finding module: {e}")
        return 1
    
    # Add quiz to module
    print(f"Adding quiz '{args.title}' to module '{args.module}' in cartridge '{args.cartridge_name}'")
    generator.add_quiz_to_module(module_id, args.title, quiz_description=args.description, points=args.points, published=True, position=None)
    
    print(f"✓ Quiz '{args.title}' added successfully")
    print(f"  Module: {args.module}")
    print(f"  Points: {args.points}")
    print(f"  Description length: {len(args.description)} characters")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_discussion(args):
    """Add a discussion to a module in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Find module by title
    try:
        module_row = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == args.module)]
        if module_row.empty:
            print(f"Error: Module '{args.module}' not found in cartridge")
            print("Available modules:")
            modules = generator.df[generator.df["type"] == "module"]["title"].tolist()
            for module in modules:
                print(f"  - {module}")
            return 1
        
        module_id = module_row.iloc[0]["identifier"]
        
    except Exception as e:
        print(f"Error finding module: {e}")
        return 1
    
    # Add discussion to module
    print(f"Adding discussion '{args.title}' to module '{args.module}' in cartridge '{args.cartridge_name}'")
    generator.add_discussion_to_module(module_id, args.title, args.description, published=True, position=None)
    
    print(f"✓ Discussion '{args.title}' added successfully")
    print(f"  Module: {args.module}")
    print(f"  Description length: {len(args.description)} characters")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_file(args):
    """Add a file to a module in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Find module by title
    try:
        module_row = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == args.module)]
        if module_row.empty:
            print(f"Error: Module '{args.module}' not found in cartridge")
            print("Available modules:")
            modules = generator.df[generator.df["type"] == "module"]["title"].tolist()
            for module in modules:
                print(f"  - {module}")
            return 1
        
        module_id = module_row.iloc[0]["identifier"]
        
    except Exception as e:
        print(f"Error finding module: {e}")
        return 1
    
    # Add file to module
    print(f"Adding file '{args.filename}' to module '{args.module}' in cartridge '{args.cartridge_name}'")
    generator.add_file_to_module(module_id, args.filename, args.content, position=None)
    
    print(f"✓ File '{args.filename}' added successfully")
    print(f"  Module: {args.module}")
    print(f"  Content length: {len(args.content)} characters")
    print(f"  Total components: {len(generator.df)}")
    
    return 0


def list_cartridge(args):
    """List contents of an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Get summary
    summary = generator.get_hydration_summary()
    
    print(f"Cartridge: {args.cartridge_name}")
    print(f"  Course: {summary['course_title']} ({summary['course_code']})")
    print(f"  Total components: {summary['total_components']}")
    print()
    
    # List modules and their contents
    modules = generator.df[generator.df["type"] == "module"]
    if not modules.empty:
        print("Modules:")
        
        # Parse organization structure from manifest to get proper module-item hierarchy
        manifest_row = generator.df[generator.df["type"] == "manifest"]
        if not manifest_row.empty:
            import xml.etree.ElementTree as ET
            try:
                manifest_xml = manifest_row.iloc[0]['xml_content']
                root = ET.fromstring(manifest_xml)
                
                # Find LearningModules organization
                learning_modules = root.find('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item[@identifier="LearningModules"]')
                if learning_modules is not None:
                    # Create a mapping of module ID to its items
                    module_items_map = {}
                    
                    for module_item in learning_modules.findall('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
                        if module_item.get('identifier') != 'LearningModules':
                            module_id = module_item.get('identifier')
                            title_elem = module_item.find('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
                            
                            # Find child items of this module
                            child_items = []
                            for child in module_item.findall('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
                                if child != module_item:  # Exclude the module itself
                                    child_title_elem = child.find('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
                                    child_title = child_title_elem.text if child_title_elem is not None else None
                                    child_ref = child.get('identifierref')
                                    if child_title:
                                        child_items.append({
                                            'title': child_title,
                                            'identifierref': child_ref
                                        })
                            
                            module_items_map[module_id] = child_items
                    
                    # Display modules with their proper items
                    for _, module in modules.iterrows():
                        print(f"  📁 {module['title']} (ID: {module['identifier']})")
                        
                        # Get items for this specific module
                        module_items = module_items_map.get(module['identifier'], [])
                        
                        # Remove duplicates while preserving order
                        seen_items = set()
                        unique_items = []
                        for item in module_items:
                            item_key = item['title'] if isinstance(item, dict) else item
                            if item_key not in seen_items:
                                seen_items.add(item_key)
                                unique_items.append(item)
                        
                        for item in unique_items:
                            if isinstance(item, dict):
                                item_title = item['title']
                                identifierref = item.get('identifierref')
                                
                                # Look up content type from resource or module_item data
                                content_type = "WikiPage"  # Default
                                
                                # Try to determine content type from identifierref
                                if identifierref:
                                    # Check resources for this identifierref
                                    resource_match = generator.df[
                                        (generator.df['identifier'] == identifierref) & 
                                        (generator.df['type'] == 'resource')
                                    ]
                                    if not resource_match.empty:
                                        resource_type = resource_match.iloc[0]['resource_type']
                                        if resource_type:
                                            if 'assessment' in resource_type:
                                                content_type = "Quiz"
                                            elif 'imsdt' in resource_type:
                                                content_type = "Discussion"
                                            elif resource_type == 'webcontent':
                                                content_type = "WikiPage"
                                            elif 'assignment' in resource_type:
                                                content_type = "Assignment"
                                            else:
                                                content_type = "File"
                                
                                # Also check module_item data for content_type
                                module_item_match = generator.df[
                                    (generator.df['title'] == item_title) & 
                                    (generator.df['type'] == 'module_item')
                                ]
                                if not module_item_match.empty:
                                    item_content_type = module_item_match.iloc[0].get('content_type')
                                    if item_content_type:
                                        content_type = item_content_type
                                        # Clean up content type names
                                        if content_type == "Quizzes::Quiz":
                                            content_type = "Quiz"
                                        elif content_type == "Attachment":
                                            content_type = "File"
                            else:
                                # Fallback for old format
                                item_title = item
                                content_type = "WikiPage"
                            
                            icons = {
                                "WikiPage": "📄",
                                "Assignment": "📝", 
                                "Quiz": "❓",
                                "DiscussionTopic": "💬",
                                "Discussion": "💬",
                                "File": "📎"
                            }
                            icon = icons.get(content_type, "❓")
                            print(f"    {icon} {item_title} ({content_type})")
                        
                        if not unique_items:
                            print("    (no items)")
                            
            except ET.ParseError as e:
                print(f"Error parsing manifest XML: {e}")
                # Fallback to simple module listing
                for _, module in modules.iterrows():
                    print(f"  📁 {module['title']} (ID: {module['identifier']})")
    
    # List component types
    print("\nComponent breakdown:")
    for comp_type, count in summary['component_types'].items():
        print(f"  {comp_type}: {count}")
    
    # Export DataFrame to HTML for inspection
    html_file = "table_inspect.html"
    generator.current_df.to_html(html_file, escape=False)
    print(f"\n✓ DataFrame exported to {html_file} for inspection")
    
    return 0


def package_cartridge(args):
    """Package cartridge into a zip file"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    print(f"Packaging cartridge '{args.cartridge_name}' into ZIP file...")
    zip_name = f"{args.cartridge_name}"
    shutil.make_archive(zip_name, 'zip', args.cartridge_name)
    
    print(f"✓ Cartridge packaged as '{zip_name}.zip'")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description="Canvas Common Cartridge CLI Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new cartridge')
    create_parser.add_argument('cartridge_name', help='Name of the cartridge directory to create')
    create_parser.add_argument('--title', required=True, help='Course title')
    create_parser.add_argument('--code', required=True, help='Course code')
    
    # Add-module command
    module_parser = subparsers.add_parser('add-module', help='Add a module to an existing cartridge')
    module_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    module_parser.add_argument('--title', required=True, help='Module title')
    module_parser.add_argument('--position', type=int, default=1, help='Module position (default: 1)')
    module_parser.add_argument('--published', type=bool, default=True, help='Whether module is published (default: True)')
    
    # Add-wiki command
    wiki_parser = subparsers.add_parser('add-wiki', help='Add a wiki page to a module')
    wiki_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    wiki_parser.add_argument('--module', required=True, help='Module title to add wiki page to')
    wiki_parser.add_argument('--title', required=True, help='Wiki page title')
    wiki_parser.add_argument('--content', required=True, help='Wiki page content')
    
    # Add-assignment command
    assignment_parser = subparsers.add_parser('add-assignment', help='Add an assignment to a module')
    assignment_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    assignment_parser.add_argument('--module', required=True, help='Module title to add assignment to')
    assignment_parser.add_argument('--title', required=True, help='Assignment title')
    assignment_parser.add_argument('--content', required=True, help='Assignment content/description')
    assignment_parser.add_argument('--points', type=int, default=100, help='Points possible (default: 100)')
    
    # Add-quiz command
    quiz_parser = subparsers.add_parser('add-quiz', help='Add a quiz to a module')
    quiz_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    quiz_parser.add_argument('--module', required=True, help='Module title to add quiz to')
    quiz_parser.add_argument('--title', required=True, help='Quiz title')
    quiz_parser.add_argument('--description', required=True, help='Quiz description')
    quiz_parser.add_argument('--points', type=int, default=10, help='Points possible (default: 10)')
    
    # Add-discussion command
    discussion_parser = subparsers.add_parser('add-discussion', help='Add a discussion to a module')
    discussion_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    discussion_parser.add_argument('--module', required=True, help='Module title to add discussion to')
    discussion_parser.add_argument('--title', required=True, help='Discussion title')
    discussion_parser.add_argument('--description', required=True, help='Discussion description/prompt')
    
    # Add-file command
    file_parser = subparsers.add_parser('add-file', help='Add a file to a module')
    file_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    file_parser.add_argument('--module', required=True, help='Module title to add file to')
    file_parser.add_argument('--filename', required=True, help='Filename')
    file_parser.add_argument('--content', required=True, help='File content')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List contents of a cartridge')
    list_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    
    # Package command
    package_parser = subparsers.add_parser('package', help='Package cartridge into ZIP file')
    package_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate function
    if args.command == 'create':
        return create_cartridge(args)
    elif args.command == 'add-module':
        return add_module(args)
    elif args.command == 'add-wiki':
        return add_wiki(args)
    elif args.command == 'add-assignment':
        return add_assignment(args)
    elif args.command == 'add-quiz':
        return add_quiz(args)
    elif args.command == 'add-discussion':
        return add_discussion(args)
    elif args.command == 'add-file':
        return add_file(args)
    elif args.command == 'list':
        return list_cartridge(args)
    elif args.command == 'package':
        return package_cartridge(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())