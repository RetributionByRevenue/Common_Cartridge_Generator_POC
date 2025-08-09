# 🧾 Cartridge CLI Example Commands

This README provides example commands for using `cartridge_cli.py` to create and manage an IMS Common Cartridge package. Commands are grouped by action type for clarity.

---

## 🧱 Create Cartridge

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py create test_cartridge --title "Test Course" --code "TEST101"</code></td></tr>
</table>

---

## 📦 Create Module

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-module test_cartridge --title "Week 1" --position 1 --published true</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-module test_cartridge --title "Week 2" --position 2 --published true</code></td></tr>
</table>

---

## 📝 Add All 5 Content Types

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-quiz test_cartridge --module "Week 1" --title "Test Quiz 1" --description "This is a test quiz" --points 10</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-discussion test_cartridge --module "Week 1" --title "My Discussion Topic 88" --description "Lets talk abou8t the birds and the bees."</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-file test_cartridge --module "Week 1" --filename "document3.txt" --content "File content here"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-wiki test_cartridge --module "Week 1" --title "booga2" --content "This is a test wiki page that we will delete."</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py add-assignment test_cartridge --module "Week 1" --title "Assignment 2" --content "Write and essay on the history of pokemon." --points 50</code></td></tr>
</table>

---

## ❌ Delete Content Types (including Modules)

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-quiz test_cartridge --title "Test Quiz 1"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-discussion test_cartridge --title "My Discussion Topic 3"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-file test_cartridge --filename "document33.txt"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-wiki test_cartridge --title "booga2"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-assignment test_cartridge --title "Assignment 2"</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py delete-module test_cartridge --title "Week 1"</code></td></tr>
</table>

---

## ✏️ Update Content and Modules

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-wiki test_cartridge --title "original title" --new-title "New Title" --content "New content" --published true --position 2</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-assignment test_cartridge --title "Assignment 1" --new-title "Updated Assignment" --content "New assignment content" --points 75 --published true --position 1</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-file test_cartridge --filename "document.txt" --new-filename "updated_document.txt" --content "New file content" --position 3</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-discussion test_cartridge --title "original discussion" --new-title "Updated Discussion Title" --content "New discussion content" --published true --position 2</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-quiz test_cartridge --title "Test Quiz 1" --new-title "Updated Quiz Title" --description "This is an updated quiz description" --points 15 --published true --position 1</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py update-module test_cartridge --title "Week 1" --new-title "Introduction Module"</code></td></tr>
</table>

---

## Copying

**Examples:**
```bash
#copy wiki page
.venv/bin/python cartridge_cli.py copy-wiki test_cartridge --title "Copy Wiki" --target-module "init_module_b"

#copy assignment
.venv/bin/python cartridge_cli.py copy-assignment test_cartridge --title "Copy Assignment" --target-module "init_module_b"

#copy discussion
.venv/bin/python cartridge_cli.py copy-discussion test_cartridge --title "Copy Discussion" --target-module "init_module_b"

#copy quiz
.venv/bin/python cartridge_cli.py copy-quiz test_cartridge --title "Copy Quiz" --target-module "init_module_b"

#copy file
.venv/bin/python cartridge_cli.py copy-file test_cartridge --filename "copy-file.txt" --target-module "init_module_b"
```

## Display

**Examples:**
```bash
#display wiki page
.venv/bin/python cartridge_cli.py display-wiki test_cartridge --title "Copy Wiki"

#display assignment
.venv/bin/python cartridge_cli.py display-assignment test_cartridge --title "Copy Assignment"

#display discussion
.venv/bin/python cartridge_cli.py display-discussion test_cartridge --title "Copy Discussion" 

#display quiz
.venv/bin/python cartridge_cli.py display-quiz test_cartridge --title "Copy Quiz"

#display file
.venv/bin/python cartridge_cli.py display-file test_cartridge --filename "copy-file.txt"
```

## 📦 Package & List Cartridge

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py package test_cartridge</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py list test_cartridge</code></td></tr>
</table>

**Examples:**
```bash
  # Remove existing test cartridge if it exists
  rm -rf test_cartridge

  # Create base cartridge
  .venv/bin/python cartridge_cli.py create test_cartridge --title "Comprehensive Test Course" --code "TEST101"

  # === MODULE 1: TESTING ADDING FUNCTIONALITY ===
  .venv/bin/python cartridge_cli.py add-module test_cartridge --title "testing adding functionality" --position 1

  # Add 5 content types to testing adding functionality module
  .venv/bin/python cartridge_cli.py add-wiki test_cartridge --module "testing adding functionality" --title "Test Wiki" --content "This is a test wiki page"
  .venv/bin/python cartridge_cli.py add-assignment test_cartridge --module "testing adding functionality" --title "Test Assignment" --content "This is a test assignment" --points 100
  .venv/bin/python cartridge_cli.py add-discussion test_cartridge --module "testing adding functionality" --title "Test Discussion" --description "This is a test discussion"
  .venv/bin/python cartridge_cli.py add-quiz test_cartridge --module "testing adding functionality" --title "Test Quiz" --description "This is a test quiz" --points 50
  .venv/bin/python cartridge_cli.py add-file test_cartridge --module "testing adding functionality" --filename "test-file.txt" --content "This is a test file"

  # === MODULE 2: TESTING DELETE FUNCTIONALITY ===
  .venv/bin/python cartridge_cli.py add-module test_cartridge --title "testing delete functionality" --position 2

  # Add 5 content types to testing delete functionality module
  .venv/bin/python cartridge_cli.py add-wiki test_cartridge --module "testing delete functionality" --title "Delete Wiki" --content "This wiki will be deleted"
  .venv/bin/python cartridge_cli.py add-assignment test_cartridge --module "testing delete functionality" --title "Delete Assignment" --content "This assignment will be deleted" --points 75
  .venv/bin/python cartridge_cli.py add-discussion test_cartridge --module "testing delete functionality" --title "Delete Discussion" --description "This discussion will be deleted"
  .venv/bin/python cartridge_cli.py add-quiz test_cartridge --module "testing delete functionality" --title "Delete Quiz" --description "This quiz will be deleted" --points 25
  .venv/bin/python cartridge_cli.py add-file test_cartridge --module "testing delete functionality" --filename "delete-file.txt" --content "This file will be deleted"

  # Delete all 5 content types from testing delete functionality module (should be empty at the end)
  .venv/bin/python cartridge_cli.py delete-wiki test_cartridge --title "Delete Wiki"
  .venv/bin/python cartridge_cli.py delete-assignment test_cartridge --title "Delete Assignment"
  .venv/bin/python cartridge_cli.py delete-discussion test_cartridge --title "Delete Discussion"
  .venv/bin/python cartridge_cli.py delete-quiz test_cartridge --title "Delete Quiz"
  .venv/bin/python cartridge_cli.py delete-file test_cartridge --filename "delete-file.txt"

  # === MODULE 3: TESTING UPDATE FUNCTIONALITY ===
  .venv/bin/python cartridge_cli.py add-module test_cartridge --title "testing update functionality" --position 3

  # Add 5 content types to testing update functionality module
  .venv/bin/python cartridge_cli.py add-wiki test_cartridge --module "testing update functionality" --title "Update Wiki" --content "Original wiki content"
  .venv/bin/python cartridge_cli.py add-assignment test_cartridge --module "testing update functionality" --title "Update Assignment" --content "Original assignment content" --points 80
  .venv/bin/python cartridge_cli.py add-discussion test_cartridge --module "testing update functionality" --title "Update Discussion" --description "Original discussion content"
  .venv/bin/python cartridge_cli.py add-quiz test_cartridge --module "testing update functionality" --title "Update Quiz" --description "Original quiz content" --points 40
  .venv/bin/python cartridge_cli.py add-file test_cartridge --module "testing update functionality" --filename "update-file.txt" --content "Original file content"

  # Update all 5 content types in testing update functionality module
  .venv/bin/python cartridge_cli.py update-wiki test_cartridge --title "Update Wiki" --new-title "Updated Wiki Title" --content "UPDATED wiki content" --position 1
  .venv/bin/python cartridge_cli.py update-assignment test_cartridge --title "Update Assignment" --new-title "Updated Assignment Title" --content "UPDATED assignment content" --points 150 --position 2
  .venv/bin/python cartridge_cli.py update-discussion test_cartridge --title "Update Discussion" --new-title "Updated Discussion Title" --content "UPDATED discussion content" --position 3
  .venv/bin/python cartridge_cli.py update-quiz test_cartridge --title "Update Quiz" --new-title "Updated Quiz Title" --description "UPDATED quiz content" --points 60 --position 4
  .venv/bin/python cartridge_cli.py update-file test_cartridge --filename "update-file.txt" --new-filename "updated-file.txt" --content "UPDATED file content" --position 5

  # === MODULE 4 & 5: TESTING COPY FUNCTIONALITY ===
  .venv/bin/python cartridge_cli.py add-module test_cartridge --title "init_module_a" --position 4
  .venv/bin/python cartridge_cli.py add-module test_cartridge --title "init_module_b" --position 5

  # Add 5 content types to init_module_a
  .venv/bin/python cartridge_cli.py add-wiki test_cartridge --module "init_module_a" --title "Copy Wiki" --content "This wiki will be copied"
  .venv/bin/python cartridge_cli.py add-assignment test_cartridge --module "init_module_a" --title "Copy Assignment" --content "This assignment will be copied" --points 90
  .venv/bin/python cartridge_cli.py add-discussion test_cartridge --module "init_module_a" --title "Copy Discussion" --description "This discussion will be copied"
  .venv/bin/python cartridge_cli.py add-quiz test_cartridge --module "init_module_a" --title "Copy Quiz" --description "This quiz will be copied" --points 35
  .venv/bin/python cartridge_cli.py add-file test_cartridge --module "init_module_a" --filename "copy-file.txt" --content "This file will be copied"

  # Copy all 5 content types from init_module_a to init_module_b
  .venv/bin/python cartridge_cli.py copy-wiki test_cartridge --title "Copy Wiki" --target-module "init_module_b"
  .venv/bin/python cartridge_cli.py copy-assignment test_cartridge --title "Copy Assignment" --target-module "init_module_b"
  .venv/bin/python cartridge_cli.py copy-discussion test_cartridge --title "Copy Discussion" --target-module "init_module_b"
  .venv/bin/python cartridge_cli.py copy-quiz test_cartridge --title "Copy Quiz" --target-module "init_module_b"
  .venv/bin/python cartridge_cli.py copy-file test_cartridge --filename "copy-file.txt" --target-module "init_module_b"

  # === LIST AND ZIP ===
  # List final cartridge contents
  .venv/bin/python cartridge_cli.py list test_cartridge

  # Package cartridge into ZIP file
  .venv/bin/python cartridge_cli.py package test_cartridge
```

# Canvas Import Result
<img src="https://raw.githubusercontent.com/RetributionByRevenue/Common_Cartridge_Generator_POC/refs/heads/main/Screenshot_2025-08-09_19-14-05.png">

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
