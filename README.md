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

- `add_wiki_page_to_module(position=None)` - Adds wiki pages to modules
- `add_assignment_to_module(position=None)` - Adds assignments to modules  
- `add_quiz_to_module(position=None)` - Adds quizzes to modules
- `add_discussion_to_module(position=None)` - Adds discussion topics to modules
- `add_file_to_module(position=None)` - Adds file attachments to modules

### Standalone Content Functions 
These functions create content not attached to any module:

- `add_wiki_page_standalone()` - Creates standalone wiki pages
- `add_assignment_standalone()` - Creates standalone assignments
- `add_quiz_standalone()` - Creates standalone quizzes
- `add_discussion_standalone()` - Creates standalone discussion topics
- `add_file_standalone()` - Creates standalone files

## Key Features

### Position Control
All module-based functions now support an optional `position` parameter:
- **1-based indexing**: `position=1` means first position, `position=2` means second position, etc.
- **Gap prevention**: Positions are automatically kept consecutive (1, 2, 3, 4, 5...)
- **Automatic reordering**: Existing items automatically shift to accommodate new insertions
- **Default behavior**: Without position parameter, items are added to the end

**Examples:**
```python
# Add to end of module (default behavior)
generator.add_wiki_page_to_module(module_id, "Page Title", "Content")

# Insert at specific position
generator.add_wiki_page_to_module(module_id, "Page Title", "Content", position=1)  # First position
generator.add_assignment_to_module(module_id, "Assignment", "Content", position=3)  # Third position
```

### Other Features
- **DataFrame-based module selection**: Use `generator.df` to query and select modules by title or other attributes
- **Automatic state management**: All functions automatically update cartridge files and scan current state
- **Canvas-compatible**: Generates proper Canvas Common Cartridge XML structure
- **Flexible content creation**: Support for both module-attached and standalone content
- **XML synchronization**: Both `module_meta.xml` and `imsmanifest.xml` maintain perfect ordering

## Output

The script generates:
- Complete cartridge directory structure
- Zipped cartridge file (`generated_cartridge.zip`)
- HTML inspection file (`table_inspect.html`) showing cartridge structure
