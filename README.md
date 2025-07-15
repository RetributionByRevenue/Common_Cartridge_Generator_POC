<b>todo:</b><br>
when adding to module, have optional argument about position. this will need to reorder all the items in the module's <slot>

delete by id

## Common Cartridge Generator (PoC)

This Python script (`generator.py`) is a Proof of Concept (PoC) for generating IMS Common Cartridge (`.imscc`) files.

<img src="https://raw.githubusercontent.com/RetributionByRevenue/Common_Cartridge_Generator_POC/refs/heads/main/Result.PNG" width=380 height=400>

### What it Does

The script automates the creation of a basic Common Cartridge structure, including:
- Initializing `imsmanifest.xml` and `module_meta.xml`.
- Adding various content types (Wiki Pages, Quizzes, Assignments, Files, Discussions) within modules.
- Packaging the generated content and metadata into a `.imscc` (ZIP) file.

### Supported Content Types

The script can generate modules containing the following items:

| Modules |
| :----------- |
| Wiki Pages   |
| Assignments  |
| Quizzes      |
| Files        |
| Discussions  |

### How to Run

1.  Ensure you have Python 3 installed.
2.  Install the `lxml` library:
    ```bash
    pip install lxml
    ```
3.  Execute the script:
    ```bash
    python generator.py
    ```

### Output

Upon successful execution, a `current_project` directory will be created containing the generated XML files and content, which is then zipped into `working_cartridge.zip` within the same directory.

### Verification

The structure of the generated `working_cartridge.zip` (which is an `.imscc` file) can be verified by uploading it to the Common Cartridge Viewer (https://common-cartridge-viewer.netlify.app/#/). The viewer confirms that the script creates the expected module and content structure.
