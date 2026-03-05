"""
Diagram Generator for JUDO ESM models.

This script parses a Sirius '.aird' file to find diagram definitions and
a corresponding ESM '.model' file (XMI) to extract the model structure.
It then generates a Markdown file containing class diagrams in either
PlantUML (default) or Mermaid format.

Prerequisites:
- Python 3

How to run:
1. Make sure you are in the root directory of the `kopogtato-manager` project.
2. Run the script from your terminal:

   # Generate PlantUML diagrams (default)
   python docs/domain/diagram_generator.py \\
     representations.aird \\
     application/model/target/generated-resources/model/kopogtato-esm.model \\
     docs/domain/generated-diagrams.md

   # Generate Mermaid diagrams
   python docs/domain/diagram_generator.py \\
     representations.aird \\
     application/model/target/generated-resources/model/kopogtato-esm.model \\
     docs/domain/generated-diagrams.md \\
     --format mermaid

   - Argument 1: Path to the .aird file.
   - Argument 2: Path to the .model file.
   - Argument 3: Path for the output Markdown file.
"""

import xml.etree.ElementTree as ET
import argparse
import sys

# Namespaces used in the XML files for parsing.
NAMESPACES = {
    "xmi": "http://www.omg.org/XMI",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "viewpoint": "http://www.eclipse.org/sirius/1.1.0",
    "description_3": "http://www.eclipse.org/sirius/diagram/description/1.1.0",
    "namespace": "http://blackbelt.hu/judo/meta/esm/namespace",
    "structure": "http://blackbelt.hu/judo/meta/esm/structure",
    "type": "http://blackbelt.hu/judo/meta/esm/type",
}

def _ns(key, attr):
    """Helper to build namespace-qualified attribute names."""
    return chr(123) + NAMESPACES[key] + chr(125) + attr


def find_diagrams(aird_tree):
    """
    Parses the .aird file tree to find all entity diagrams.
    Returns a list of tuples, each containing (diagram_name, target_href).
    """
    diagrams = []
    for desc in aird_tree.findall(".//ownedRepresentationDescriptors", NAMESPACES):
        description = desc.find("description", NAMESPACES)
        if (
            description is not None
            and description.get(_ns('xmi', 'type'))
            == "description_3:DiagramDescription"
        ):
            desc_href = description.get("href", "")
            if "diagramEntity" in desc_href:
                diagram_name = desc.get("name")
                target = desc.find("target", NAMESPACES)
                if target is not None:
                    target_href = target.get("href")
                    diagrams.append((diagram_name, target_href))
    return diagrams


def parse_model(model_path):
    """
    Parses the .model file and creates a lookup map from xmi:id to element.
    Returns the root of the tree and the map.
    """
    tree = ET.parse(model_path)
    root = tree.getroot()
    id_map = {
        elem.get(_ns('xmi', 'id')): elem
        for elem in root.iter()
        if elem.get(_ns('xmi', 'id'))
    }
    return root, id_map


def get_elements_from_package(package_element):
    """
    Extracts all supported model elements from a given Package element.
    """
    elements = []
    for elem in package_element.findall("./elements", NAMESPACES):
        elem_type = elem.get(_ns('xsi', 'type'))
        if elem_type in [
            "structure:EntityType",
            "structure:TransferObjectType",
            "type:EnumerationType",
        ]:
            elements.append(elem)
    return elements


def get_cardinality_string(rel_element):
    """Formats the cardinality string for a diagram relation."""
    lower = rel_element.get("lower")
    upper = rel_element.get("upper")
    if lower is None and upper is None:
        return ""
    lower = lower or "0"
    upper = upper or "-1"
    if lower == "1" and upper == "1":
        return "1"
    if lower == "0" and upper == "1":
        return "0..1"
    if lower == "1" and upper == "-1":
        return "1..*"
    if lower == "0" and upper == "-1":
        return "*"
    return f"{lower}..{upper.replace('-1', '*')}"


def generate_plantuml_diagram(diagram_name, elements, id_map):
    """Generates a PlantUML class diagram string."""
    if not elements:
        return ""

    OPEN_BRACE = chr(123) + chr(123)  # Double opening brace
    puml_string = f"## {diagram_name}\n\n"
    puml_string += "```plantuml\n"
    puml_string += "@startuml\n"
    puml_string += "'!theme vibrant\n"
    puml_string += "hide empty members\n"
    puml_string += "skinparam classAttributeIconSize 0\n\n"

    relations_to_draw = []
    inheritance_to_draw = []
    element_names = {e.get("name") for e in elements}

    for element in elements:
        element_name = element.get("name")
        elem_type = element.get(_ns('xsi', 'type'))

        stereotype, keyword = "", "class"
        if elem_type == "type:EnumerationType":
            stereotype, keyword = "<<Enumeration>>", "enum"
        elif elem_type == "structure:EntityType":
            stereotype = "<<EntityType>>"
        elif elem_type == "structure:TransferObjectType":
            stereotype = "<<TransferObjectType>>"

        puml_string += f'{keyword} "{element_name}" as {element_name} {stereotype} {OPEN_BRACE}\n'
        if elem_type == "type:EnumerationType":
            for literal in element.findall("members", NAMESPACES):
                puml_string += f"  {literal.get('name')}\n"
        else:
            for attr in element.findall("attributes", NAMESPACES):
                puml_string += f"  + {attr.get('name')}\n"
        puml_string += "}\n\n"

        for rel in element.findall("relations", NAMESPACES):
            target_id = rel.get("target")
            if target_id and target_id in id_map:
                target_element = id_map[target_id]
                target_name = target_element.get("name")
                if target_name in element_names:
                    rel_name = rel.get("name", "")
                    cardinality = get_cardinality_string(rel)
                    relations_to_draw.append(
                        f'{element_name} --> "{cardinality}" {target_name} : {rel_name}'
                    )

        for gen in element.findall("generalization", NAMESPACES):
            superclass_id = gen.get("general")
            if superclass_id and superclass_id in id_map:
                superclass_element = id_map[superclass_id]
                superclass_name = superclass_element.get("name")
                if superclass_name in element_names:
                    inheritance_to_draw.append(f"{superclass_name} <|-- {element_name}")

    for line in sorted(list(set(relations_to_draw + inheritance_to_draw))):
        puml_string += line + "\n"

    puml_string += "@enduml\n"
    puml_string += "```\n\n"
    return puml_string


def generate_mermaid_diagram(diagram_name, elements, id_map):
    """Generates a Mermaid class diagram string."""
    if not elements:
        return ""

    OPEN_BRACE = chr(123) + chr(123)  # Double opening brace
    mermaid_string = f"## {diagram_name}\n\n"
    mermaid_string += "```mermaid\n"
    mermaid_string += "%%{ init: { 'class': { 'defaultRenderer': 'elk' } } }%%\n"
    mermaid_string += "classDiagram\n"

    relations_to_draw = []
    inheritance_to_draw = []
    element_names = {e.get("name") for e in elements}

    for element in elements:
        element_name = element.get("name")
        elem_type = element.get(_ns('xsi', 'type'))

        stereotype = ""
        if elem_type == "type:EnumerationType":
            stereotype = "Enumeration"
        elif elem_type == "structure:EntityType":
            stereotype = "EntityType"
        elif elem_type == "structure:TransferObjectType":
            stereotype = "TransferObjectType"

        mermaid_string += f"  class {element_name} {OPEN_BRACE}\n"
        if stereotype:
            mermaid_string += f"    <<{stereotype}>>\n"

        if elem_type == "type:EnumerationType":
            for literal in element.findall("members", NAMESPACES):
                mermaid_string += f"    + {literal.get('name')}\n"
        else:
            for attr in element.findall("attributes", NAMESPACES):
                mermaid_string += f"    + {attr.get('name')}\n"
        mermaid_string += "  }\n"

        for rel in element.findall("relations", NAMESPACES):
            target_id = rel.get("target")
            if target_id and target_id in id_map:
                target_element = id_map[target_id]
                target_name = target_element.get("name")
                if target_name in element_names:
                    rel_name = rel.get("name", "")
                    cardinality = get_cardinality_string(rel)
                    relations_to_draw.append(
                        f'  {element_name} --> "{cardinality}" {target_name} : {rel_name}'
                    )

        for gen in element.findall("generalization", NAMESPACES):
            superclass_id = gen.get("general")
            if superclass_id and superclass_id in id_map:
                superclass_element = id_map[superclass_id]
                superclass_name = superclass_element.get("name")
                if superclass_name in element_names:
                    inheritance_to_draw.append(
                        f"  {superclass_name} <|-- {element_name}"
                    )

    for line in sorted(list(set(relations_to_draw + inheritance_to_draw))):
        mermaid_string += line + "\n"

    mermaid_string += "```\n\n"
    return mermaid_string


def main():
    """Main function to drive the diagram generation."""
    parser = argparse.ArgumentParser(
        description="Generate diagrams from Sirius .aird and ESM .model files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage from project root:
  # For PlantUML (default)
  python docs/domain/diagram_generator.py \\
    representations.aird \\
    application/model/target/generated-resources/model/kopogtato-esm.model \\
    docs/domain/generated-diagrams.md

  # For Mermaid
  python docs/domain/diagram_generator.py \\
    representations.aird \\
    application/model/target/generated-resources/model/kopogtato-esm.model \\
    docs/domain/generated-diagrams.md \\
    --format mermaid
""",
    )
    parser.add_argument("aird_path", help="Path to the representations.aird file.")
    parser.add_argument("model_path", help="Path to the ESM .model file.")
    parser.add_argument("output_path", help="Path to the output Markdown file.")
    parser.add_argument(
        "--format",
        choices=["plantuml", "mermaid"],
        default="plantuml",
        help="The output format for the diagrams (default: plantuml).",
    )
    args = parser.parse_args()

    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    try:
        aird_tree = ET.parse(args.aird_path)
    except FileNotFoundError:
        sys.exit(f"Error: aird file not found at '{args.aird_path}'")
    except ET.ParseError as e:
        sys.exit(f"Error: Could not parse aird file '{args.aird_path}'. Reason: {e}")

    diagram_defs = find_diagrams(aird_tree)
    if not diagram_defs:
        print("No entity diagrams found in the .aird file.")
        return

    try:
        _, id_map = parse_model(args.model_path)
    except FileNotFoundError:
        sys.exit(f"Error: model file not found at '{args.model_path}'")
    except ET.ParseError as e:
        sys.exit(f"Error: Could not parse model file '{args.model_path}'. Reason: {e}")

    output_md = f"# ESM Model Diagrams ({args.format.capitalize()})\n\n"
    output_md += (
        "This document is auto-generated by the `diagram_generator.py` script.\n\n"
    )

    for name, href in diagram_defs:
        target_id = href.split("#")[-1]
        if target_id not in id_map:
            print(
                f"Warning: Target ID '{target_id}' for diagram '{name}' not in model. Skipping."
            )
            continue

        target_package = id_map[target_id]
        elements = get_elements_from_package(target_package)

        if elements:
            print(f"Processing diagram: '{name}'...")
            if args.format == "plantuml":
                diagram_code = generate_plantuml_diagram(name, elements, id_map)
            else:
                diagram_code = generate_mermaid_diagram(name, elements, id_map)
            output_md += diagram_code
        else:
            print(
                f"Warning: No supported elements found for diagram '{name}'. Skipping."
            )

    try:
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write(output_md)
        print(
            f"\nSuccessfully generated {args.format.capitalize()} diagrams to {args.output_path}"
        )
    except IOError as e:
        sys.exit(
            f"Error: Could not write to output file '{args.output_path}'. Reason: {e}"
        )


if __name__ == "__main__":
    main()
