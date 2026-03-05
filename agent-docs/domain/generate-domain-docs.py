#!/usr/bin/env python3
"""
generate_domain_docs.py
Extracts domain information from JUDO model and generates documentation
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# Define namespaces for ESM model
NAMESPACES = {
    'xmi': 'http://www.omg.org/XMI',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'namespace': 'http://blackbelt.hu/judo/meta/esm/namespace',
    'structure': 'http://blackbelt.hu/judo/meta/esm/structure',
    'type': 'http://blackbelt.hu/judo/meta/esm/type',
    'accesspoint': 'http://blackbelt.hu/judo/meta/esm/accesspoint',
    'measure': 'http://blackbelt.hu/judo/meta/esm/measure',
    'ui': 'http://blackbelt.hu/judo/meta/esm/ui'
}

def extract_entities(esm_file):
    """Extract entity information from ESM model"""
    tree = ET.parse(esm_file)
    root = tree.getroot()
    
    entities = []
    
    # Find all elements with xsi:type="structure:EntityType"
    for entity in root.findall(".//*[@{http://www.w3.org/2001/XMLSchema-instance}type='structure:EntityType']"):
        entity_name = entity.get('name')
        
        # Find parent package
        package_name = None
        parent = find_parent_package(root, entity)
        if parent is not None:
            package_name = parent.get('name')
        
        # Extract attributes
        attributes = []
        for attr in entity.findall(".//*[@{http://www.w3.org/2001/XMLSchema-instance}type='structure:DataMember']"):
            attr_name = attr.get('name')
            attr_required = attr.get('required', 'false') == 'true'
            attr_type = get_type_name(attr.get('dataType'))
            
            attributes.append({
                'name': attr_name,
                'type': attr_type,
                'required': attr_required,
                'documentation': ''
            })
        
        # Extract relationships
        relationships = []
        for rel in entity.findall(".//*[@{http://www.w3.org/2001/XMLSchema-instance}type='structure:OneWayRelationMember']"):
            rel_name = rel.get('name')
            rel_target = rel.get('target')
            rel_kind = rel.get('relationKind', 'ASSOCIATION')
            lower = rel.get('lower', '0')
            upper = rel.get('upper', '1')
            
            cardinality = f"{lower}..{'*' if upper == '-1' else upper}"
            
            relationships.append({
                'name': rel_name,
                'target': get_entity_name_from_id(root, rel_target),
                'cardinality': cardinality,
                'kind': rel_kind
            })
        
        entities.append({
            'name': entity_name,
            'package': package_name,
            'documentation': '',
            'attributes': attributes,
            'relationships': relationships
        })
    
    return entities

def find_parent_package(root, entity):
    """Find the parent package of an entity"""
    for package in root.findall(".//*[@{http://www.w3.org/2001/XMLSchema-instance}type='namespace:Package']"):
        for child in package:
            if child == entity:
                return package
    return None

def get_entity_name_from_id(root, entity_id):
    """Get entity name from XMI ID"""
    if not entity_id:
        return 'Unknown'
    
    entity = root.find(f".//*[@xmi:id='{entity_id}']", NAMESPACES)
    if entity is not None:
        return entity.get('name', 'Unknown')
    return 'Unknown'

def get_type_name(type_id):
    """Convert type ID to readable name"""
    # This is a simplified version - in a real implementation,
    # you would look up the type definition
    type_map = {
        'PZ94Agq6Ee6tvPbknJiimg': 'String',
        'PZ94Bwq6Ee6tvPbknJiimg': 'Boolean',
        'PZ94BAq6Ee6tvPbknJiimg': 'Integer',
        'PZ94Bgq6Ee6tvPbknJiimg': 'Decimal',
    }
    return type_map.get(type_id, 'Unknown')

def extract_database_schema(liquibase_file):
    """Extract database schema from Liquibase changelog"""
    tree = ET.parse(liquibase_file)
    root = tree.getroot()
    
    # Use wildcard namespace matching for dynamic namespaces
    tables = {}
    
    # Find all createTable elements regardless of namespace prefix
    for create_table in root.iter():
        if create_table.tag.endswith('createTable'):
            table_name = create_table.get('tableName')
            if table_name:
                tables[table_name] = {
                    'columns': [],
                    'foreign_keys': []
                }
                
                # Extract columns from this createTable element
                for column in create_table.iter():
                    if column.tag.endswith('column'):
                        col_name = column.get('name')
                        col_type = column.get('type')
                        if col_name and col_type:
                            tables[table_name]['columns'].append({
                                'name': col_name,
                                'type': col_type
                            })
    
    # Extract foreign keys
    for fk in root.iter():
        if fk.tag.endswith('addForeignKeyConstraint'):
            base_table = fk.get('baseTableName')
            if base_table and base_table in tables:
                tables[base_table]['foreign_keys'].append({
                    'column': fk.get('baseColumnNames'),
                    'referenced_table': fk.get('referencedTableName'),
                    'referenced_column': fk.get('referencedColumnNames')
                })
    
    return tables

def generate_entity_reference(entities, output_file):
    """Generate entity-reference.md from extracted data"""
    with open(output_file, 'w') as f:
        f.write("# Complete Entity Reference\n\n")
        f.write("This document provides detailed information about all entities in the Webshop domain model.\n\n")
        f.write(f"**Total Entities**: {len(entities)}\n\n")
        
        f.write("## Entity Summary\n\n")
        f.write("| Entity | Package | Attributes | Relationships |\n")
        f.write("|--------|---------|------------|---------------|\n")
        
        for entity in sorted(entities, key=lambda e: e['name']):
            package = entity['package'] or 'root'
            attr_count = len(entity['attributes'])
            rel_count = len(entity['relationships'])
            f.write(f"| [{entity['name']}](#{entity['name'].lower()}) | {package} | {attr_count} | {rel_count} |\n")
        
        f.write("\n---\n\n")
        
        # Write detailed entity sections
        for entity in sorted(entities, key=lambda e: e['name']):
            f.write(f"## {entity['name']}\n\n")
            f.write(f"**Package**: `{entity['package'] or 'root'}`  \n")
            f.write(f"**Database Table**: `T_ENTITIES_{entity['name'].upper()}`  \n\n")
            
            # Attributes
            if entity['attributes']:
                f.write("### Attributes\n\n")
                f.write("| Attribute | Type | Required | Description |\n")
                f.write("|-----------|------|----------|-------------|\n")
                for attr in sorted(entity['attributes'], key=lambda a: a['name']):
                    required = "✓" if attr['required'] else ""
                    f.write(f"| `{attr['name']}` | {attr['type']} | {required} | {attr.get('documentation', '')} |\n")
                f.write("\n")
            else:
                f.write("*No attributes defined*\n\n")
            
            # Relationships
            if entity['relationships']:
                f.write("### Relationships\n\n")
                f.write("| Relationship | Type | Target | Cardinality |\n")
                f.write("|--------------|------|--------|-------------|\n")
                for rel in sorted(entity['relationships'], key=lambda r: r['name']):
                    f.write(f"| `{rel['name']}` | {rel['kind']} | [{rel['target']}](#{rel['target'].lower()}) | {rel['cardinality']} |\n")
                f.write("\n")
            else:
                f.write("*No relationships defined*\n\n")
            
            f.write("---\n\n")

def generate_er_diagram(tables, output_file):
    """Generate Mermaid ER diagram from database schema"""
    OPEN_BRACE = chr(123) + chr(123)  # Double opening brace
    
    # Filter to only entity tables (T_ENTITIES_*)
    entity_tables = {k: v for k, v in tables.items() if k.startswith('T_ENTITIES_')}
    
    with open(output_file, 'w') as f:
        f.write("# Entity Relationship Diagram\n\n")
        f.write("This diagram shows the database schema relationships between entities.\n\n")
        f.write("```mermaid\n")
        f.write("erDiagram\n")

        # Write relationships
        for table_name, table_data in entity_tables.items():
            for fk in table_data['foreign_keys']:
                ref_table = fk['referenced_table']
                if ref_table in entity_tables:
                    fk_column = fk['column']
                    # Simplify table names for readability
                    source = table_name.replace('T_ENTITIES_', '')
                    target = ref_table.replace('T_ENTITIES_', '')
                    f.write(f'    {source} }}o--|| {target} : "{fk_column}"\n')
        
        f.write("\n")
        
        # Write table definitions (limited to key columns for readability)
        for table_name, table_data in sorted(entity_tables.items()):
            simple_name = table_name.replace('T_ENTITIES_', '')
            f.write(f"    {simple_name} {OPEN_BRACE}\n")
            
            # Show first 8 columns
            for column in table_data['columns'][:8]:
                col_name = column['name']
                col_type = column['type'].split('(')[0]  # Remove size specs
                f.write(f'        {col_type} {col_name}\n')
            
            if len(table_data['columns']) > 8:
                f.write(f'        string ... ({len(table_data["columns"]) - 8} more)\n')
            
            f.write("    }\n")
        
        f.write("```\n")

if __name__ == "__main__":
    # Paths to model files
    ESM_FILE = Path("model/webshop.model")
    LIQUIBASE_FILE = Path("application/model/target/generated-resources/model/webshop-liquibase_postgresql.changelog.xml")
    OUTPUT_DIR = Path("agent-docs/domain")
    
    print("Extracting entities from ESM model...")
    entities = extract_entities(ESM_FILE)
    print(f"  Found {len(entities)} entities")
    
    print("Extracting database schema from Liquibase...")
    tables = extract_database_schema(LIQUIBASE_FILE)
    entity_tables = {k: v for k, v in tables.items() if k.startswith('T_ENTITIES_')}
    print(f"  Found {len(entity_tables)} entity tables (out of {len(tables)} total tables)")
    
    print("Generating entity-reference.md...")
    generate_entity_reference(entities, OUTPUT_DIR / "entity-reference.md")
    
    print("Generating ER diagram...")
    generate_er_diagram(tables, OUTPUT_DIR / "er-diagram.md")
    
    print("\n✓ Domain documentation generated successfully!")
    print(f"  - {OUTPUT_DIR / 'entity-reference.md'}")
    print(f"  - {OUTPUT_DIR / 'er-diagram.md'}")
