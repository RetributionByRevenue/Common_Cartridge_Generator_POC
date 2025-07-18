# Canvas Common Cartridge Generator

This tool generates Canvas Common Cartridge packages with various content types. The main script demonstrates the available functions by creating a sample cartridge with modules and different content types.

## Usage

```bash
python cartridge_generator.py output_directory --title "Course Title" --code "COURSE_CODE"
```

## Functions Used in Main Script

### Core Setup Functions
- `create_base_cartridge()` - Creates the basic cartridge structure and core XML files
- `add_module()` - Creates learning modules with specified titles and positions

### Module-Based Content Functions
These functions add content to specific modules using DataFrame-based module selection:

- `add_wiki_page_to_module(module_id, page_title, page_content="", published=True, position=None)` - Adds wiki pages to modules
- `add_assignment_to_module(module_id, assignment_title, assignment_content="", points=100, published=True, position=None)` - Adds assignments to modules  
- `add_quiz_to_module(module_id, quiz_title, quiz_description="", points=1, published=True, position=None)` - Adds quizzes to modules
- `add_discussion_to_module(module_id, title, body, published=True, position=None)` - Adds discussion topics to modules
- `add_file_to_module(module_id, filename, file_content, position=None)` - Adds file attachments to modules

### Standalone Content Functions 
These functions create content not attached to any module:

- `add_wiki_page_standalone(page_title, page_content="", published=True)` - Creates standalone wiki pages
- `add_assignment_standalone(assignment_title, assignment_content="", points=100, published=True)` - Creates standalone assignments
- `add_quiz_standalone(quiz_title, quiz_description="", points=1, published=True)` - Creates standalone quizzes
- `add_discussion_standalone(title, body, published=True)` - Creates standalone discussion topics
- `add_file_standalone(filename, file_content)` - Creates standalone files

## Key Features

### Position Control
All module-based functions now support an optional `position` parameter:
- **1-based indexing**: `position=1` means first position, `position=2` means second position, etc.
- **Gap prevention**: Positions are automatically kept consecutive (1, 2, 3, 4, 5...)
- **Automatic reordering**: Existing items automatically shift to accommodate new insertions
- **Default behavior**: Without position parameter, items are added to the end

**Examples:**
```python
    # Create generator
    generator = CartridgeGenerator(args.title, args.code)
    
    # Create base cartridge
    print(f"Creating base cartridge: {args.output_dir}")
    generator.create_base_cartridge(args.output_dir)
    
    # Add modules
    print("Adding module...")
    module_id_test1 = generator.add_module("module1", position=1, published=True)

    selected_module_1_id = (generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "module1")]).identifier.item()

    #adding content into module
    generator.add_wiki_page_to_module(selected_module_1_id, "test_page 1", page_content="haha", published=True, position=None)
    generator.add_assignment_to_module(selected_module_1_id, "assignment_title", assignment_content="test", points=100, published=True, position=None)
    generator.add_quiz_to_module(selected_module_1_id, "quiz_title", quiz_description="test", points=1, published=True, position=None)
    generator.add_discussion_to_module(selected_module_1_id, "title", "dy", published=True, position=None)
    generator.add_file_to_module(selected_module_1_id, "filename", "file_content", position=None)
    
    generator.add_wiki_page_to_module(selected_module_1_id, "test_page2", page_content="haha", published=True, position=None)
    generator.add_assignment_to_module(selected_module_1_id, "assignment_title2", assignment_content="test", points=100, published=True, position=None)
    generator.add_quiz_to_module(selected_module_1_id, "quiz_title2", quiz_description="test", points=1, published=True, position=None)
    generator.add_discussion_to_module(selected_module_1_id, "title2", "dy", published=True, position=None)
    generator.add_file_to_module(selected_module_1_id, "filename2", "file_content", position=None)

    # Wiki pages - select by type and title
    selected_wiki = (generator.df[(generator.df["type"] == "wiki_page") & (generator.df["title"] == "test_page2")]).identifier.item()
    # Assignments - select by type and title  
    selected_assignment = (generator.df[(generator.df["type"] == "assignment_settings") & (generator.df["title"] == "assignment_title2")]).identifier.item()
    # Quizzes - select by type and title
    selected_quiz = (generator.df[(generator.df["type"] == "qti_assessment") & (generator.df["title"] == "quiz_title2")]).iloc[0]['identifier']
    # Files - select by type and href (file path)
    selected_file = (generator.df[(generator.df["type"] == "resource") & (generator.df["href"] == "web_resources/filename2")]).identifier.item()
    # Discussions - select by type and title
    selected_discussion = (generator.df[(generator.df["type"] == "resource") & (generator.df["title"] == "title2")]).identifier.item()

    # Delete wiki page
    generator.delete_wiki_page_by_id(selected_wiki)
    # Delete assignment  
    generator.delete_assignment_by_id(selected_assignment)
    # Delete quiz
    generator.delete_quiz_by_id(selected_quiz)
    # Delete file
    generator.delete_file_by_id(selected_file)
    # Delete discussion
    generator.delete_discussion_by_id(selected_discussion)
```

### Other Features
- **DataFrame-based module selection**: Use `generator.df` to query and select modules by title or other attributes
- **Automatic state management**: All functions automatically update cartridge files and scan current state
- **Canvas-compatible**: Generates proper Canvas Common Cartridge XML structure
- **Flexible content creation**: Support for both module-attached and standalone content
- **XML synchronization**: Both `module_meta.xml` and `imsmanifest.xml` maintain perfect ordering

## Content Deletion

The tool provides deletion functions for removing content from cartridges. Each content type has its own selection method and deletion function.

### Content Selection Methods

Use these patterns to select content for deletion from the DataFrame:

```python
# Wiki pages - select by type and title
selected_wiki = (generator.df[(generator.df["type"] == "wiki_page") & (generator.df["title"] == "page_name")]).identifier.item()

# Assignments - select by type and title  
selected_assignment = (generator.df[(generator.df["type"] == "assignment_settings") & (generator.df["title"] == "assignment_name")]).identifier.item()

# Quizzes - select by type and title
selected_quiz = (generator.df[(generator.df["type"] == "qti_assessment") & (generator.df["title"] == "quiz_title2")]).iloc[0]['identifier']

# Files - select by type and href (file path)
selected_file = (generator.df[(generator.df["type"] == "resource") & (generator.df["href"] == "web_resources/filename.txt")]).identifier.item()

# Discussions - select by type and title
selected_discussion = (generator.df[(generator.df["type"] == "resource") & (generator.df["title"] == "discussion_name")]).identifier.item()
```

### Deletion Functions

Once content is selected, use these functions to delete it:

```python
# Delete wiki page
generator.delete_wiki_page_by_id(selected_wiki)

# Delete assignment  
generator.delete_assignment_by_id(selected_assignment)

# Delete quiz
generator.delete_quiz_by_id(selected_quiz)

# Delete file
generator.delete_file_by_id(selected_file)

# Delete discussion
generator.delete_discussion_by_id(selected_discussion)
```

### Module Deletion

Delete an entire module and all its contents:

```python
# Get module ID
module_id = generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "module1")].identifier.item()

# Delete entire module and all its contents
generator.delete_module_by_id(module_id)
```

The `delete_module_by_id()` function:
- Deletes all content inside the module (wiki pages, assignments, quizzes, discussions, files)
- Uses existing deletion methods for each content type
- Removes the empty module from all structures
- Provides comprehensive cleanup with error handling

Each deletion function:
- Removes content from internal data structures
- Cleans up XML references in manifest and module files
- Deletes physical files and directories
- Adjusts position numbering for remaining module items
- Updates cartridge state automatically

## Content Updates

The tool provides update functions for modifying existing content without deleting and recreating it. Each content type has its own update method.

### Update Functions

```python
# Update wiki page
generator.update_wiki(wiki_id, page_title="New Title", page_content="New content", published=True)

# Update assignment
generator.update_assignment(assignment_id, assignment_title="New Title", assignment_content="New content", points=150, published=True)

# Update quiz
generator.update_quiz(quiz_id, quiz_title="New Title", quiz_description="New description", points=5, published=True)

# Update discussion
generator.update_discussion(discussion_id, title="New Title", body="New content", published=True)

# Update file
generator.update_file(file_id, filename="new_file.txt", file_content="New content")
```

### Update Features

All update functions support:
- **Selective Updates**: Only specify the parameters you want to change
- **Reference Synchronization**: Automatically updates all references in modules and organization items
- **State Consistency**: Maintains proper workflow states across all structures
- **Detailed Logging**: Shows exactly what was changed
- **No-op Safety**: Only applies changes if values actually differ

**Examples:**
```python
# Update just the title
generator.update_wiki(wiki_id, page_title="Updated Page Title")

# Update multiple properties
generator.update_assignment(assignment_id, 
                           assignment_title="Updated Assignment",
                           points=200,
                           published=False)
```

Each update function will show you exactly what changed:
```
Wiki page 'Updated Page Title' (ID: g123...) updated: title: 'old title' → 'Updated Page Title', content updated, published: False → True
```

## Output

The script generates:
- Complete cartridge directory structure
- Zipped cartridge file (`generated_cartridge.zip`)
- HTML inspection file (`table_inspect.html`) showing cartridge structure
