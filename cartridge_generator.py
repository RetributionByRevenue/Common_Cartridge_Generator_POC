#!/usr/bin/env python3
# Command to run this file: /home/q/Desktop/test_cartridge/.venv/bin/python cartridge_generator.py generated_cartridge
"""
Canvas Common Cartridge Generator
Generates a complete Common Cartridge with all content types from scratch

USAGE EXAMPLES:
    # Basic generation with default course
    python cartridge_generator.py my_new_cartridge
    
    # Generate with custom course title and code
    python cartridge_generator.py generated_course --title "Introduction to Python" --code "CS101"
    
    # Generate and compare with existing cartridge (commented out in main)
    python cartridge_generator.py test_cartridge --title "Test Course" --code "TEST" --compare produced_cartridge
    
    # Real-world example
    python cartridge_generator.py biology_101 --title "Biology Fundamentals" --code "BIO101"

WHAT IT CREATES:
    - Complete cartridge directory structure with all Canvas XML files
    - Sample module with wiki page
    - Sample assignment with HTML content and settings
    - Sample quiz with QTI assessment and multiple choice question
    - Sample announcement with proper topic/meta structure
    - Sample web resource file
    - Full imsmanifest.xml with proper resource dependencies
"""

import os
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import argparse
import filecmp
import shutil
from cartridge_replicator import scan_cartridge

class CartridgeGenerator:
    def __init__(self, course_title="Generated Course", course_code="GEN101"):
        self.course_title = course_title
        self.course_code = course_code
        
        # Generate main identifiers
        self.course_id = f"g{uuid.uuid4().hex}"
        self.manifest_id = f"g{uuid.uuid4().hex}"
        self.root_account_uuid = f"ff2e5780-fa5b-012d-f7b3-{uuid.uuid4().hex[:12]}"
        
        # Storage for generated content
        self.modules = []
        self.assignments = []
        self.quizzes = []
        self.announcements = []
        self.wiki_pages = []
        self.files = []
        self.resources = []
        self.organization_items = []
        
        # Assignment group ID (required for assignments/quizzes)
        self.assignment_group_id = f"g{uuid.uuid4().hex}"
        
        # Store current cartridge state and DataFrame
        self.output_dir = None
        self.current_df = None
    
    @property
    def df(self):
        """Get the current DataFrame state"""
        return self.current_df
    
    def _update_cartridge_state(self):
        """Write cartridge files and update DataFrame state"""
        if self.output_dir:
            self.write_cartridge_files(self.output_dir)
            self.current_df = scan_cartridge(self.output_dir)
            print(f"Cartridge state updated. Found {len(self.current_df)} components.")
        
    def create_base_cartridge(self, output_dir):
        """Create the base cartridge structure with core files"""
        output_path = Path(output_dir)
        
        # Remove existing contents if directory is not empty
        if output_path.exists() and any(output_path.iterdir()):
            print(f"Removing existing contents from {output_dir}")
            shutil.rmtree(output_path)
        
        output_path.mkdir(exist_ok=True)
        
        # Create directory structure
        directories = [
            'course_settings', 'wiki_content', 'non_cc_assessments', 
            'web_resources', 'assignments', 'discussions', 'quizzes', 
            'files', 'media', 'external_tools'
        ]
        
        for directory in directories:
            (output_path / directory).mkdir(exist_ok=True)
        
        # Create core course settings files
        self._create_canvas_export_txt(output_path / "course_settings" / "canvas_export.txt")
        self._create_course_settings_xml(output_path / "course_settings" / "course_settings.xml")
        self._create_context_xml(output_path / "course_settings" / "context.xml")
        self._create_assignment_groups_xml(output_path / "course_settings" / "assignment_groups.xml")
        self._create_files_meta_xml(output_path / "course_settings" / "files_meta.xml")
        self._create_late_policy_xml(output_path / "course_settings" / "late_policy.xml")
        self._create_media_tracks_xml(output_path / "course_settings" / "media_tracks.xml")
        
        # Module meta will be created later when modules are added
        self._create_empty_module_meta_xml(output_path / "course_settings" / "module_meta.xml")
        
        # Store output directory and update state
        self.output_dir = str(output_path)
        self._update_cartridge_state()
        
        return str(output_path)
    
    def _create_canvas_export_txt(self, filepath):
        """Create canvas_export.txt file"""
        content = "Q: What did the panda say when he was forced out of his natural habitat?\nA: This is un-BEAR-able\n"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_course_settings_xml(self, filepath):
        """Create course_settings.xml file"""
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<course identifier="{self.course_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{self.course_title}</title>
  <course_code>{self.course_code}</course_code>
  <start_at/>
  <conclude_at/>
  <is_public>false</is_public>
  <allow_student_wiki_edits>false</allow_student_wiki_edits>
  <lock_all_announcements>false</lock_all_announcements>
  <allow_student_organized_groups>true</allow_student_organized_groups>
  <default_view>modules</default_view>
  <allow_final_grade_override>false</allow_final_grade_override>
  <usage_rights_required>false</usage_rights_required>
  <restrict_student_future_view>false</restrict_student_future_view>
  <restrict_student_past_view>false</restrict_student_past_view>
  <homeroom_course>false</homeroom_course>
  <horizon_course>false</horizon_course>
  <conditional_release>true</conditional_release>
  <content_library>false</content_library>
  <grading_standard_enabled>false</grading_standard_enabled>
  <storage_quota>500000000</storage_quota>
  <overridden_course_visibility/>
  <root_account_uuid>{self.root_account_uuid}</root_account_uuid>
  <default_post_policy>
    <post_manually>false</post_manually>
  </default_post_policy>
  <allow_final_grade_override>false</allow_final_grade_override>
  <enable_course_paces>false</enable_course_paces>
</course>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_context_xml(self, filepath):
        """Create context.xml file"""
        course_id_num = abs(hash(self.course_id)) % 100000000
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<context_info xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <course_id>{course_id_num}</course_id>
  <course_name>{self.course_title}</course_name>
  <root_account_id>70000000000010</root_account_id>
  <root_account_name>Free for Teacher</root_account_name>
  <root_account_uuid>{self.root_account_uuid}</root_account_uuid>
  <canvas_domain>canvas.instructure.com</canvas_domain>
</context_info>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_assignment_groups_xml(self, filepath):
        """Create assignment_groups.xml file"""
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <assignmentGroup identifier="{self.assignment_group_id}">
    <title>Assignments</title>
    <position>1</position>
    <group_weight>0.0</group_weight>
  </assignmentGroup>
</assignmentGroups>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_files_meta_xml(self, filepath):
        """Create files_meta.xml file"""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<fileMeta xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
</fileMeta>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_late_policy_xml(self, filepath):
        """Create late_policy.xml file"""
        late_policy_id = f"g{uuid.uuid4().hex}"
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<late_policy identifier="{late_policy_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <missing_submission_deduction_enabled>false</missing_submission_deduction_enabled>
  <missing_submission_deduction>100.0</missing_submission_deduction>
  <late_submission_deduction_enabled>false</late_submission_deduction_enabled>
  <late_submission_deduction>0.0</late_submission_deduction>
  <late_submission_interval>day</late_submission_interval>
  <late_submission_minimum_percent_enabled>false</late_submission_minimum_percent_enabled>
  <late_submission_minimum_percent>0.0</late_submission_minimum_percent>
</late_policy>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_media_tracks_xml(self, filepath):
        """Create media_tracks.xml file"""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<media_tracks xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
</media_tracks>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_empty_module_meta_xml(self, filepath):
        """Create empty module_meta.xml file"""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
</modules>
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def add_module(self, module_title, position=None, published=True):
        """Add a module to the cartridge"""
        module_id = f"g{uuid.uuid4().hex}"
        
        module = {
            'identifier': module_id,
            'title': module_title,
            'position': position or len(self.modules) + 1,
            'workflow_state': 'published' if published else 'unpublished',
            'items': []
        }
        
        self.modules.append(module)
        
        # Add to organization structure
        self.organization_items.append({
            'identifier': module_id,
            'title': module_title,
            'type': 'module',
            'items': []
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return module_id
    
    def add_wiki_page_to_module(self, module_id, page_title, page_content="", published=True):
        """Add a wiki page to a specific module using actual module identifier from DataFrame"""
        page_id = f"g{uuid.uuid4().hex}"
        resource_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"
        
        # Find the module in both internal list and verify it exists in current state
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            # If not found in internal list, check if it exists in current DataFrame
            if self.current_df is not None:
                module_exists = not self.current_df[(self.current_df['type'] == 'module') & 
                                                   (self.current_df['identifier'] == module_id)].empty
                if module_exists:
                    # Get module title from DataFrame to create new internal module entry
                    module_title = self.current_df[(self.current_df['type'] == 'module') & 
                                                  (self.current_df['identifier'] == module_id)]['title'].iloc[0]
                    # Create internal module entry
                    module = {
                        'identifier': module_id,
                        'title': module_title,
                        'position': len(self.modules) + 1,
                        'workflow_state': 'unpublished',
                        'items': []
                    }
                    self.modules.append(module)
                    
                    # Add to organization structure
                    self.organization_items.append({
                        'identifier': module_id,
                        'title': module_title,
                        'type': 'module',
                        'items': []
                    })
                else:
                    raise ValueError(f"Module with identifier {module_id} not found in current cartridge state")
            else:
                raise ValueError(f"Module with identifier {module_id} not found")
        
        # Add item to module
        item = {
            'identifier': item_id,
            'title': page_title,
            'content_type': 'WikiPage',
            'workflow_state': 'published' if published else 'unpublished',
            'identifierref': resource_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)
        
        # Store wiki page info
        wiki_page = {
            'identifier': page_id,
            'resource_id': resource_id,
            'title': page_title,
            'content': page_content,
            'workflow_state': 'published' if published else 'unpublished',
            'filename': f"wiki_content/{page_title.lower().replace(' ', '-').replace('_', '-')}.html"
        }
        self.wiki_pages.append(wiki_page)
        
        # Add to resources
        self.resources.append({
            'identifier': resource_id,
            'type': 'webcontent',
            'href': wiki_page['filename']
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': page_title,
                'identifierref': resource_id
            })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return page_id
    
    def add_assignment_to_module(self, module_id, assignment_title, assignment_content="", points=100, published=True):
        """Add an assignment to a specific module using actual module identifier from DataFrame"""
        assignment_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"
        
        # Find the module in both internal list and verify it exists in current state
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            # If not found in internal list, check if it exists in current DataFrame
            if self.current_df is not None:
                module_exists = not self.current_df[(self.current_df['type'] == 'module') & 
                                                   (self.current_df['identifier'] == module_id)].empty
                if module_exists:
                    # Get module title from DataFrame to create new internal module entry
                    module_title = self.current_df[(self.current_df['type'] == 'module') & 
                                                  (self.current_df['identifier'] == module_id)]['title'].iloc[0]
                    # Create internal module entry
                    module = {
                        'identifier': module_id,
                        'title': module_title,
                        'position': len(self.modules) + 1,
                        'workflow_state': 'unpublished',
                        'items': []
                    }
                    self.modules.append(module)
                    
                    # Add to organization structure
                    self.organization_items.append({
                        'identifier': module_id,
                        'title': module_title,
                        'type': 'module',
                        'items': []
                    })
                else:
                    raise ValueError(f"Module with identifier {module_id} not found in current cartridge state")
            else:
                raise ValueError(f"Module with identifier {module_id} not found")
        
        # Add item to module
        item = {
            'identifier': item_id,
            'title': assignment_title,
            'content_type': 'Assignment',
            'workflow_state': 'published' if published else 'unpublished',
            'identifierref': assignment_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)
        
        # Store assignment info
        assignment = {
            'identifier': assignment_id,
            'title': assignment_title,
            'content': assignment_content,
            'points_possible': points,
            'workflow_state': 'published' if published else 'unpublished',
            'assignment_group_id': self.assignment_group_id,
            'position': len(self.assignments) + 1
        }
        self.assignments.append(assignment)
        
        # Add to resources
        self.resources.append({
            'identifier': assignment_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"{assignment_id}/my-first-assignment.html"
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': assignment_title,
                'identifierref': assignment_id
            })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return assignment_id
    
    def add_quiz_to_module(self, module_id, quiz_title, quiz_description="", points=1, published=True):
        """Add a quiz to a specific module using actual module identifier from DataFrame"""
        quiz_id = f"g{uuid.uuid4().hex}"
        assignment_id = f"g{uuid.uuid4().hex}"
        resource_id = f"g{uuid.uuid4().hex}"
        question_id = f"g{uuid.uuid4().hex}"
        assessment_question_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"
        
        # Find the module in both internal list and verify it exists in current state
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            # If not found in internal list, check if it exists in current DataFrame
            if self.current_df is not None:
                module_exists = not self.current_df[(self.current_df['type'] == 'module') & 
                                                   (self.current_df['identifier'] == module_id)].empty
                if module_exists:
                    # Get module title from DataFrame to create new internal module entry
                    module_title = self.current_df[(self.current_df['type'] == 'module') & 
                                                  (self.current_df['identifier'] == module_id)]['title'].iloc[0]
                    # Create internal module entry
                    module = {
                        'identifier': module_id,
                        'title': module_title,
                        'position': len(self.modules) + 1,
                        'workflow_state': 'unpublished',
                        'items': []
                    }
                    self.modules.append(module)
                    
                    # Add to organization structure
                    self.organization_items.append({
                        'identifier': module_id,
                        'title': module_title,
                        'type': 'module',
                        'items': []
                    })
                else:
                    raise ValueError(f"Module with identifier {module_id} not found in current cartridge state")
            else:
                raise ValueError(f"Module with identifier {module_id} not found")
        
        # Add item to module
        item = {
            'identifier': item_id,
            'title': quiz_title,
            'content_type': 'Quizzes::Quiz',
            'workflow_state': 'published' if published else 'unpublished',
            'identifierref': quiz_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)
        
        # Store quiz info
        quiz = {
            'identifier': quiz_id,
            'title': quiz_title,
            'description': quiz_description,
            'points_possible': points,
            'workflow_state': 'published' if published else 'unpublished',
            'assignment_id': assignment_id,
            'assignment_group_id': self.assignment_group_id,
            'position': len(self.quizzes) + 1,
            'question_id': question_id,
            'assessment_question_id': assessment_question_id
        }
        self.quizzes.append(quiz)
        
        # Add to resources
        self.resources.append({
            'identifier': quiz_id,
            'type': 'imsqti_xmlv1p2/imscc_xmlv1p1/assessment',
            'href': f"{quiz_id}/assessment_qti.xml",
            'dependency': resource_id
        })
        
        self.resources.append({
            'identifier': resource_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"{quiz_id}/assessment_meta.xml"
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': quiz_title,
                'identifierref': quiz_id
            })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return quiz_id
    
    def add_discussion_to_module(self, module_id, title, body, published=True):
        """Add a discussion topic to a specific module using actual module identifier from DataFrame"""
        topic_id = f"g{uuid.uuid4().hex}"
        meta_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"
        
        # Find the module in both internal list and verify it exists in current state
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            # If not found in internal list, check if it exists in current DataFrame
            if self.current_df is not None:
                module_exists = not self.current_df[(self.current_df['type'] == 'module') & 
                                                   (self.current_df['identifier'] == module_id)].empty
                if module_exists:
                    # Get module title from DataFrame to create new internal module entry
                    module_title = self.current_df[(self.current_df['type'] == 'module') & 
                                                  (self.current_df['identifier'] == module_id)]['title'].iloc[0]
                    # Create internal module entry
                    module = {
                        'identifier': module_id,
                        'title': module_title,
                        'position': len(self.modules) + 1,
                        'workflow_state': 'unpublished',
                        'items': []
                    }
                    self.modules.append(module)
                    
                    # Add to organization structure
                    self.organization_items.append({
                        'identifier': module_id,
                        'title': module_title,
                        'type': 'module',
                        'items': []
                    })
                else:
                    raise ValueError(f"Module with identifier {module_id} not found in current cartridge state")
            else:
                raise ValueError(f"Module with identifier {module_id} not found")
        
        # Add item to module
        item = {
            'identifier': item_id,
            'title': title,
            'content_type': 'DiscussionTopic',
            'workflow_state': 'published' if published else 'unpublished',
            'identifierref': topic_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)
        
        # Store discussion topic info
        discussion_topic = {
            'topic_id': topic_id,
            'meta_id': meta_id,
            'title': title,
            'body': body,
            'workflow_state': 'active' if published else 'unpublished',
        }
        self.announcements.append(discussion_topic)
        
        # Add to resources
        self.resources.append({
            'identifier': topic_id,
            'type': 'imsdt_xmlv1p1',
            'href': f"discussions/{topic_id}.xml",
            'dependency': meta_id
        })
        
        self.resources.append({
            'identifier': meta_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"discussions/{meta_id}.xml"
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': title,
                'identifierref': topic_id
            })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return topic_id
    
    def add_assignment(self, assignment_title, assignment_content="", points=100, published=True):
        """Add an assignment to the cartridge"""
        assignment_id = f"g{uuid.uuid4().hex}"
        
        assignment = {
            'identifier': assignment_id,
            'title': assignment_title,
            'content': assignment_content,
            'points_possible': points,
            'workflow_state': 'published' if published else 'unpublished',
            'assignment_group_id': self.assignment_group_id,
            'position': len(self.assignments) + 1
        }
        
        self.assignments.append(assignment)
        
        # Add to resources
        self.resources.append({
            'identifier': assignment_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"{assignment_id}/my-first-assignment.html"
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return assignment_id
    
    def add_quiz(self, quiz_title, quiz_description="", points=1, published=True):
        """Add a quiz to the cartridge"""
        quiz_id = f"g{uuid.uuid4().hex}"
        assignment_id = f"g{uuid.uuid4().hex}"
        resource_id = f"g{uuid.uuid4().hex}"
        question_id = f"g{uuid.uuid4().hex}"
        assessment_question_id = f"g{uuid.uuid4().hex}"
        
        quiz = {
            'identifier': quiz_id,
            'title': quiz_title,
            'description': quiz_description,
            'points_possible': points,
            'workflow_state': 'published' if published else 'unpublished',
            'assignment_id': assignment_id,
            'assignment_group_id': self.assignment_group_id,
            'position': len(self.quizzes) + 1,
            'question_id': question_id,
            'assessment_question_id': assessment_question_id
        }
        
        self.quizzes.append(quiz)
        
        # Add to resources
        self.resources.append({
            'identifier': quiz_id,
            'type': 'imsqti_xmlv1p2/imscc_xmlv1p1/assessment',
            'href': f"{quiz_id}/assessment_qti.xml",
            'dependency': resource_id
        })
        
        self.resources.append({
            'identifier': resource_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"{quiz_id}/assessment_meta.xml"
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return quiz_id
    
    def add_discussion_topic(self, module_id, title, body, published=True):
        """Add a discussion topic to a specific module"""
        topic_id = f"g{uuid.uuid4().hex}"
        meta_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"

        # Find the module
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            raise ValueError(f"Module with identifier {module_id} not found")

        # Add item to module
        item = {
            'identifier': item_id,
            'title': title,
            'content_type': 'DiscussionTopic',
            'workflow_state': 'published' if published else 'unpublished',
            'identifierref': topic_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)

        # Store discussion topic info
        discussion_topic = {
            'topic_id': topic_id,
            'meta_id': meta_id,
            'title': title,
            'body': body,
            'workflow_state': 'active' if published else 'unpublished',
        }
        self.announcements.append(discussion_topic)

        # Add to resources
        self.resources.append({
            'identifier': topic_id,
            'type': 'imsdt_xmlv1p1',
            'href': f"discussions/{topic_id}.xml",
            'dependency': meta_id
        })

        self.resources.append({
            'identifier': meta_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"discussions/{meta_id}.xml"
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': title,
                'identifierref': topic_id
            })

        # Update cartridge state
        self._update_cartridge_state()

        return topic_id
    
    def add_standalone_wiki_page(self, page_title, page_content="", published=True):
        """Add a standalone wiki page (not attached to any module)"""
        page_id = f"g{uuid.uuid4().hex}"
        resource_id = f"g{uuid.uuid4().hex}"
        
        # Store wiki page info
        wiki_page = {
            'identifier': page_id,
            'resource_id': resource_id,
            'title': page_title,
            'content': page_content,
            'workflow_state': 'published' if published else 'unpublished',
            'filename': f"wiki_content/{page_title.lower().replace(' ', '-').replace('_', '-')}.html"
        }
        self.wiki_pages.append(wiki_page)
        
        # Add to resources (but not to organization structure)
        self.resources.append({
            'identifier': resource_id,
            'type': 'webcontent',
            'href': wiki_page['filename']
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return page_id
    
    def add_standalone_discussion(self, title, body, published=True):
        """Add a standalone discussion (not attached to any module)"""
        topic_id = f"g{uuid.uuid4().hex}"
        meta_id = f"g{uuid.uuid4().hex}"
        
        # Store discussion topic info
        discussion_topic = {
            'topic_id': topic_id,
            'meta_id': meta_id,
            'title': title,
            'body': body,
            'workflow_state': 'unpublished' if not published else 'active',
        }
        self.announcements.append(discussion_topic)
        
        # Add to resources (files go in root directory, not discussions/ subdirectory)
        self.resources.append({
            'identifier': topic_id,
            'type': 'imsdt_xmlv1p1',
            'href': f"{topic_id}.xml",
            'dependency': meta_id
        })
        
        self.resources.append({
            'identifier': meta_id,
            'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
            'href': f"{meta_id}.xml"
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return topic_id
    
    def add_file_to_module(self, module_id, filename, file_content):
        """Add a file to a specific module using actual module identifier from DataFrame"""
        file_id = f"g{uuid.uuid4().hex}"
        item_id = f"g{uuid.uuid4().hex}"
        
        # Find the module in both internal list and verify it exists in current state
        module = next((m for m in self.modules if m['identifier'] == module_id), None)
        if not module:
            # If not found in internal list, check if it exists in current DataFrame
            if self.current_df is not None:
                module_exists = not self.current_df[(self.current_df['type'] == 'module') & 
                                                   (self.current_df['identifier'] == module_id)].empty
                if module_exists:
                    # Get module title from DataFrame to create new internal module entry
                    module_title = self.current_df[(self.current_df['type'] == 'module') & 
                                                  (self.current_df['identifier'] == module_id)]['title'].iloc[0]
                    # Create internal module entry
                    module = {
                        'identifier': module_id,
                        'title': module_title,
                        'position': len(self.modules) + 1,
                        'workflow_state': 'unpublished',
                        'items': []
                    }
                    self.modules.append(module)
                    
                    # Add to organization structure
                    self.organization_items.append({
                        'identifier': module_id,
                        'title': module_title,
                        'type': 'module',
                        'items': []
                    })
                else:
                    raise ValueError(f"Module with identifier {module_id} not found in current cartridge state")
            else:
                raise ValueError(f"Module with identifier {module_id} not found")
        
        # Add item to module
        item = {
            'identifier': item_id,
            'title': filename,
            'content_type': 'Attachment',
            'workflow_state': 'published',
            'identifierref': file_id,
            'position': len(module['items']) + 1
        }
        module['items'].append(item)
        
        # Store file info
        file_info = {
            'identifier': file_id,
            'filename': filename,
            'content': file_content,
            'path': f"web_resources/{filename}"
        }
        self.files.append(file_info)
        
        # Add to resources
        self.resources.append({
            'identifier': file_id,
            'type': 'webcontent',
            'href': f"web_resources/{filename}"
        })
        
        # Add to organization structure
        org_module = next((m for m in self.organization_items if m['identifier'] == module_id), None)
        if org_module:
            org_module['items'].append({
                'identifier': item_id,
                'title': filename,
                'identifierref': file_id
            })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return file_id
    
    def add_file_standalone(self, filename, file_content):
        """Add a standalone file (not attached to any module)"""
        file_id = f"g{uuid.uuid4().hex}"
        
        # Store file info
        file_info = {
            'identifier': file_id,
            'filename': filename,
            'content': file_content,
            'path': f"web_resources/{filename}"
        }
        self.files.append(file_info)
        
        # Add to resources (files go in web_resources/ directory)
        self.resources.append({
            'identifier': file_id,
            'type': 'webcontent',
            'href': f"web_resources/{filename}"
        })
        
        # Update cartridge state
        self._update_cartridge_state()
        
        return file_id
    
    def write_cartridge_files(self, output_dir):
        """Write all content files to the cartridge directory"""
        output_path = Path(output_dir)
        
        # Update module_meta.xml
        self._update_module_meta_xml(output_path / "course_settings" / "module_meta.xml")
        
        # Create wiki pages
        for page in self.wiki_pages:
            self._create_wiki_page_html(output_path / page['filename'], page)
        
        # Create assignments
        for assignment in self.assignments:
            self._create_assignment_files(output_path, assignment)
        
        # Create quizzes
        for quiz in self.quizzes:
            self._create_quiz_files(output_path, quiz)
        
        # Create announcements
        for announcement in self.announcements:
            self._create_announcement_files(output_path, announcement)
        
        # Create web resources
        for file_info in self.files:
            self._create_web_resource_file(output_path, file_info)
        
        # Create manifest
        self._create_imsmanifest_xml(output_path / "imsmanifest.xml")
        
        return str(output_path)
    
    def _update_module_meta_xml(self, filepath):
        """Update module_meta.xml with all modules"""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<modules xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
"""
        
        for module in self.modules:
            content += f"""  <module identifier="{module['identifier']}">
    <title>{module['title']}</title>
    <workflow_state>{module['workflow_state']}</workflow_state>
    <position>{module['position']}</position>
    <require_sequential_progress>false</require_sequential_progress>
    <locked>false</locked>
    <items>
"""
            
            for item in module['items']:
                content += f"""      <item identifier="{item['identifier']}">
        <content_type>{item['content_type']}</content_type>
        <workflow_state>{item['workflow_state']}</workflow_state>
        <title>{item['title']}</title>
        <identifierref>{item['identifierref']}</identifierref>
        <position>{item['position']}</position>
        <new_tab/>
        <indent>0</indent>
        <link_settings_json>null</link_settings_json>
      </item>
"""
            
            content += """    </items>
  </module>
"""
        
        content += "</modules>\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_wiki_page_html(self, filepath, page):
        """Create wiki page HTML file"""
        content = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{page['title']}</title>
<meta name="identifier" content="{page['resource_id']}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="{page['workflow_state']}"/>
</head>
<body>
{page['content']}
</body>
</html>"""
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_assignment_files(self, output_path, assignment):
        """Create assignment files"""
        assignment_dir = output_path / assignment['identifier']
        assignment_dir.mkdir(parents=True, exist_ok=True)
        
        # Create assignment_settings.xml
        settings_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{assignment['identifier']}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{assignment['title']}</title>
  <due_at/>
  <lock_at/>
  <unlock_at/>
  <module_locked>false</module_locked>
  <assignment_group_identifierref>{assignment['assignment_group_id']}</assignment_group_identifierref>
  <workflow_state>{assignment['workflow_state']}</workflow_state>
  <assignment_overrides>
  </assignment_overrides>
  <allowed_extensions></allowed_extensions>
  <has_group_category>false</has_group_category>
  <points_possible>{assignment['points_possible']}.0</points_possible>
  <grading_type>points</grading_type>
  <all_day>false</all_day>
  <submission_types>on_paper</submission_types>
  <position>{assignment['position']}</position>
  <turnitin_enabled>false</turnitin_enabled>
  <vericite_enabled>false</vericite_enabled>
  <peer_review_count>0</peer_review_count>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <grade_group_students_individually>false</grade_group_students_individually>
  <freeze_on_copy>false</freeze_on_copy>
  <omit_from_final_grade>false</omit_from_final_grade>
  <hide_in_gradebook>false</hide_in_gradebook>
  <intra_group_peer_reviews>false</intra_group_peer_reviews>
  <only_visible_to_overrides>false</only_visible_to_overrides>
  <post_to_sis>false</post_to_sis>
  <moderated_grading>false</moderated_grading>
  <grader_count>0</grader_count>
  <grader_comments_visible_to_graders>true</grader_comments_visible_to_graders>
  <anonymous_grading>false</anonymous_grading>
  <graders_anonymous_to_graders>false</graders_anonymous_to_graders>
  <grader_names_visible_to_final_grader>true</grader_names_visible_to_final_grader>
  <anonymous_instructor_annotations>false</anonymous_instructor_annotations>
  <post_policy>
    <post_manually>false</post_manually>
  </post_policy>
</assignment>
"""
        
        with open(assignment_dir / "assignment_settings.xml", 'w', encoding='utf-8') as f:
            f.write(settings_content)
        
        # Create assignment content HTML
        html_content = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Assignment: {assignment['title']}</title>
</head>
<body>
<p>{assignment['content']}</p>
</body>
</html>"""
        
        with open(assignment_dir / "my-first-assignment.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _create_quiz_files(self, output_path, quiz):
        """Create quiz files"""
        quiz_dir = output_path / quiz['identifier']
        quiz_dir.mkdir(parents=True, exist_ok=True)
        
        # Create assessment_meta.xml
        meta_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{quiz['identifier']}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{quiz['title']}</title>
  <description>&lt;p&gt;{quiz['description']}&lt;/p&gt;</description>
  <shuffle_answers>false</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <hide_results>always</hide_results>
  <quiz_type>assignment</quiz_type>
  <points_possible>{quiz['points_possible']}.0</points_possible>
  <require_lockdown_browser>false</require_lockdown_browser>
  <require_lockdown_browser_for_results>false</require_lockdown_browser_for_results>
  <require_lockdown_browser_monitor>false</require_lockdown_browser_monitor>
  <lockdown_browser_monitor_data/>
  <show_correct_answers>false</show_correct_answers>
  <anonymous_submissions>false</anonymous_submissions>
  <could_be_locked>false</could_be_locked>
  <disable_timer_autosubmission>false</disable_timer_autosubmission>
  <allowed_attempts>1</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>true</available>
  <one_time_results>false</one_time_results>
  <show_correct_answers_last_attempt>false</show_correct_answers_last_attempt>
  <only_visible_to_overrides>false</only_visible_to_overrides>
  <module_locked>false</module_locked>
  <assignment identifier="{quiz['assignment_id']}">
    <title>{quiz['title']}</title>
    <due_at/>
    <lock_at/>
    <unlock_at/>
    <module_locked>false</module_locked>
    <assignment_group_identifierref>{quiz['assignment_group_id']}</assignment_group_identifierref>
    <workflow_state>{quiz['workflow_state']}</workflow_state>
    <assignment_overrides>
    </assignment_overrides>
    <quiz_identifierref>{quiz['identifier']}</quiz_identifierref>
    <allowed_extensions></allowed_extensions>
    <has_group_category>false</has_group_category>
    <points_possible>{quiz['points_possible']}.0</points_possible>
    <grading_type>points</grading_type>
    <all_day>false</all_day>
    <submission_types>online_quiz</submission_types>
    <position>{quiz['position']}</position>
    <turnitin_enabled>false</turnitin_enabled>
    <vericite_enabled>false</vericite_enabled>
    <peer_review_count>0</peer_review_count>
    <peer_reviews>false</peer_reviews>
    <automatic_peer_reviews>false</automatic_peer_reviews>
    <anonymous_peer_reviews>false</anonymous_peer_reviews>
    <grade_group_students_individually>false</grade_group_students_individually>
    <freeze_on_copy>false</freeze_on_copy>
    <omit_from_final_grade>false</omit_from_final_grade>
    <hide_in_gradebook>false</hide_in_gradebook>
    <intra_group_peer_reviews>false</intra_group_peer_reviews>
    <only_visible_to_overrides>false</only_visible_to_overrides>
    <post_to_sis>false</post_to_sis>
    <moderated_grading>false</moderated_grading>
    <grader_count>0</grader_count>
    <grader_comments_visible_to_graders>true</grader_comments_visible_to_graders>
    <anonymous_grading>false</anonymous_grading>
    <graders_anonymous_to_graders>false</graders_anonymous_to_graders>
    <grader_names_visible_to_final_grader>true</grader_names_visible_to_final_grader>
    <anonymous_instructor_annotations>false</anonymous_instructor_annotations>
    <post_policy>
      <post_manually>false</post_manually>
    </post_policy>
  </assignment>
  <assignment_group_identifierref>{quiz['assignment_group_id']}</assignment_group_identifierref>
  <assignment_overrides>
  </assignment_overrides>
</quiz>
"""
        
        with open(quiz_dir / "assessment_meta.xml", 'w', encoding='utf-8') as f:
            f.write(meta_content)
        
        # Create assessment_qti.xml
        qti_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="{quiz['identifier']}" title="{quiz['title']}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
      <item ident="{quiz['question_id']}" title="Question">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>multiple_choice_question</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>{quiz['points_possible']}.0</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>original_answer_ids</fieldlabel>
              <fieldentry>5666,7024,7959,520</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>{quiz['assessment_question_id']}</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">&lt;div&gt;&lt;p&gt;Sample question: What is 2 + 2?&lt;/p&gt;&lt;/div&gt;</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Single">
            <render_choice>
              <response_label ident="5666">
                <material>
                  <mattext texttype="text/plain">3</mattext>
                </material>
              </response_label>
              <response_label ident="7024">
                <material>
                  <mattext texttype="text/plain">4</mattext>
                </material>
              </response_label>
              <response_label ident="7959">
                <material>
                  <mattext texttype="text/plain">5</mattext>
                </material>
              </response_label>
              <response_label ident="520">
                <material>
                  <mattext texttype="text/plain">6</mattext>
                </material>
              </response_label>
            </render_choice>
          </response_lid>
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">7024</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
      </item>
    </section>
  </assessment>
</questestinterop>
"""
        
        with open(quiz_dir / "assessment_qti.xml", 'w', encoding='utf-8') as f:
            f.write(qti_content)
        
        # Create QTI file in non_cc_assessments
        qti_file_id = f"g{uuid.uuid4().hex}"
        qti_path = output_path / "non_cc_assessments" / f"{quiz['identifier']}.xml.qti"
        qti_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(qti_path, 'w', encoding='utf-8') as f:
            f.write(qti_content)
        
        # Create additional QTI file
        additional_qti_path = output_path / "non_cc_assessments" / f"{qti_file_id}.xml.qti"
        with open(additional_qti_path, 'w', encoding='utf-8') as f:
            f.write(qti_content)
    
    def _create_announcement_files(self, output_path, announcement):
        """Create announcement and discussion topic files"""
        # Determine file paths based on resource href
        topic_file_path = None
        meta_file_path = None
        
        # Check if this is a standalone discussion (files in root) or module discussion (files in discussions/)
        for resource in self.resources:
            if resource['identifier'] == announcement['topic_id']:
                if resource['href'].startswith('discussions/'):
                    # Module discussion - files in discussions/ subdirectory
                    topic_file_path = output_path / resource['href']
                else:
                    # Standalone discussion - files in root directory
                    topic_file_path = output_path / resource['href']
                break
        
        for resource in self.resources:
            if resource['identifier'] == announcement['meta_id']:
                if resource['href'].startswith('discussions/'):
                    # Module discussion - files in discussions/ subdirectory
                    meta_file_path = output_path / resource['href']
                else:
                    # Standalone discussion - files in root directory
                    meta_file_path = output_path / resource['href']
                break
        
        # Create announcement topic XML (topic content)
        topic_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1  http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imsdt_v1p1.xsd">
  <title>{announcement['title']}</title>
  <text texttype="text/html">&lt;p&gt;{announcement.get('content', announcement.get('body', ''))}&lt;/p&gt;</text>
</topic>
"""
        
        # Ensure directory exists and write topic file
        if topic_file_path:
            topic_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(topic_file_path, 'w', encoding='utf-8') as f:
                f.write(topic_content)
        
        # Create announcement meta XML (topicMeta)
        meta_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<topicMeta identifier="{announcement['meta_id']}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <topic_id>{announcement['topic_id']}</topic_id>
  <title>{announcement['title']}</title>
  <position>{announcement.get('position', '')}</position>
  <type>{'topic' if 'body' in announcement else 'announcement'}</type>
  <discussion_type>threaded</discussion_type>
  <has_group_category>false</has_group_category>
  <workflow_state>{announcement['workflow_state']}</workflow_state>
  <module_locked>false</module_locked>
  <allow_rating>false</allow_rating>
  <only_graders_can_rate>false</only_graders_can_rate>
  <sort_by_rating>false</sort_by_rating>
  <sort_order>{'asc' if 'body' not in announcement else 'desc'}</sort_order>
  <sort_order_locked>false</sort_order_locked>
  <expanded>{'true' if 'body' not in announcement else 'false'}</expanded>
  <expanded_locked>false</expanded_locked>
  <todo_date/>
  <locked>{'true' if 'body' not in announcement else 'false'}</locked>
</topicMeta>
"""
        
        # Ensure directory exists and write meta file
        if meta_file_path:
            meta_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                f.write(meta_content)
    
    def _create_web_resource_file(self, output_path, file_info):
        """Create web resource file"""
        file_path = output_path / file_info['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_info['content'])
    
    def _create_imsmanifest_xml(self, filepath):
        """Create imsmanifest.xml file"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{self.manifest_id}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>{self.course_title}</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
      <lomimscc:lifeCycle>
        <lomimscc:contribute>
          <lomimscc:date>
            <lomimscc:dateTime>{today}</lomimscc:dateTime>
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
"""
        
        # Add organization items (modules)
        for org_item in self.organization_items:
            content += f"""        <item identifier="{org_item['identifier']}">
          <title>{org_item['title']}</title>
"""
            for item in org_item['items']:
                content += f"""          <item identifier="{item['identifier']}" identifierref="{item['identifierref']}">
            <title>{item['title']}</title>
          </item>
"""
            content += """        </item>
"""
        
        content += """      </item>
    </organization>
  </organizations>
  <resources>
"""
        
        # Add course settings resource
        content += f"""    <resource identifier="{self.course_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt">
      <file href="course_settings/course_settings.xml"/>
      <file href="course_settings/module_meta.xml"/>
      <file href="course_settings/assignment_groups.xml"/>
      <file href="course_settings/files_meta.xml"/>
      <file href="course_settings/late_policy.xml"/>
      <file href="course_settings/context.xml"/>
      <file href="course_settings/media_tracks.xml"/>
      <file href="course_settings/canvas_export.txt"/>
    </resource>
"""
        
        # Add all other resources
        for resource in self.resources:
            content += f"""    <resource identifier="{resource['identifier']}" type="{resource['type']}" href="{resource['href']}">
      <file href="{resource['href']}"/>
"""
            
            # Add assignment settings files
            if resource['type'] == 'associatedcontent/imscc_xmlv1p1/learning-application-resource' and resource['href'].endswith('.html'):
                assignment_id = resource['href'].split('/')[0]
                content += f"""      <file href="{assignment_id}/assignment_settings.xml"/>
"""
            
            # Add quiz dependency files
            if resource['type'] == 'imsqti_xmlv1p2/imscc_xmlv1p1/assessment':
                quiz_id = resource['href'].split('/')[0]
                content += f"""      <dependency identifierref="{resource['dependency']}"/>
"""
            
            # Add assessment meta files
            if resource['type'] == 'associatedcontent/imscc_xmlv1p1/learning-application-resource' and 'assessment_meta.xml' in resource['href']:
                quiz_id = resource['href'].split('/')[0]
                content += f"""      <file href="non_cc_assessments/{quiz_id}.xml.qti"/>
"""
            
            # Add announcement dependencies
            if resource['type'] == 'imsdt_xmlv1p1':
                content += f"""      <dependency identifierref="{resource['dependency']}"/>
"""
            
            content += """    </resource>
"""
        
        content += """  </resources>
</manifest>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def count_files_and_lines(directory):
    """Count files and lines in a directory"""
    file_count = 0
    line_count = 0
    
    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            file_count += 1
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count += len(f.readlines())
            except UnicodeDecodeError:
                # Handle binary files
                line_count += 1
    
    return file_count, line_count


def main():
    parser = argparse.ArgumentParser(description="Generate a Canvas Common Cartridge")
    parser.add_argument("output_dir", help="Output directory for generated cartridge")
    parser.add_argument("--title", default="Generated Course", help="Course title")
    parser.add_argument("--code", default="GEN101", help="Course code")
    parser.add_argument("--compare", help="Directory to compare against (e.g., produced_cartridge)")
    
    args = parser.parse_args()
    
    # Create generator
    generator = CartridgeGenerator(args.title, args.code)
    
    # Create base cartridge
    print(f"Creating base cartridge: {args.output_dir}")
    generator.create_base_cartridge(args.output_dir)
    
    # Add modules
    print("Adding module...")
    module_id_test1 = generator.add_module("test1", position=1, published=True)

    print("Adding module...")
    module_id_test2 = generator.add_module("test2", position=2, published=True)

    print("Adding module...")
    module_id_test3 = generator.add_module("test3", position=3, published=True)

    #selecting module 1,2, and 3
    selected_module_1_id = (generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "test1")]).identifier.item()
    selected_module_2_id = (generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "test2")]).identifier.item()
    selected_module_3_id = (generator.df[(generator.df["type"] == "module") & (generator.df["title"] == "test3")]).identifier.item()

    # Add wiki page to selected existing module
    print("Adding wiki page to existing module...")
    generator.add_wiki_page_to_module(selected_module_1_id, "test_wiki_page1", "<p>This is test1 wiki content</p>", published=True)
    generator.add_wiki_page_to_module(selected_module_2_id, "test_wiki_page2", "<p>This is test2 wiki content</p>", published=True)
    generator.add_wiki_page_to_module(selected_module_3_id, "test_wiki_page3", "<p>This is test3 wiki content</p>", published=True)
    
    # Add assignment to selected existing module
    print("Adding assignment to existing module...")
    generator.add_assignment_to_module(selected_module_2_id, "Module 2 Assignment", "<p>Complete this assignment for module 2</p>", points=50, published=True)
    
    # Add quiz to selected existing module  
    print("Adding quiz to existing module...")
    generator.add_quiz_to_module(selected_module_3_id, "Module 3 Quiz", "Test your knowledge of module 3", points=25, published=True)
    
    # Add discussion to selected existing module
    print("Adding discussion to existing module...")
    generator.add_discussion_to_module(selected_module_1_id, "Module 1 Discussion", "<p>Let's discuss the topics from module 1</p>", published=True)
    
    # Add file to selected existing module
    print("Adding file to existing module...")
    generator.add_file_to_module(selected_module_1_id, "module_file.txt", "This file is attached to module 1")

    '''
    # Add standalone discussion (not attached to any module)
    print("Adding standalone discussion...")
    generator.add_standalone_discussion("Standalone Discussion", "<p>This is a standalone discussion not attached to any module</p>", published=True)
    
    # Add standalone file
    print("Adding standalone file...")
    generator.add_file_standalone("hello.txt", "hello world!")

    # Add standalone wiki page (not attached to any module)
    print("Adding standalone wiki page...")
    generator.add_standalone_wiki_page("standalone_wiki_page", "<p>This is a standalone wiki page not attached to any module</p>", published=True)

    # Add assignment
    print("Adding assignment...")
    generator.add_assignment("my first assignment", "write me 100 words about why the sky is blue. ", 100, published=True)
    
    # Add quiz
    print("Adding quiz...")
    generator.add_quiz("my first quiz!", "only 1 attempt. good luck.", 1, published=True)

    #Add discussion topic to module
    print("Adding discussion topic...")
    generator.add_discussion_topic(module_id, "My First Discussion", "<p>This is the body of the discussion.</p>", published=True)
    '''

    #zip the cartridge
    shutil.make_archive('./generated_cartridge','zip','./generated_cartridge')
    # Save current state to HTML
    with open("table_inspect.html", "w") as f:
        f.write(generator.df.to_html())

    # Compare with reference if provided
    # if args.compare and Path(args.compare).exists():
    #     print(f"\nComparing with {args.compare}...")
    #     
    #     gen_files, gen_lines = count_files_and_lines(args.output_dir)
    #     ref_files, ref_lines = count_files_and_lines(args.compare)
    #     
    #     print(f"Generated cartridge: {gen_files} files, {gen_lines} lines")
    #     print(f"Reference cartridge: {ref_files} files, {ref_lines} lines")
    #     
    #     if gen_files == ref_files:
    #         print("✓ File count matches!")
    #     else:
    #         print(f"✗ File count differs: {gen_files} vs {ref_files}")
    #     
    #     if gen_lines == ref_lines:
    #         print("✓ Line count matches!")
    #     else:
    #         print(f"✗ Line count differs: {gen_lines} vs {ref_lines}")


if __name__ == "__main__":
    main()

# QUICK REFERENCE - COMMAND LINE EXAMPLES:
# python cartridge_generator.py my_new_cartridge
# python cartridge_generator.py generated_course --title "Introduction to Python" --code "CS101" 
# python cartridge_generator.py biology_101 --title "Biology Fundamentals" --code "BIO101"