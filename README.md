# Canvas Common Cartridge Generator

This tool generates Canvas Common Cartridge packages with various content types. The main script demonstrates the available functions by creating a sample cartridge with modules and different content types.

## Usage

```bash
/home/q/Desktop/test_cartridge/.venv/bin/python cartridge_generator.py generated_cartridge
```

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

    #adding set 1 content 
    generator.add_wiki_page_to_module(selected_module_1_id, "test_page", page_content="haha", published=True, position=None)
    generator.add_assignment_to_module(selected_module_1_id, "assignment_title", assignment_content="test", points=100, published=True, position=None)
    generator.add_quiz_to_module(selected_module_1_id, "quiz_title", quiz_description="test", points=1, published=True, position=None)
    generator.add_discussion_to_module(selected_module_1_id, "title", "dy", published=True, position=None)
    generator.add_file_to_module(selected_module_1_id, "filename", "file_content", position=None)
    
    #adding set 2 content 
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

    # Wiki pages - select by type and title
    selected_wiki = (generator.df[(generator.df["type"] == "wiki_page") & (generator.df["title"] == "test_page")]).identifier.item()
    # Assignments - select by type and title  
    selected_assignment = (generator.df[(generator.df["type"] == "assignment_settings") & (generator.df["title"] == "assignment_title")]).identifier.item()
    # Quizzes - select by type and title
    selected_quiz = (generator.df[(generator.df["type"] == "qti_assessment") & (generator.df["title"] == "quiz_title")]).iloc[0]['identifier']
    # Files - select by type and href (file path)
    selected_file = (generator.df[(generator.df["type"] == "resource") & (generator.df["href"] == "web_resources/filename")]).identifier.item()
    # Discussions - select by type and title
    selected_discussion = (generator.df[(generator.df["type"] == "resource") & (generator.df["title"] == "title")]).identifier.item()    
    
    # Update wiki page
    generator.update_wiki(selected_wiki, page_title="New Title", page_content="New content", published=True)
    # Update assignment
    generator.update_assignment(selected_assignment, assignment_title="New Title", assignment_content="New content", points=150, published=True)
    # Update quiz
    generator.update_quiz(selected_quiz, quiz_title="New Title", quiz_description="New description", points=5, published=True)
    # Update discussion
    generator.update_discussion(selected_discussion, title="New Title", body="New content", published=True)
    # Update file
    generator.update_file(selected_file, filename="new_file.txt", file_content="New content")

    print("Adding new module...")
    module_id_test2 = generator.add_module("module2", position=2, published=True)   
    
    #select_module
    selected_module_2_id = (generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "module2")]).identifier.item()
    
    #copy wiki page to new module
    generator.copy_wiki_page(selected_wiki, selected_module_2_id)
    #copy assignment to new module
    generator.copy_assignment(selected_assignment, selected_module_2_id)
    #copy quiz to new module
    generator.copy_quiz(selected_quiz, selected_module_2_id)
    #copy discussion to new module
    generator.copy_discussion(selected_discussion, selected_module_2_id)
    #copy file to new module
    generator.copy_file(selected_file, selected_module_2_id)
```
# Canvas Import Result
<img src="https://raw.githubusercontent.com/RetributionByRevenue/Common_Cartridge_Generator_POC/refs/heads/main/Screenshot_2025-07-24_14-30-26.png">

# Canvas Common Cartridge Methods Documentation

## CartridgeGenerator.py Methods

| Method Name | Type | Description | Parameters |
| --- | --- | --- | --- |
| \_\_init\_\_ | Constructor | Initialize the CartridgeGenerator with course title and code | course\_title, course\_code |
| df  | Property | Get current DataFrame with cartridge contents | None |
| \_update\_cartridge\_state | Private | Update internal state and DataFrame | None |
| create\_base\_cartridge | Public | Create the basic cartridge structure and core XML files | output\_dir |
| \_create\_canvas\_export\_txt | Private | Create Canvas export text file | filepath |
| \_create\_course\_settings\_xml | Private | Generate course settings XML | filepath |
| \_create\_context\_xml | Private | Generate context XML file | filepath |
| \_create\_assignment\_groups\_xml | Private | Generate assignment groups XML | filepath |
| \_create\_files\_meta\_xml | Private | Generate files metadata XML | filepath |
| \_create\_late\_policy\_xml | Private | Generate late policy XML | filepath |
| \_create\_media\_tracks\_xml | Private | Generate media tracks XML | filepath |
| \_create\_empty\_module\_meta\_xml | Private | Generate empty module metadata XML | filepath |
| add\_module | Public | Add a module to the cartridge | module\_title, position=None, published=True |
| add\_wiki\_page\_to\_module | Public | Add a wiki page to a specific module | module\_id, page\_title, page\_content="", published=True, position=None |
| delete\_wiki\_page\_by\_id | Public | Delete a wiki page by its identifier | page\_id |
| delete\_assignment\_by\_id | Public | Delete an assignment by its identifier | assignment\_id |
| delete\_quiz\_by\_id | Public | Delete a quiz by its identifier | quiz\_id |
| delete\_file\_by\_id | Public | Delete a file by its identifier | file\_id |
| delete\_discussion\_by\_id | Public | Delete a discussion by its identifier | discussion\_id |
| delete\_module\_by\_id | Public | Delete an entire module and all its contents | module\_id |
| rename\_module | Public | Rename a module by its identifier | module\_id, new\_title |
| update\_wiki | Public | Update a wiki page's properties | wiki\_id, page\_title=None, page\_content=None, published=None, position=None |
| update\_assignment | Public | Update an assignment's properties | assignment\_id, assignment\_title=None, assignment\_content=None, points=None, published=None, position=None |
| update\_quiz | Public | Update a quiz's properties | quiz\_id, quiz\_title=None, quiz\_description=None, points=None, published=None, position=None |
| update\_discussion | Public | Update a discussion's properties | discussion\_id, title=None, body=None, published=None, position=None |
| update\_file | Public | Update a file's properties | file\_id, filename=None, file\_content=None, position=None |
| add\_assignment\_to\_module | Public | Add an assignment to a specific module | module\_id, assignment\_title, assignment\_content="", points=100, published=True, position=None |
| add\_quiz\_to\_module | Public | Add a quiz to a specific module | module\_id, quiz\_title, quiz\_description="", points=1, published=True, position=None |
| add\_discussion\_to\_module | Public | Add a discussion topic to a specific module | module\_id, title, body, published=True, position=None |
| add\_assignment\_standalone | Public | Create a standalone assignment not attached to any module | assignment\_title, assignment\_content="", points=100, published=True |
| add\_quiz\_standalone | Public | Create a standalone quiz not attached to any module | quiz\_title, quiz\_description="", points=1, published=True |
| add\_wiki\_page\_standalone | Public | Create a standalone wiki page not attached to any module | page\_title, page\_content="", published=True |
| add\_discussion\_standalone | Public | Create a standalone discussion not attached to any module | title, body, published=True |
| add\_file\_to\_module | Public | Add a file to a specific module | module\_id, filename, file\_content, position=None |
| add\_file\_standalone | Public | Create a standalone file not attached to any module | filename, file\_content |
| copy\_wiki\_page | Public | Copy a wiki page to another module or as standalone | wiki\_page\_id, module\_id=None |
| copy\_assignment | Public | Copy an assignment to another module or as standalone | assignment\_id, module\_id=None |
| copy\_quiz | Public | Copy a quiz to another module or as standalone | quiz\_id, module\_id=None |
| copy\_discussion | Public | Copy a discussion to another module or as standalone | discussion\_id, module\_id=None |
| copy\_file | Public | Copy a file to another module or as standalone | file\_id, module\_id=None |
| write\_cartridge\_files | Public | Write all cartridge files to disk | output\_dir |
| \_update\_module\_meta\_xml | Private | Update module metadata XML file | filepath |
| \_create\_wiki\_page\_html | Private | Create HTML file for wiki page | filepath, page |
| \_create\_assignment\_files | Private | Create assignment XML and HTML files | output\_path, assignment |
| \_create\_quiz\_files | Private | Create quiz XML and related files | output\_path, quiz |
| \_create\_announcement\_files | Private | Create announcement/discussion XML and HTML files | output\_path, announcement |
| \_create\_web\_resource\_file | Private | Create web resource files | output\_path, file\_info |
| \_create\_imsmanifest\_xml | Private | Generate IMS manifest XML file | filepath |
| count\_files\_and\_lines | Function | Count files and lines in a directory | directory |
| main | Function | Main execution function with argument parsing | None |

  
  

## CartridgeReplicator.py Methods

| Method Name | Type | Description | Parameters |
| --- | --- | --- | --- |
| scan\_cartridge | Function | Scan an existing cartridge and extract all metadata into a DataFrame | input\_cartridge\_path |
| generate\_course\_structure | Function | Generate the complete course structure from DataFrame | df, output\_dir |
| make\_module | Function | Create module structure and files | df, output\_dir |
| add\_wiki\_page | Function | Add wiki pages to the cartridge structure | df, output\_dir |
| create\_imsmanifest | Function | Create the IMS manifest XML file | df, output\_dir |
| verify\_cartridge\_match | Function | Verify that input and output cartridges match | input\_dir, output\_dir |
| get\_file\_structure | Nested Function | Get directory structure for comparison | path |
| main | Function | Main execution function for cartridge replication | None |

  
  

## Method Categories Summary

### CartridgeGenerator.py Categories:

*   **Core Setup:** create\_base\_cartridge, \_\_init\_\_
*   **Content Creation - Module-based:** add\_wiki\_page\_to\_module, add\_assignment\_to\_module, add\_quiz\_to\_module, add\_discussion\_to\_module, add\_file\_to\_module
*   **Content Creation - Standalone:** add\_wiki\_page\_standalone, add\_assignment\_standalone, add\_quiz\_standalone, add\_discussion\_standalone, add\_file\_standalone
*   **Content Copying:** copy\_wiki\_page, copy\_assignment, copy\_quiz, copy\_discussion, copy\_file
*   **Content Updates:** update\_wiki, update\_assignment, update\_quiz, update\_discussion, update\_file
*   **Content Deletion:** delete\_wiki\_page\_by\_id, delete\_assignment\_by\_id, delete\_quiz\_by\_id, delete\_file\_by\_id, delete\_discussion\_by\_id
*   **Module Management:** add\_module, delete\_module\_by\_id, rename\_module
*   **File Generation:** write\_cartridge\_files, \_create\_imsmanifest\_xml, \_update\_module\_meta\_xml
*   **State Management:** \_update\_cartridge\_state, df property
*   **Private XML Creators:** \_create\_course\_settings\_xml, \_create\_context\_xml, \_create\_assignment\_groups\_xml, etc.

### CartridgeReplicator.py Categories:

*   **Analysis:** scan\_cartridge
*   **Generation:** generate\_course\_structure, make\_module, add\_wiki\_page, create\_imsmanifest
*   **Verification:** verify\_cartridge\_match, get\_file\_structure
*   **Execution:** main
