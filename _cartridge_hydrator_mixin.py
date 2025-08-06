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
        
        # Create a mapping of module_id -> items from organization structure first
        module_items_map = {}
        manifest_row = self.current_df[self.current_df['type'] == 'manifest']
        if not manifest_row.empty:
            try:
                import xml.etree.ElementTree as ET
                manifest_xml = manifest_row.iloc[0]['xml_content']
                root = ET.fromstring(manifest_xml)
                
                # Find LearningModules organization to get proper module-item hierarchy
                learning_modules = root.find('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item[@identifier="LearningModules"]')
                if learning_modules is not None:
                    for module_item in learning_modules.findall('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
                        if module_item.get('identifier') != 'LearningModules':
                            module_id = module_item.get('identifier')
                            items = []
                            
                            # Get child items of this module
                            for child in module_item.findall('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
                                if child != module_item:  # Don't include the module itself
                                    child_id = child.get('identifier')
                                    child_ref = child.get('identifierref')
                                    child_title_elem = child.find('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
                                    child_title = child_title_elem.text if child_title_elem is not None else None
                                    
                                    if child_title:
                                        items.append({
                                            'identifier': child_id,
                                            'identifierref': child_ref,
                                            'title': child_title
                                        })
                            
                            module_items_map[module_id] = items
                            
            except ET.ParseError:
                print("Warning: Could not parse organization structure from manifest")
        
        # Hydrate modules using proper module-item mapping
        modules = self.current_df[self.current_df['type'] == 'module']
        for _, module_row in modules.iterrows():
            module_id = module_row['identifier']
            module = {
                'identifier': module_id,
                'title': module_row['title'],
                'position': int(module_row['position']) if module_row['position'] else 1,
                'workflow_state': module_row['workflow_state'] or 'published',
                'items': []
            }
            
            # Get items that actually belong to this module from organization structure
            org_items = module_items_map.get(module_id, [])
            
            # Match organization items with module_item data from DataFrame
            all_module_items = self.current_df[self.current_df['type'] == 'module_item']
            
            for org_item in org_items:
                # Find matching module_item data
                matching_item = all_module_items[all_module_items['identifier'] == org_item['identifier']]
                if not matching_item.empty:
                    item_row = matching_item.iloc[0]
                    item = {
                        'identifier': org_item['identifier'],
                        'content_type': item_row['content_type'] or 'WikiPage',
                        'workflow_state': item_row['workflow_state'] or 'published',
                        'title': org_item['title'],
                        'identifierref': org_item['identifierref'],
                        'position': int(item_row['position']) if item_row['position'] else 1
                    }
                    module['items'].append(item)
            
            self.modules.append(module)
            
            # Add to organization structure with proper items
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
                'resource_id': wiki_row['identifier'],
                'title': wiki_row['title'],
                'filename': wiki_row['filename'],
                'workflow_state': wiki_row['workflow_state'] or 'published',
                'content': self._extract_content_from_html(wiki_row['xml_content'])
            }
            self.wiki_pages.append(wiki_page)
        
        print(f"Hydrated {len(self.modules)} modules, {len(self.resources)} resources, {len(self.wiki_pages)} wiki pages")
    
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