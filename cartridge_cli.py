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
    """Add a wiki page to a module or as standalone in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Check if module is specified
    if hasattr(args, 'module') and args.module:
        # Module-attached mode
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
    else:
        # Standalone mode
        print(f"Adding standalone wiki page '{args.title}' to cartridge '{args.cartridge_name}'")
        generator.add_wiki_page_standalone(args.title, page_content=args.content, published=True)
        
        print(f"✓ Standalone wiki page '{args.title}' added successfully")
        print(f"  Mode: Standalone (not attached to any module)")
        print(f"  Content length: {len(args.content)} characters")
        print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_assignment(args):
    """Add an assignment to a module or as standalone in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Check if module is specified
    if hasattr(args, 'module') and args.module:
        # Module-attached mode
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
    else:
        # Standalone mode
        print(f"Adding standalone assignment '{args.title}' to cartridge '{args.cartridge_name}'")
        generator.add_assignment_standalone(args.title, assignment_content=args.content, points=args.points, published=True)
        
        print(f"✓ Standalone assignment '{args.title}' added successfully")
        print(f"  Mode: Standalone (not attached to any module)")
        print(f"  Points: {args.points}")
        print(f"  Content length: {len(args.content)} characters")
        print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_quiz(args):
    """Add a quiz to a module or as standalone in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Check if module is specified
    if hasattr(args, 'module') and args.module:
        # Module-attached mode
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
    else:
        # Standalone mode
        print(f"Adding standalone quiz '{args.title}' to cartridge '{args.cartridge_name}'")
        generator.add_quiz_standalone(args.title, quiz_description=args.description, points=args.points, published=True)
        
        print(f"✓ Standalone quiz '{args.title}' added successfully")
        print(f"  Mode: Standalone (not attached to any module)")
        print(f"  Points: {args.points}")
        print(f"  Description length: {len(args.description)} characters")
        print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_discussion(args):
    """Add a discussion to a module or as standalone in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Check if module is specified
    if hasattr(args, 'module') and args.module:
        # Module-attached mode
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
    else:
        # Standalone mode
        print(f"Adding standalone discussion '{args.title}' to cartridge '{args.cartridge_name}'")
        generator.add_discussion_standalone(args.title, args.description, published=True)
        
        print(f"✓ Standalone discussion '{args.title}' added successfully")
        print(f"  Mode: Standalone (not attached to any module)")
        print(f"  Description length: {len(args.description)} characters")
        print(f"  Total components: {len(generator.df)}")
    
    return 0


def add_file(args):
    """Add a file to a module or as standalone in an existing cartridge"""
    cartridge_path = Path(args.cartridge_name)
    
    if not cartridge_path.exists():
        print(f"Error: Cartridge '{args.cartridge_name}' does not exist")
        return 1
    
    # Load existing cartridge
    generator = CartridgeGenerator("temp", "temp")  # Will be overridden during hydration
    if not generator.hydrate_from_existing_cartridge(args.cartridge_name):
        print("Failed to load existing cartridge")
        return 1
    
    # Check if module is specified
    if hasattr(args, 'module') and args.module:
        # Module-attached mode
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
    else:
        # Standalone mode
        print(f"Adding standalone file '{args.filename}' to cartridge '{args.cartridge_name}'")
        generator.add_file_standalone(args.filename, args.content)
        
        print(f"✓ Standalone file '{args.filename}' added successfully")
        print(f"  Mode: Standalone (not attached to any module)")
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
        for _, module in modules.iterrows():
            print(f"  📁 {module['title']} (ID: {module['identifier']})")
            
            # Find items in this module (this is simplified - in real implementation you'd need proper module-item mapping)
            module_items = generator.df[generator.df["type"] == "module_item"]
            if not module_items.empty:
                for _, item in module_items.iterrows():
                    content_type = item.get('content_type', 'Unknown')
                    icons = {
                        "WikiPage": "📄",
                        "Assignment": "📝", 
                        "Quiz": "❓",
                        "Discussion": "💬",
                        "File": "📎"
                    }
                    icon = icons.get(content_type, "❓")
                    print(f"    {icon} {item['title']} ({content_type})")
    
    # List component types
    print("\nComponent breakdown:")
    for comp_type, count in summary['component_types'].items():
        print(f"  {comp_type}: {count}")
    
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
    wiki_parser.add_argument('--module', help='Module title to add wiki page to (optional - if not specified, creates standalone wiki page)')
    wiki_parser.add_argument('--title', required=True, help='Wiki page title')
    wiki_parser.add_argument('--content', required=True, help='Wiki page content')
    
    # Add-assignment command
    assignment_parser = subparsers.add_parser('add-assignment', help='Add an assignment to a module')
    assignment_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    assignment_parser.add_argument('--module', help='Module title to add assignment to (optional - if not specified, creates standalone assignment)')
    assignment_parser.add_argument('--title', required=True, help='Assignment title')
    assignment_parser.add_argument('--content', required=True, help='Assignment content/description')
    assignment_parser.add_argument('--points', type=int, default=100, help='Points possible (default: 100)')
    
    # Add-quiz command
    quiz_parser = subparsers.add_parser('add-quiz', help='Add a quiz to a module')
    quiz_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    quiz_parser.add_argument('--module', help='Module title to add quiz to (optional - if not specified, creates standalone quiz)')
    quiz_parser.add_argument('--title', required=True, help='Quiz title')
    quiz_parser.add_argument('--description', required=True, help='Quiz description')
    quiz_parser.add_argument('--points', type=int, default=10, help='Points possible (default: 10)')
    
    # Add-discussion command
    discussion_parser = subparsers.add_parser('add-discussion', help='Add a discussion to a module')
    discussion_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    discussion_parser.add_argument('--module', help='Module title to add discussion to (optional - if not specified, creates standalone discussion)')
    discussion_parser.add_argument('--title', required=True, help='Discussion title')
    discussion_parser.add_argument('--description', required=True, help='Discussion description/prompt')
    
    # Add-file command
    file_parser = subparsers.add_parser('add-file', help='Add a file to a module')
    file_parser.add_argument('cartridge_name', help='Name of the cartridge directory')
    file_parser.add_argument('--module', help='Module title to add file to (optional - if not specified, creates standalone file)')
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