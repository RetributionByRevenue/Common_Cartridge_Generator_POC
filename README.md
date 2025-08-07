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

## 📦 Package & List Cartridge

<table>
  <tr><td><code>.venv/bin/python cartridge_cli.py package test_cartridge</code></td></tr>
  <tr><td><code>.venv/bin/python cartridge_cli.py list test_cartridge</code></td></tr>
</table>
