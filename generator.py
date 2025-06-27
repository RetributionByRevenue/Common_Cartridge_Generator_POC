import os
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
import shutil
import zipfile
from lxml import etree

def generate_uuid():
    """Generate a UUID in the format used by Canvas (i + 32 hex characters)"""
    return 'i' + uuid.uuid4().hex

def create_project_structure():
    """
    First function: Check if 'current_project' folder exists along with the 2 files.
    If not, create the directory and initialize the XML files with default data.
    """
    project_dir = "current_project"
    module_meta_file = os.path.join(project_dir, "module_meta.xml")
    manifest_file = os.path.join(project_dir, "imsmanifest.xml")
    
    # Check if directory and files exist
    if os.path.exists(project_dir) and os.path.exists(module_meta_file) and os.path.exists(manifest_file):
        print(f"Project structure already exists in '{project_dir}'")
        return project_dir, module_meta_file, manifest_file
    
    # Create directory if it doesn't exist
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"Created directory: {project_dir}")
    
    # Generate UUIDs for the project
    manifest_id = generate_uuid()
    course_title = "New Course"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create module_meta.xml with default structure (no modules initially)
    module_meta_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 http://canvas.instructure.com/xsd/cccv1p0.xsd">
</modules>'''
    
    # Create imsmanifest.xml with default structure
    manifest_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{manifest_id}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>{course_title}</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
      <lomimscc:lifeCycle>
        <lomimscc:contribute>
          <lomimscc:date>
            <lomimscc:dateTime>{current_date}</lomimscc:dateTime>
          </lomimscc:date>
        </lomimscc:contribute>
      </lomimscc:lifeCycle>
      <lomimscc:rights>
        <lomimscc:copyrightAndOtherRestrictions>
          <lomimscc:value>yes</lomimscc:value>
        </lomimscc:copyrightAndOtherRestrictions>
        <lomimscc:description>
          <lomimscc:string>Private (Copyrighted) - http://en.wikipedia.org/wiki/Copyright</lomimscc:string>
        </lomimscc:description>
      </lomimscc:rights>
    </lomimscc:lom>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules">
      </item>
    </organization>
  </organizations>
  <resources>
  </resources>
</manifest>'''
    
    # Write the files
    with open(module_meta_file, 'w', encoding='utf-8') as f:
        f.write(module_meta_xml)
    print(f"Created: {module_meta_file}")
    
    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write(manifest_xml)
    print(f"Created: {manifest_file}")
    
    return project_dir, module_meta_file, manifest_file

def add_module_with_content(module_meta_file, manifest_file, module_title="Module 1", content_items=None):
    """
    Second function: Add a module with content items to both XML files.
    Updates both module_meta.xml and imsmanifest.xml with matching UUIDs.
    Creates the actual HTML file for the wiki page.
    """
    if content_items is None:
        content_items = [{'type': 'page', 'title': 'Wiki Page 1'}]

    # Generate UUID for the module
    module_id = generate_uuid()
    
    # Get project directory from the file path
    project_dir = os.path.dirname(module_meta_file)
    
    # --- Update module_meta.xml ---
    try:
        tree = ET.parse(module_meta_file)
        root = tree.getroot()
        
        module = ET.SubElement(root, 'module')
        module.set('identifier', module_id)
        
        ET.SubElement(module, 'title').text = module_title
        ET.SubElement(module, 'workflow_state').text = 'active'
        ET.SubElement(module, 'position').text = str(len(root.findall('module')))
        ET.SubElement(module, 'locked').text = 'false'
        
        items = ET.SubElement(module, 'items')
    except ET.ParseError as e:
        print(f"Error parsing {module_meta_file}: {e}")
        return False
    
    # --- Update imsmanifest.xml ---
    try:
        manifest_tree = ET.parse(manifest_file)
        manifest_root = manifest_tree.getroot()
        
        ns = {'': 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1'}
        learning_modules = manifest_root.find('.//item[@identifier="LearningModules"]', ns)
        
        module_item_org = ET.SubElement(learning_modules, 'item')
        module_item_org.set('identifier', module_id)
        ET.SubElement(module_item_org, 'title').text = module_title
        
        resources = manifest_root.find('.//resources', ns)
    except ET.ParseError as e:
        print(f"Error parsing {manifest_file}: {e}")
        return False

    # --- Process content items ---
    for i, content_def in enumerate(content_items):
        content_type = content_def['type']
        content_title = content_def['title']
        position = str(i + 1)
        item_id = generate_uuid()
        resource_id = generate_uuid()

        if content_type == 'page':
            # Add item to module_meta.xml
            item = ET.SubElement(items, 'item')
            item.set('identifier', item_id)
            ET.SubElement(item, 'content_type').text = 'WikiPage'
            ET.SubElement(item, 'workflow_state').text = 'active'
            ET.SubElement(item, 'title').text = content_title
            ET.SubElement(item, 'identifierref').text = resource_id
            ET.SubElement(item, 'position').text = position
            ET.SubElement(item, 'new_tab').text = 'false'
            ET.SubElement(item, 'indent').text = '0'

            # Create HTML file
            wiki_content_dir = os.path.join(project_dir, 'wiki_content')
            os.makedirs(wiki_content_dir, exist_ok=True)
            html_filename = f'{content_title.lower().replace(" ", "-")}.html'
            html_filepath = os.path.join(wiki_content_dir, html_filename)
            html_content = f'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{content_title}</title>
<meta name="identifier" content="{resource_id}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="active"/>
</head>
<body>
<h1>Hello World</h1>
<p>This is a test wiki page created by the Common Cartridge generator.</p>
<p>Page title: {content_title}</p>
<p>Resource ID: {resource_id}</p>
</body>
</html>'''
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Created HTML file: {html_filepath}")

            # Add item to imsmanifest.xml organizations
            page_item_org = ET.SubElement(module_item_org, 'item')
            page_item_org.set('identifier', item_id)
            page_item_org.set('identifierref', resource_id)
            ET.SubElement(page_item_org, 'title').text = content_title

            # Add resource to imsmanifest.xml resources
            resource = ET.SubElement(resources, 'resource')
            resource.set('identifier', resource_id)
            resource.set('type', 'webcontent')
            resource.set('href', f'wiki_content/{html_filename}')
            file_elem = ET.SubElement(resource, 'file')
            file_elem.set('href', f'wiki_content/{html_filename}')

        elif content_type == 'assignment':
            # Add item to module_meta.xml
            item = ET.SubElement(items, 'item')
            item.set('identifier', item_id)
            ET.SubElement(item, 'content_type').text = 'Assignment'
            ET.SubElement(item, 'workflow_state').text = 'active'
            ET.SubElement(item, 'title').text = content_title
            ET.SubElement(item, 'identifierref').text = resource_id
            ET.SubElement(item, 'position').text = position
            ET.SubElement(item, 'new_tab').text = 'false'
            ET.SubElement(item, 'indent').text = '0'

            # Add item to imsmanifest.xml organizations
            assignment_item_org = ET.SubElement(module_item_org, 'item')
            assignment_item_org.set('identifier', item_id)
            assignment_item_org.set('identifierref', resource_id)
            ET.SubElement(assignment_item_org, 'title').text = content_title

            # Create assignment files and directories
            assignment_dir = os.path.join(project_dir, resource_id)
            os.makedirs(assignment_dir, exist_ok=True)

            # Create assignment settings XML
            settings_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{resource_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 http://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{content_title}</title>
  <points_possible>100</points_possible>
  <grading_type>points</grading_type>
  <submission_types>online_text_entry</submission_types>
  <workflow_state>unpublished</workflow_state>
  <due_at>2024-12-31T23:59:59Z</due_at>
  <unlock_at>2024-01-01T00:00:00Z</unlock_at>
  <lock_at>2024-12-31T23:59:59Z</lock_at>
  <description>
    <![CDATA[<p>This is a sample assignment. Please replace this with your assignment description.</p>]]>
  </description>
</assignment>'''

            settings_filename = 'assignment_settings.xml'
            settings_filepath = os.path.join(assignment_dir, settings_filename)
            with open(settings_filepath, 'w', encoding='utf-8') as f:
                f.write(settings_content)
            print(f"Created assignment settings file: {settings_filepath}")

            # Create assignment resource in imsmanifest.xml
            resource = ET.SubElement(resources, 'resource')
            resource.set('identifier', resource_id)
            resource.set('type', 'associatedcontent/imscc_xmlv1p1/learning-application-resource')
            resource.set('href', f'{resource_id}/{settings_filename}')
            file_elem = ET.SubElement(resource, 'file')
            file_elem.set('href', f'{resource_id}/{settings_filename}')


        elif content_type == 'file':
            # Add item to module_meta.xml
            item = ET.SubElement(items, 'item')
            item.set('identifier', item_id)
            ET.SubElement(item, 'content_type').text = 'Attachment'
            ET.SubElement(item, 'workflow_state').text = 'active'
            ET.SubElement(item, 'title').text = content_title
            ET.SubElement(item, 'identifierref').text = resource_id
            ET.SubElement(item, 'position').text = position
            ET.SubElement(item, 'new_tab').text = 'false'
            ET.SubElement(item, 'indent').text = '0'

            # Create the actual file
            files_dir = os.path.join(project_dir, 'web_resources')
            os.makedirs(files_dir, exist_ok=True)
            file_filepath = os.path.join(files_dir, content_title)
            with open(file_filepath, 'w', encoding='utf-8') as f:
                f.write("hello world")
            print(f"Created file: {file_filepath}")

            # Add item to imsmanifest.xml organizations
            file_item_org = ET.SubElement(module_item_org, 'item')
            file_item_org.set('identifier', item_id)
            file_item_org.set('identifierref', resource_id)
            ET.SubElement(file_item_org, 'title').text = content_title

            # Add resource to imsmanifest.xml resources
            resource = ET.SubElement(resources, 'resource')
            resource.set('identifier', resource_id)
            resource.set('type', 'webcontent')
            resource.set('href', f'web_resources/{content_title}')
            file_elem = ET.SubElement(resource, 'file')
            file_elem.set('href', f'web_resources/{content_title}')

        elif content_type == 'quiz':
            dependency_id = generate_uuid()
            
            # Add item to module_meta.xml
            item = ET.SubElement(items, 'item')
            item.set('identifier', item_id)
            ET.SubElement(item, 'content_type').text = 'Quizzes::Quiz'
            ET.SubElement(item, 'workflow_state').text = 'active'
            ET.SubElement(item, 'title').text = content_title
            ET.SubElement(item, 'identifierref').text = resource_id
            ET.SubElement(item, 'position').text = position
            ET.SubElement(item, 'new_tab').text = 'false'
            ET.SubElement(item, 'indent').text = '0'

            # Add item to imsmanifest.xml organizations
            quiz_item_org = ET.SubElement(module_item_org, 'item')
            quiz_item_org.set('identifier', item_id)
            quiz_item_org.set('identifierref', resource_id)
            ET.SubElement(quiz_item_org, 'title').text = content_title

            # Create quiz files and directories
            quiz_dir = os.path.join(project_dir, resource_id)
            os.makedirs(quiz_dir, exist_ok=True)
            non_cc_dir = os.path.join(project_dir, 'non_cc_assessments')
            os.makedirs(non_cc_dir, exist_ok=True)

            qti_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/qti/qtiv1p2/qtiasi_v1p2.xsd">
  <assessment ident="{resource_id}" title="{content_title}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>qmd_assessmenttype</fieldlabel>
        <fieldentry>Assignment</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section"/>
  </assessment>
</questestinterop>'''
            
            qti_filename = 'assessment_qti.xml'
            qti_filepath = os.path.join(quiz_dir, qti_filename)
            with open(qti_filepath, 'w', encoding='utf-8') as f:
                f.write(qti_content)
            print(f"Created QTI file: {qti_filepath}")

            non_cc_filename = f'{resource_id}.xml.qti'
            non_cc_filepath = os.path.join(non_cc_dir, non_cc_filename)
            with open(non_cc_filepath, 'w', encoding='utf-8') as f:
                f.write(qti_content)
            print(f"Created non-CC QTI file: {non_cc_filepath}")

            meta_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{resource_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 http://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{content_title}</title>
  <quiz_type>assignment</quiz_type>
  <shuffle_answers>true</shuffle_answers>
  <scoring_policy>keep_latest</scoring_policy>
  <hide_results></hide_results>
  <show_correct_answers>true</show_correct_answers>
  <allowed_attempts>-1</allowed_attempts>
  <published>true</published>
  <only_visible_to_overrides>false</only_visible_to_overrides>
</quiz>'''
            meta_filename = 'assessment_meta.xml'
            meta_filepath = os.path.join(quiz_dir, meta_filename)
            with open(meta_filepath, 'w', encoding='utf-8') as f:
                f.write(meta_content)
            print(f"Created quiz meta file: {meta_filepath}")

            # Add resources to imsmanifest.xml
            # Main quiz resource
            resource_elem = ET.SubElement(resources, 'resource')
            resource_elem.set('identifier', resource_id)
            resource_elem.set('type', 'imsqti_xmlv1p2/imscc_xmlv1p1/assessment')
            resource_elem.set('href', f'{resource_id}/{qti_filename}')
            file_elem = ET.SubElement(resource_elem, 'file')
            file_elem.set('href', f'{resource_id}/{qti_filename}')
            dep_elem = ET.SubElement(resource_elem, 'dependency')
            dep_elem.set('identifierref', dependency_id)

            # Dependency resource
            dep_resource_elem = ET.SubElement(resources, 'resource')
            dep_resource_elem.set('identifier', dependency_id)
            dep_resource_elem.set('type', 'associatedcontent/imscc_xmlv1p1/learning-application-resource')
            dep_resource_elem.set('href', f'{resource_id}/{meta_filename}')
            file_elem1 = ET.SubElement(dep_resource_elem, 'file')
            file_elem1.set('href', f'{resource_id}/{meta_filename}')
            file_elem2 = ET.SubElement(dep_resource_elem, 'file')
            file_elem2.set('href', f'non_cc_assessments/{non_cc_filename}')

        elif content_type == 'discussion':
            dependency_id = generate_uuid()

            # Add item to module_meta.xml
            item = ET.SubElement(items, 'item')
            item.set('identifier', item_id)
            ET.SubElement(item, 'content_type').text = 'DiscussionTopic'
            ET.SubElement(item, 'workflow_state').text = 'active'
            ET.SubElement(item, 'title').text = content_title
            ET.SubElement(item, 'identifierref').text = resource_id
            ET.SubElement(item, 'position').text = position
            ET.SubElement(item, 'new_tab').text = 'false'
            ET.SubElement(item, 'indent').text = '0'

            # Add item to imsmanifest.xml organizations
            discussion_item_org = ET.SubElement(module_item_org, 'item')
            discussion_item_org.set('identifier', item_id)
            discussion_item_org.set('identifierref', resource_id)
            ET.SubElement(discussion_item_org, 'title').text = content_title

            # Create discussion files
            # Main discussion topic file
            topic_filename = f'{resource_id}.xml'
            topic_filepath = os.path.join(project_dir, topic_filename)
            topic_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imsdt_v1p1.xsd">
  <title>{content_title}</title>
  <text texttype="text/html">This is a sample discussion topic. Please add your prompt here.</text>
</topic>'''
            with open(topic_filepath, 'w', encoding='utf-8') as f:
                f.write(topic_content)
            print(f"Created discussion topic file: {topic_filepath}")

            # Canvas metadata file
            meta_filename = f'{dependency_id}.xml'
            meta_filepath = os.path.join(project_dir, meta_filename)
            meta_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<topicMeta xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 http://canvas.instructure.com/xsd/cccv1p0.xsd" identifier="{resource_id}">
  <title>{content_title}</title>
  <discussion_type>side_comment</discussion_type>
  <workflow_state>active</workflow_state>
  <locked>false</locked>
</topicMeta>'''
            with open(meta_filepath, 'w', encoding='utf-8') as f:
                f.write(meta_content)
            print(f"Created discussion meta file: {meta_filepath}")

            # Add resources to imsmanifest.xml
            # Main discussion resource
            resource_elem = ET.SubElement(resources, 'resource')
            resource_elem.set('identifier', resource_id)
            resource_elem.set('type', 'imsdt_xmlv1p1')
            file_elem = ET.SubElement(resource_elem, 'file')
            file_elem.set('href', topic_filename)
            dep_elem = ET.SubElement(resource_elem, 'dependency')
            dep_elem.set('identifierref', dependency_id)

            # Dependency resource for metadata
            dep_resource_elem = ET.SubElement(resources, 'resource')
            dep_resource_elem.set('identifier', dependency_id)
            dep_resource_elem.set('type', 'associatedcontent/imscc_xmlv1p1/learning-application-resource')
            dep_resource_elem.set('href', meta_filename)
            file_elem2 = ET.SubElement(dep_resource_elem, 'file')
            file_elem2.set('href', meta_filename)

    # Write the updated XMLs
    tree.write(module_meta_file, encoding='utf-8', xml_declaration=True)
    print(f"Updated {module_meta_file} with module: {module_title}")
    manifest_tree.write(manifest_file, encoding='utf-8', xml_declaration=True)
    print(f"Updated {manifest_file} with module: {module_title}")
    return True

def create_zip_archive(source_dir, output_filename):
    """formats, then Zips the contents of the source_dir into output_filename."""

    # Pretty-print XML files before zipping
    xml_files_to_format = [
        os.path.join(source_dir, 'module_meta.xml'),
        os.path.join(source_dir, 'imsmanifest.xml')
    ]
    for xml_file in xml_files_to_format:
        if os.path.exists(xml_file):
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(xml_file, parser)
            tree.write(xml_file, pretty_print=True, encoding='utf-8', xml_declaration=True)
            print(f"Formatted {os.path.basename(xml_file)}")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Don't add the zip file itself to the archive
                if os.path.abspath(file_path) == os.path.abspath(output_filename):
                    continue
                archive_name = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, archive_name)
    print(f"Successfully created zip archive: {output_filename}")

def main():
    """
    Main function that runs the functions sequentially:
    1. Create project structure
    2. Add a module with a WikiPage
    3. Add a module with a Quiz
    4. Add a module with an Assignment
    5. Add a module with a File
    6. Add a module with a Discussion
    7. Zip the project
    """
    print("=== Common Cartridge Generator ===")
    
    project_dir_name = "current_project"
    if os.path.exists(project_dir_name):
        print(f"Deleting existing project directory: {project_dir_name}")
        shutil.rmtree(project_dir_name)
    
    print("\n1. Creating project structure...")
    project_dir, module_meta_file, manifest_file = create_project_structure()
    
    print("\n2. Adding module with a WikiPage...")
    success = add_module_with_content(
        module_meta_file, manifest_file,
        module_title="Module with Page",
        content_items=[{'type': 'page', 'title': 'My First Page'}]
    )
    
    if success:
        print("\n3. Adding another module with a Quiz...")
        success = add_module_with_content(
            module_meta_file, manifest_file,
            module_title="Module with Quiz",
            content_items=[{'type': 'quiz', 'title': 'My First Quiz'}]
        )
    
    if success:
        print("\n4. Adding a module with an Assignment...")
        success = add_module_with_content(
            module_meta_file, manifest_file,
            module_title="Module with Assignment",
            content_items=[{'type': 'assignment', 'title': 'My First Assignment'}]
        )

    if success:
        print("\n5. Adding a module with a File...")
        success = add_module_with_content(
            module_meta_file, manifest_file,
            module_title="Module with File",
            content_items=[{'type': 'file', 'title': 'hello.txt'}]
        )

    if success:
        print("\n6. Adding a module with a Discussion...")
        success = add_module_with_content(
            module_meta_file, manifest_file,
            module_title="Module with Discussion",
            content_items=[{'type': 'discussion', 'title': 'My First Discussion'}]
        )

    if success:
        print("\n7. Zipping project contents...")
        zip_filename = os.path.join(project_dir, "working_cartridge.zip")
        create_zip_archive(project_dir, zip_filename)
    else:
        print("Error occurred while adding module")

if __name__ == "__main__":
    main()