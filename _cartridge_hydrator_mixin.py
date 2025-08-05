#!/usr/bin/env python3
"""
Cartridge Hydrator Mixin
Provides functionality to hydrate a CartridgeGenerator from an existing cartridge directory
"""

from pathlib import Path
from cartridge_replicator import scan_cartridge


class CartridgeHydratorMixin:
    """Mixin to add cartridge hydration capabilities"""
    
    def hydrate_from_existing_cartridge(self, cartridge_path):
        """
        Hydrate the generator by scanning an existing cartridge directory
        
        Args:
            cartridge_path (str): Path to existing cartridge directory
            
        Returns:
            bool: True if hydration successful, False otherwise
        """
        cartridge_path = Path(cartridge_path)
        
        if not cartridge_path.exists():
            print(f"Error: Cartridge directory {cartridge_path} does not exist")
            return False
            
        if not (cartridge_path / "imsmanifest.xml").exists():
            print(f"Error: {cartridge_path} does not contain imsmanifest.xml - not a valid cartridge")
            return False
        
        print(f"Hydrating from existing cartridge: {cartridge_path}")
        
        # Set output directory to the existing cartridge
        self.output_dir = str(cartridge_path)
        
        # Scan the existing cartridge to populate DataFrame
        self.current_df = scan_cartridge(cartridge_path)
        
        if self.current_df is None or self.current_df.empty:
            print("Error: Failed to scan cartridge or cartridge is empty")
            return False
        
        # Extract course information from the DataFrame
        self._extract_course_info_from_df()
        
        # Hydrate internal data structures from DataFrame
        self._hydrate_internal_structures()
        
        print(f"Cartridge hydrated successfully. Found {len(self.current_df)} components.")
        print(f"Component types: {dict(self.current_df['type'].value_counts())}")
        
        return True
    
    def _extract_course_info_from_df(self):
        """Extract course title and code from the hydrated DataFrame"""
        # Try to get course info from course_settings
        course_settings = self.current_df[self.current_df['type'] == 'course_settings']
        if not course_settings.empty:
            xml_content = course_settings.iloc[0]['xml_content']
            if xml_content:
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(xml_content)
                    
                    # Extract course title
                    title_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}title')
                    if title_elem is not None and title_elem.text:
                        self.course_title = title_elem.text
                    
                    # Extract course code
                    code_elem = root.find('.//{http://canvas.instructure.com/xsd/cccv1p0}course_code')
                    if code_elem is not None and code_elem.text:
                        self.course_code = code_elem.text
                        
                    # Extract course identifier
                    course_id = root.get('identifier')
                    if course_id:
                        self.course_id = course_id
                        
                except ET.ParseError:
                    print("Warning: Could not parse course_settings.xml")
        
        print(f"Course info - Title: '{self.course_title}', Code: '{self.course_code}', ID: '{self.course_id}'")
    
    def _hydrate_internal_structures(self):
        """Hydrate internal data structures from the DataFrame"""
        # Clear existing structures
        self.modules = []
        self.assignments = []
        self.quizzes = []
        self.announcements = []
        self.wiki_pages = []
        self.files = []
        self.resources = []
        self.organization_items = []
        
        # Hydrate modules
        modules = self.current_df[self.current_df['type'] == 'module']
        for _, module_row in modules.iterrows():
            module = {
                'identifier': module_row['identifier'],
                'title': module_row['title'],
                'position': int(module_row['position']) if module_row['position'] else 1,
                'workflow_state': module_row['workflow_state'] or 'published',
                'items': []
            }
            
            # Find module items for this module
            module_items = self.current_df[
                (self.current_df['type'] == 'module_item') & 
                (self.current_df['identifierref'].notna())
            ]
            
            for _, item_row in module_items.iterrows():
                # This is a simplification - in a real scenario you'd need to match items to modules
                # For now, we'll add all items to all modules (this should be refined)
                item = {
                    'identifier': item_row['identifier'],
                    'content_type': item_row['content_type'] or 'WikiPage',  # Default to WikiPage if missing
                    'workflow_state': item_row['workflow_state'] or 'published',
                    'title': item_row['title'],
                    'identifierref': item_row['identifierref'],
                    'position': int(item_row['position']) if item_row['position'] else 1
                }
                module['items'].append(item)
            
            self.modules.append(module)
            
            # Add to organization structure
            self.organization_items.append({
                'identifier': module['identifier'],
                'title': module['title'],
                'type': 'module',
                'items': module['items']
            })
        
        # Hydrate resources from DataFrame
        resources = self.current_df[self.current_df['type'] == 'resource']
        for _, resource_row in resources.iterrows():
            resource = {
                'identifier': resource_row['identifier'],
                'type': resource_row['resource_type'],
                'href': resource_row['href']
            }
            # Add dependency if it exists (for quizzes, announcements, etc.)
            if resource_row['resource_type'] in ['imsqti_xmlv1p2/imscc_xmlv1p1/assessment', 'imsdt_xmlv1p1']:
                # Find corresponding meta resource
                meta_resources = self.current_df[
                    (self.current_df['type'] == 'resource') & 
                    (self.current_df['href'].str.contains('assessment_meta.xml|topicMeta', na=False))
                ]
                if not meta_resources.empty:
                    resource['dependency'] = meta_resources.iloc[0]['identifier']
            
            self.resources.append(resource)
        
        # Hydrate wiki pages
        wiki_pages = self.current_df[self.current_df['type'] == 'wiki_page']
        for _, wiki_row in wiki_pages.iterrows():
            wiki_page = {
                'identifier': wiki_row['identifier'],
                'resource_id': wiki_row['identifier'],
                'title': wiki_row['title'],
                'filename': wiki_row['filename'],
                'workflow_state': wiki_row['workflow_state'] or 'published',
                'content': self._extract_content_from_html(wiki_row['xml_content'])
            }
            self.wiki_pages.append(wiki_page)
        
        # Hydrate assignments
        assignment_settings = self.current_df[self.current_df['type'] == 'assignment_settings']
        
        # Extract assignment_group_id from the first assignment if it exists
        if not assignment_settings.empty:
            first_assignment_xml = assignment_settings.iloc[0]['xml_content']
            extracted_group_id = self._extract_assignment_group_id_from_xml(first_assignment_xml)
            if extracted_group_id:
                self.assignment_group_id = extracted_group_id
        
        for i, (_, assignment_row) in enumerate(assignment_settings.iterrows()):
            assignment = {
                'identifier': assignment_row['identifier'],
                'title': assignment_row['title'],
                'workflow_state': assignment_row['workflow_state'] or 'published',
                'points_possible': self._extract_points_from_assignment_xml(assignment_row['xml_content']),
                'content': self._extract_assignment_content(assignment_row['identifier']),
                'assignment_group_id': self.assignment_group_id,
                'position': i + 1
            }
            self.assignments.append(assignment)
        
        # Hydrate quizzes
        assessment_meta = self.current_df[self.current_df['type'] == 'assessment_meta']
        for i, (_, quiz_row) in enumerate(assessment_meta.iterrows()):
            quiz = {
                'identifier': quiz_row['identifier'],
                'title': quiz_row['title'],
                'workflow_state': quiz_row['workflow_state'] or 'published',
                'points_possible': self._extract_points_from_quiz_xml(quiz_row['xml_content']),
                'description': self._extract_description_from_quiz_xml(quiz_row['xml_content']),
                'assignment_group_id': self.assignment_group_id,
                'position': i + 1,
                'assignment_id': f"a{quiz_row['identifier'][1:]}",  # Convert quiz ID to assignment ID format
                'question_id': f"q{quiz_row['identifier'][1:]}",
                'assessment_question_id': f"aq{quiz_row['identifier'][1:]}"
            }
            self.quizzes.append(quiz)
        
        # Hydrate discussions (stored in announcements list)
        discussion_meta = self.current_df[self.current_df['type'] == 'discussion_topic_meta']
        for _, discussion_row in discussion_meta.iterrows():
            discussion = {
                'topic_id': self._extract_topic_id_from_discussion_xml(discussion_row['xml_content']),
                'meta_id': discussion_row['identifier'],
                'title': discussion_row['title'],
                'body': self._extract_discussion_content(discussion_row['identifier']),
                'workflow_state': discussion_row['workflow_state'] or 'active'
            }
            self.announcements.append(discussion)
        
        # Hydrate files
        web_files = self.current_df[self.current_df['type'] == 'web_resources_file']
        for _, file_row in web_files.iterrows():
            # Get the corresponding resource entry to find the identifier
            file_resource = self.current_df[
                (self.current_df['type'] == 'resource') & 
                (self.current_df['href'] == file_row['href'])
            ]
            
            if not file_resource.empty:
                file_info = {
                    'identifier': file_resource.iloc[0]['identifier'],
                    'filename': file_row['title'] + '.txt' if '.' not in file_row['title'] else file_row['title'],
                    'content': file_row['xml_content'] or '',
                    'path': file_row['href']
                }
                self.files.append(file_info)
        
        print(f"Hydrated {len(self.modules)} modules, {len(self.resources)} resources, {len(self.wiki_pages)} wiki pages, {len(self.assignments)} assignments, {len(self.quizzes)} quizzes, {len(self.announcements)} discussions, {len(self.files)} files")
    
    def _extract_content_from_html(self, html_content):
        """Extract body content from HTML"""
        if not html_content:
            return ""
        
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(html_content)
            body = root.find('.//body')
            if body is not None:
                # Return the inner text/HTML of the body
                content = ET.tostring(body, encoding='unicode', method='html')
                # Remove the body tags
                content = content.replace('<body>', '').replace('</body>', '')
                return content.strip()
        except ET.ParseError:
            pass
        
        return html_content
    
    def _extract_points_from_assignment_xml(self, xml_content):
        """Extract points possible from assignment XML"""
        if not xml_content:
            return 100
        
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_content)
            points_elem = root.find('.//points_possible')
            if points_elem is not None and points_elem.text:
                return float(points_elem.text)
        except (ET.ParseError, ValueError):
            pass
        
        return 100
    
    def _extract_assignment_content(self, assignment_id):
        """Extract assignment content from the assignment_content row"""
        assignment_content = self.current_df[
            (self.current_df['type'] == 'assignment_content') & 
            (self.current_df['identifier'] == assignment_id)
        ]
        
        if not assignment_content.empty:
            return self._extract_content_from_html(assignment_content.iloc[0]['xml_content'])
        
        return ""
    
    def _extract_assignment_group_id_from_xml(self, xml_content):
        """Extract assignment_group_identifierref from assignment XML"""
        if not xml_content:
            return None
        
        import re
        match = re.search(r'<assignment_group_identifierref>([^<]+)</assignment_group_identifierref>', xml_content)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_points_from_quiz_xml(self, xml_content):
        """Extract points possible from quiz XML"""
        if not xml_content:
            return 10
        
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_content)
            points_elem = root.find('.//points_possible')
            if points_elem is not None and points_elem.text:
                return int(float(points_elem.text))
        except (ET.ParseError, ValueError):
            pass
        
        return 10
    
    def _extract_description_from_quiz_xml(self, xml_content):
        """Extract description from quiz XML"""
        if not xml_content:
            return ""
        
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(xml_content)
            desc_elem = root.find('.//description')
            if desc_elem is not None and desc_elem.text:
                # Decode HTML entities in the description
                import html
                return html.unescape(desc_elem.text)
        except ET.ParseError:
            pass
        
        return ""
    
    def _extract_topic_id_from_discussion_xml(self, xml_content):
        """Extract topic_id from discussion XML"""
        if not xml_content:
            return None
        
        import re
        # Use regex to extract topic_id since XML namespaces can complicate parsing
        match = re.search(r'<topic_id>([^<]+)</topic_id>', xml_content)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_discussion_content(self, discussion_id):
        """Extract discussion content from the discussion_topic_content row"""
        discussion_content = self.current_df[
            (self.current_df['type'] == 'discussion_topic_content') & 
            (self.current_df['filename'].str.contains(f'{discussion_id}', na=False))
        ]
        
        if not discussion_content.empty:
            return self._extract_content_from_html(discussion_content.iloc[0]['xml_content'])
        
        return ""
    
    def get_hydration_summary(self):
        """Get a summary of the hydrated cartridge"""
        if self.current_df is None:
            return "No cartridge hydrated"
        
        summary = {
            'total_components': len(self.current_df),
            'component_types': dict(self.current_df['type'].value_counts()),
            'course_title': self.course_title,
            'course_code': self.course_code,
            'modules_count': len(self.modules),
            'resources_count': len(self.resources),
            'wiki_pages_count': len(self.wiki_pages)
        }
        
        return summary