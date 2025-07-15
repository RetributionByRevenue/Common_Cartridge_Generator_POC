<b>todo:</b><br>
when adding to module, have optional argument about position. this will need to reorder all the items in the module's <slot>

delete by id

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

### Module-Based Content Functions (Currently Active)
These functions add content to specific modules using DataFrame-based module selection:

- `add_wiki_page_to_module()` - Adds wiki pages to modules
- `add_assignment_to_module()` - Adds assignments to modules  
- `add_quiz_to_module()` - Adds quizzes to modules
- `add_discussion_to_module()` - Adds discussion topics to modules
- `add_file_to_module()` - Adds file attachments to modules

### Standalone Content Functions 
These functions create content not attached to any module:

- `add_standalone_discussion()` - Creates standalone discussion topics
- `add_file_standalone()` - Creates standalone files
- `add_standalone_wiki_page()` - Creates standalone wiki pages
- `add_assignment()` - Creates standalone assignments
- `add_quiz()` - Creates standalone quizzes

## Key Features

- **DataFrame-based module selection**: Use `generator.df` to query and select modules by title or other attributes
- **Automatic state management**: All functions automatically update cartridge files and scan current state
- **Canvas-compatible**: Generates proper Canvas Common Cartridge XML structure
- **Flexible content creation**: Support for both module-attached and standalone content

## Output

The script generates:
- Complete cartridge directory structure
- Zipped cartridge file (`generated_cartridge.zip`)
- HTML inspection file (`table_inspect.html`) showing cartridge structure
