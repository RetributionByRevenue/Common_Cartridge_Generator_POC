# 🧾 Cartridge CLI Example Commands

This README provides example commands for using `cartridge_cli.py` to create new or edit existing unzipped IMS Common Cartridge courses. Commands are grouped by action type for clarity.

---

## Install

**Examples:**
```bash
python -m venv .venv && pip install pandas
```

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
